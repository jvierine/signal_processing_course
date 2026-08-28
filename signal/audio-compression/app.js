import { mountPythonHighlighting, showPythonError } from "../python-highlight.js?v=20260826-1";

const PYTHON_CODE = `import numpy as np

def compress_audio(samples, compression_ratio=0.90):
    spectrum = np.fft.rfft(samples)
    total = spectrum.size

    weakest_first = np.argsort(np.abs(spectrum))
    remove_count = min(total - 1, int(total * compression_ratio))
    spectrum[weakest_first[:remove_count]] = 0.0

    reconstructed = np.fft.irfft(spectrum, n=samples.size).real
    return reconstructed, spectrum

# The browser supplies a mono floating-point audio signal.
samples = np.fromfile("/tmp/audio.raw", dtype=np.float32)
original_fft = np.fft.rfft(samples)
compressed, compressed_fft = compress_audio(samples, compression_ratio)

# Pool the spectra into compact arrays for browser plotting.
def spectrum_envelope(values, bins=1200):
    power_db = 20 * np.log10(np.abs(values) + 1e-12)
    edges = np.linspace(0, power_db.size, min(bins, power_db.size) + 1, dtype=int)
    return np.array([np.max(power_db[edges[i]:max(edges[i] + 1, edges[i + 1])])
                     for i in range(edges.size - 1)], dtype=np.float32)

original_spectrum_db = spectrum_envelope(original_fft)
compressed_spectrum_db = spectrum_envelope(compressed_fft)
compressed_samples = np.asarray(compressed, dtype=np.float32)

kept_count = int(np.count_nonzero(compressed_fft))
total_count = int(compressed_fft.size)
signal_power = float(np.sum(samples ** 2))
error_power = float(np.sum((samples - compressed) ** 2))
reconstruction_snr = float(10 * np.log10(signal_power / max(error_power, 1e-24)))

# Approximate the course example: 16-bit input samples versus an index and
# two 8-bit spectral values for each retained coefficient, plus one scale.
original_bits = 16 * samples.size
compressed_bits = 32 * kept_count + 32
storage_reduction = float(1 - compressed_bits / original_bits)`;

const els = {
  slider: document.querySelector("#compression-slider"),
  ratio: document.querySelector("#compression-output"),
  run: document.querySelector("#run-button"),
  stop: document.querySelector("#stop-button"),
  status: document.querySelector("#runtime-status"),
  upload: document.querySelector("#source-audio"),
  code: document.querySelector("#python-code"),
  originalWaveform: document.querySelector("#original-waveform"),
  originalSpectrum: document.querySelector("#original-spectrum"),
  compressedWaveform: document.querySelector("#compressed-waveform"),
  compressedSpectrum: document.querySelector("#compressed-spectrum"),
  originalPlayer: document.querySelector("#original-player"),
  compressedPlayer: document.querySelector("#compressed-player"),
  compressedTitle: document.querySelector("#compressed-title"),
  kept: document.querySelector("#kept-value"),
  reduction: document.querySelector("#reduction-value"),
  snr: document.querySelector("#snr-value"),
  runTime: document.querySelector("#run-time"),
  sourceName: document.querySelector("#source-name"),
  waveformRanges: document.querySelectorAll(".waveform-range"),
  waveformResets: document.querySelectorAll(".waveform-reset"),
};

const syncPythonHighlighting = mountPythonHighlighting(els.code);
const COMPRESSION_RATIOS = [0.5, 0.75, 0.9, 0.95, 0.975, 0.99];
const MAX_SECONDS = 20;
const MAX_FILE_BYTES = 30 * 1024 * 1024;

let worker;
let ready = false;
let running = false;
let sourceSamples;
let compressedSamples;
let sampleRate = 44100;
let originalSpectrum;
let compressedSpectrum;
let originalAudioUrl;
let compressedAudioUrl;
let waveformViewStart = 0;
let waveformViewEnd = 1;

const WAVEFORM_MARGIN_LEFT = 34;
const WAVEFORM_MARGIN_RIGHT = 8;

function selectedRatio() {
  return COMPRESSION_RATIOS[Number(els.slider.value)] ?? COMPRESSION_RATIOS[2];
}

function formatRatio(ratio) {
  return `${Number((ratio * 100).toFixed(1))}%`;
}

function updateRatioLabel() {
  const label = formatRatio(selectedRatio());
  els.ratio.value = label;
  els.slider.setAttribute("aria-valuetext", `${label} of Fourier components removed`);
  els.compressedTitle.textContent = `${label} removed`;
}

function setStatus(message, isError = false) {
  els.status.value = message;
  els.status.classList.toggle("is-error", isError);
}

function setRunning(value) {
  running = value;
  els.run.disabled = value || !ready || !sourceSamples;
  els.stop.disabled = !value;
  els.upload.disabled = value;
  els.run.textContent = value ? "Running…" : "Run code";
}

function canvasContext(canvas) {
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  const width = Math.max(260, Math.round(canvas.clientWidth));
  const height = Math.max(100, Math.round(canvas.clientHeight));
  canvas.width = Math.round(width * ratio);
  canvas.height = Math.round(height * ratio);
  const context = canvas.getContext("2d");
  context.setTransform(ratio, 0, 0, ratio, 0, 0);
  return { context, width, height };
}

function plotFrame(context, width, height, xEndLabel, xStartLabel = "0") {
  context.clearRect(0, 0, width, height);
  context.fillStyle = "#f4f5f3";
  context.fillRect(0, 0, width, height);
  context.strokeStyle = "#d9ddd7";
  context.lineWidth = 1;
  context.beginPath();
  context.moveTo(34, 10);
  context.lineTo(34, height - 22);
  context.lineTo(width - 8, height - 22);
  context.stroke();
  context.fillStyle = "#66736f";
  context.font = "10px system-ui, sans-serif";
  context.fillText(xStartLabel, 30, height - 7);
  context.textAlign = "right";
  context.fillText(xEndLabel, width - 8, height - 7);
  context.textAlign = "left";
  return { left: 34, top: 10, right: width - 8, bottom: height - 22 };
}

function drawWaveform(canvas, samples) {
  if (!samples?.length) return;
  const { context, width, height } = canvasContext(canvas);
  const startIndex = Math.max(0, Math.floor(waveformViewStart * samples.length));
  const endIndex = Math.min(samples.length, Math.max(startIndex + 1, Math.ceil(waveformViewEnd * samples.length)));
  const startSeconds = startIndex / sampleRate;
  const endSeconds = endIndex / sampleRate;
  const decimals = endSeconds - startSeconds < 1 ? 3 : endSeconds - startSeconds < 10 ? 2 : 1;
  const bounds = plotFrame(context, width, height, `${endSeconds.toFixed(decimals)} s`, `${startSeconds.toFixed(decimals)} s`);
  const center = (bounds.top + bounds.bottom) / 2;
  const amplitude = (bounds.bottom - bounds.top) * 0.46;
  const columns = Math.max(1, Math.floor(bounds.right - bounds.left));
  const step = (endIndex - startIndex) / columns;
  context.strokeStyle = "#0072b2";
  context.lineWidth = 1;
  context.beginPath();
  for (let column = 0; column < columns; column += 1) {
    const start = startIndex + Math.floor(column * step);
    const end = Math.max(start + 1, startIndex + Math.floor((column + 1) * step));
    let low = 1;
    let high = -1;
    for (let index = start; index < end && index < samples.length; index += 1) {
      low = Math.min(low, samples[index]);
      high = Math.max(high, samples[index]);
    }
    const x = bounds.left + column;
    context.moveTo(x, center - high * amplitude);
    context.lineTo(x, center - low * amplitude);
  }
  context.stroke();
}

function waveformSpan() {
  return waveformViewEnd - waveformViewStart;
}

function minimumWaveformSpan() {
  return sourceSamples?.length ? Math.min(1, Math.max(256 / sourceSamples.length, 0.0005)) : 0.0005;
}

function setWaveformView(start, end) {
  const span = Math.min(1, Math.max(minimumWaveformSpan(), end - start));
  waveformViewStart = Math.max(0, Math.min(1 - span, start));
  waveformViewEnd = waveformViewStart + span;
  drawWaveformViews();
}

function resetWaveformView() {
  waveformViewStart = 0;
  waveformViewEnd = 1;
  drawWaveformViews();
}

function zoomWaveform(focus, factor) {
  const oldSpan = waveformSpan();
  const newSpan = Math.min(1, Math.max(minimumWaveformSpan(), oldSpan * factor));
  const absoluteFocus = waveformViewStart + Math.max(0, Math.min(1, focus)) * oldSpan;
  setWaveformView(absoluteFocus - Math.max(0, Math.min(1, focus)) * newSpan, absoluteFocus + (1 - Math.max(0, Math.min(1, focus))) * newSpan);
}

function panWaveform(fraction) {
  const span = waveformSpan();
  setWaveformView(waveformViewStart + fraction * span, waveformViewEnd + fraction * span);
}

function drawWaveformViews() {
  drawWaveform(els.originalWaveform, sourceSamples);
  drawWaveform(els.compressedWaveform, compressedSamples);
  if (!sourceSamples?.length) return;
  const start = waveformViewStart * sourceSamples.length / sampleRate;
  const end = waveformViewEnd * sourceSamples.length / sampleRate;
  const full = waveformSpan() > 0.999999;
  const decimals = end - start < 1 ? 3 : end - start < 10 ? 2 : 1;
  const label = full ? "Full waveform" : `${start.toFixed(decimals)}–${end.toFixed(decimals)} s`;
  els.waveformRanges.forEach((element) => { element.textContent = label; });
  els.waveformResets.forEach((button) => { button.disabled = full; });
}

function waveformFraction(canvas, clientX) {
  const rectangle = canvas.getBoundingClientRect();
  const plotWidth = Math.max(1, rectangle.width - WAVEFORM_MARGIN_LEFT - WAVEFORM_MARGIN_RIGHT);
  return Math.max(0, Math.min(1, (clientX - rectangle.left - WAVEFORM_MARGIN_LEFT) / plotWidth));
}

function bindWaveformInteraction(canvas) {
  const pointers = new Map();
  let gesture;

  canvas.addEventListener("wheel", (event) => {
    event.preventDefault();
    zoomWaveform(waveformFraction(canvas, event.clientX), Math.exp(event.deltaY * 0.0015));
  }, { passive: false });

  canvas.addEventListener("dblclick", resetWaveformView);
  canvas.addEventListener("pointerdown", (event) => {
    canvas.setPointerCapture(event.pointerId);
    pointers.set(event.pointerId, { x: event.clientX });
    canvas.classList.add("is-panning");
    if (pointers.size === 1) {
      gesture = { kind: "pan", x: event.clientX, start: waveformViewStart, end: waveformViewEnd };
    } else if (pointers.size === 2) {
      const values = [...pointers.values()];
      const center = (values[0].x + values[1].x) / 2;
      gesture = {
        kind: "pinch",
        distance: Math.max(1, Math.abs(values[0].x - values[1].x)),
        focus: waveformViewStart + waveformFraction(canvas, center) * waveformSpan(),
      };
    }
  });

  canvas.addEventListener("pointermove", (event) => {
    if (!pointers.has(event.pointerId)) return;
    pointers.set(event.pointerId, { x: event.clientX });
    if (pointers.size === 2 && gesture?.kind === "pinch") {
      const values = [...pointers.values()];
      const distance = Math.max(1, Math.abs(values[0].x - values[1].x));
      const center = (values[0].x + values[1].x) / 2;
      const newSpan = Math.min(1, Math.max(minimumWaveformSpan(), waveformSpan() * gesture.distance / distance));
      const focus = waveformFraction(canvas, center);
      setWaveformView(gesture.focus - focus * newSpan, gesture.focus + (1 - focus) * newSpan);
      gesture.distance = distance;
      gesture.focus = waveformViewStart + focus * waveformSpan();
    } else if (pointers.size === 1 && gesture?.kind === "pan") {
      const rectangle = canvas.getBoundingClientRect();
      const plotWidth = Math.max(1, rectangle.width - WAVEFORM_MARGIN_LEFT - WAVEFORM_MARGIN_RIGHT);
      const shift = (gesture.x - event.clientX) / plotWidth * (gesture.end - gesture.start);
      setWaveformView(gesture.start + shift, gesture.end + shift);
    }
  });

  const endPointer = (event) => {
    pointers.delete(event.pointerId);
    if (pointers.size === 0) {
      gesture = undefined;
      canvas.classList.remove("is-panning");
    } else {
      const remaining = [...pointers.values()][0];
      gesture = { kind: "pan", x: remaining.x, start: waveformViewStart, end: waveformViewEnd };
    }
  };
  canvas.addEventListener("pointerup", endPointer);
  canvas.addEventListener("pointercancel", endPointer);

  canvas.addEventListener("keydown", (event) => {
    if (event.key === "+" || event.key === "=") zoomWaveform(0.5, 0.8);
    else if (event.key === "-") zoomWaveform(0.5, 1.25);
    else if (event.key === "ArrowLeft") panWaveform(-0.1);
    else if (event.key === "ArrowRight") panWaveform(0.1);
    else if (event.key === "0" || event.key === "Home") resetWaveformView();
    else return;
    event.preventDefault();
  });
}

function drawSpectrum(canvas, values) {
  if (!values?.length) return;
  const { context, width, height } = canvasContext(canvas);
  const bounds = plotFrame(context, width, height, `${(sampleRate / 2000).toFixed(1)} kHz`);
  const finite = Array.from(values).filter(Number.isFinite);
  const high = Math.max(...finite, -20);
  const low = high - 100;
  context.fillStyle = "#66736f";
  context.font = "10px system-ui, sans-serif";
  context.fillText(`${Math.round(high)} dB`, 2, 18);
  context.fillText(`${Math.round(low)} dB`, 2, bounds.bottom);
  context.strokeStyle = "#0072b2";
  context.lineWidth = 1.5;
  context.beginPath();
  values.forEach((value, index) => {
    const x = bounds.left + (index / Math.max(1, values.length - 1)) * (bounds.right - bounds.left);
    const normalized = Math.max(0, Math.min(1, (value - low) / (high - low)));
    const y = bounds.bottom - normalized * (bounds.bottom - bounds.top);
    if (index === 0) context.moveTo(x, y); else context.lineTo(x, y);
  });
  context.stroke();
}

function wavBlob(samples, rate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);
  const text = (offset, value) => { for (let index = 0; index < value.length; index += 1) view.setUint8(offset + index, value.charCodeAt(index)); };
  text(0, "RIFF");
  view.setUint32(4, 36 + samples.length * 2, true);
  text(8, "WAVE");
  text(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, rate, true);
  view.setUint32(28, rate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  text(36, "data");
  view.setUint32(40, samples.length * 2, true);
  for (let index = 0; index < samples.length; index += 1) {
    const value = Math.max(-1, Math.min(1, samples[index]));
    view.setInt16(44 + index * 2, value < 0 ? value * 32768 : value * 32767, true);
  }
  return new Blob([buffer], { type: "audio/wav" });
}

function setPlayer(player, samples, kind) {
  if (kind === "original" && originalAudioUrl) URL.revokeObjectURL(originalAudioUrl);
  if (kind === "compressed" && compressedAudioUrl) URL.revokeObjectURL(compressedAudioUrl);
  const url = URL.createObjectURL(wavBlob(samples, sampleRate));
  if (kind === "original") originalAudioUrl = url; else compressedAudioUrl = url;
  player.src = url;
  player.load();
}

function startWorker() {
  ready = false;
  setRunning(false);
  setStatus("Starting local Python WebAssembly…");
  worker = new Worker("./worker.js?v=20260826-2", { type: "module" });
  worker.addEventListener("message", (event) => {
    if (event.data.type === "ready") {
      ready = true;
      setRunning(false);
      setStatus(`Python ready · ${(event.data.milliseconds / 1000).toFixed(1)} s initial load`);
      runCode();
      return;
    }
    if (event.data.type === "result") {
      compressedSamples = event.data.compressed;
      originalSpectrum = event.data.originalSpectrum;
      compressedSpectrum = event.data.compressedSpectrum;
      drawWaveformViews();
      drawSpectrum(els.originalSpectrum, originalSpectrum);
      drawSpectrum(els.compressedSpectrum, compressedSpectrum);
      setPlayer(els.compressedPlayer, compressedSamples, "compressed");
      els.kept.textContent = `${event.data.kept.toLocaleString()} / ${event.data.total.toLocaleString()}`;
      els.reduction.textContent = `${Math.max(0, event.data.reduction * 100).toFixed(1)}%`;
      els.snr.textContent = `${event.data.snr.toFixed(1)} dB`;
      els.runTime.textContent = `Python ${event.data.milliseconds.toFixed(0)} ms`;
      setStatus("Reconstructed locally · use the players to compare");
      setRunning(false);
      return;
    }
    if (event.data.type === "error") {
      setStatus(showPythonError(els.code, event.data.message), true);
      setRunning(false);
    }
  });
  worker.addEventListener("error", (event) => {
    setStatus(event.message || "Python worker failed to start", true);
    setRunning(false);
  });
}

function runCode() {
  if (!ready || running || !sourceSamples) return;
  els.originalPlayer.pause();
  els.compressedPlayer.pause();
  setRunning(true);
  setStatus("Running NumPy real FFT…");
  const samples = sourceSamples.slice();
  worker.postMessage({ type: "run", code: els.code.value, samples: samples.buffer, ratio: selectedRatio() }, [samples.buffer]);
}

async function decodeAudio(data, label) {
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  if (!AudioContextClass) throw new Error("This browser does not support Web Audio.");
  const context = new AudioContextClass();
  try {
    const decoded = await context.decodeAudioData(data.slice(0));
    sampleRate = decoded.sampleRate;
    const length = Math.min(decoded.length, Math.floor(MAX_SECONDS * sampleRate));
    sourceSamples = new Float32Array(length);
    for (let channel = 0; channel < decoded.numberOfChannels; channel += 1) {
      const values = decoded.getChannelData(channel);
      for (let index = 0; index < length; index += 1) sourceSamples[index] += values[index] / decoded.numberOfChannels;
    }
  } finally {
    await context.close();
  }
  compressedSamples = undefined;
  originalSpectrum = undefined;
  compressedSpectrum = undefined;
  waveformViewStart = 0;
  waveformViewEnd = 1;
  setPlayer(els.originalPlayer, sourceSamples, "original");
  els.compressedPlayer.removeAttribute("src");
  els.compressedPlayer.load();
  drawWaveformViews();
  els.sourceName.textContent = `${label} · ${(sourceSamples.length / sampleRate).toFixed(1)} s mono · ${(sampleRate / 1000).toFixed(1)} kHz`;
  els.kept.textContent = "—";
  els.reduction.textContent = "—";
  els.snr.textContent = "—";
  els.runTime.textContent = "—";
  setRunning(false);
  if (ready) runCode();
}

async function loadDefault() {
  const response = await fetch("./fur-elise.wav");
  if (!response.ok) throw new Error("Unable to load Für Elise.");
  await decodeAudio(await response.arrayBuffer(), "Für Elise");
}

async function loadUpload(file) {
  if (!file) throw new Error("Choose an audio file.");
  if (file.size > MAX_FILE_BYTES) throw new Error("Choose an audio file smaller than 30 MB.");
  try {
    await decodeAudio(await file.arrayBuffer(), file.name);
  } catch {
    throw new Error("This browser could not decode that audio file. Try WAV, MP3, M4A, Ogg, FLAC, or WebM.");
  }
  setStatus(`Loaded ${file.name} locally${sourceSamples.length >= MAX_SECONDS * sampleRate ? " · using first 20 s" : ""}`);
}

els.code.value = PYTHON_CODE;
syncPythonHighlighting();
els.run.addEventListener("click", runCode);
els.stop.addEventListener("click", () => {
  worker.terminate();
  setStatus("Python stopped · restarting…");
  startWorker();
});
els.slider.addEventListener("input", updateRatioLabel);
els.slider.addEventListener("change", runCode);
els.upload.addEventListener("change", () => {
  const file = els.upload.files?.[0];
  els.upload.value = "";
  if (file) void loadUpload(file).catch((error) => setStatus(error.message, true));
});
els.waveformResets.forEach((button) => button.addEventListener("click", resetWaveformView));
bindWaveformInteraction(els.originalWaveform);
bindWaveformInteraction(els.compressedWaveform);
window.addEventListener("resize", () => {
  drawWaveformViews();
  drawSpectrum(els.originalSpectrum, originalSpectrum);
  drawSpectrum(els.compressedSpectrum, compressedSpectrum);
});
window.addEventListener("beforeunload", () => {
  if (originalAudioUrl) URL.revokeObjectURL(originalAudioUrl);
  if (compressedAudioUrl) URL.revokeObjectURL(compressedAudioUrl);
});

updateRatioLabel();
void loadDefault().catch((error) => setStatus(error.message, true));
startWorker();
