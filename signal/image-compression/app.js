import { mountPythonHighlighting, showPythonError } from "../python-highlight.js?v=20260826-1";

const PYTHON_CODE = `import numpy as np

def compress_image(image, compression_ratio=0.9):
    image_fft = np.fft.fft2(image)
    total = image_fft.size

    flat_fft = image_fft.flatten()
    weakest_first = np.argsort(np.abs(flat_fft))
    remove_count = min(total - 1, int(total * compression_ratio))
    flat_fft[weakest_first[:remove_count]] = 0.0
    image_fft = flat_fft.reshape(image.shape)

    compressed = np.fft.ifft2(image_fft).real
    return compressed, image_fft

# The browser supplies the grayscale image as raw pixels.
image = np.fromfile("/tmp/image.raw", dtype=np.uint8)
image = image.reshape((image_height, image_width)).astype(float)
# compression_ratio is read from the browser slider.
compressed, compressed_fft = compress_image(image, compression_ratio)

# Convert results to compact byte arrays for the four canvases.
original_fft = np.fft.fft2(image)
original_db = 20 * np.log10(np.abs(np.fft.fftshift(original_fft)) + 1e-9)
compressed_db = 20 * np.log10(np.abs(np.fft.fftshift(compressed_fft)) + 1e-9)
low, high = np.percentile(original_db, [5, 99.5])

def display_spectrum(values):
    scaled = 255 * (values - low) / max(high - low, 1e-9)
    return np.clip(scaled, 0, 255).astype(np.uint8).tobytes()

compressed_pixels = np.clip(compressed, 0, 255).astype(np.uint8).tobytes()
original_spectrum = display_spectrum(original_db)
compressed_spectrum = display_spectrum(compressed_db)
kept_count = int(np.count_nonzero(compressed_fft))
total_count = int(compressed_fft.size)
reconstruction_rmse = float(np.sqrt(np.mean((image - compressed) ** 2)))`;

const els = {
  slider: document.querySelector("#compression-slider"),
  ratio: document.querySelector("#compression-output"),
  run: document.querySelector("#run-button"),
  stop: document.querySelector("#stop-button"),
  status: document.querySelector("#runtime-status"),
  upload: document.querySelector("#source-image"),
  code: document.querySelector("#python-code"),
  original: document.querySelector("#original-canvas"),
  originalSpectrum: document.querySelector("#original-spectrum"),
  compressed: document.querySelector("#compressed-canvas"),
  compressedSpectrum: document.querySelector("#compressed-spectrum"),
  compressedTitle: document.querySelector("#compressed-title"),
  kept: document.querySelector("#kept-value"),
  rmse: document.querySelector("#rmse-value"),
  runTime: document.querySelector("#run-time"),
  sourceName: document.querySelector("#source-name"),
  expandOriginal: document.querySelector("#expand-original"),
  expandCompressed: document.querySelector("#expand-compressed"),
  lightbox: document.querySelector("#image-lightbox"),
  lightboxTitle: document.querySelector("#lightbox-title"),
  closeLightbox: document.querySelector("#close-lightbox"),
  expanded: document.querySelector("#expanded-canvas"),
};
const syncPythonHighlighting = mountPythonHighlighting(els.code);
const COMPRESSION_RATIOS = [0.1, 0.5, 0.8, 0.9, 0.99, 0.999, 0.9999];
const MAX_IMAGE_PIXELS = 1_600_000;

let worker;
let ready = false;
let running = false;
let sourcePixels;
let imageWidth = 0;
let imageHeight = 0;
let lightboxTrigger = null;

function selectedRatio() {
  return COMPRESSION_RATIOS[Number(els.slider.value)] ?? COMPRESSION_RATIOS[3];
}

function formatRatio(ratio) {
  return `${Number((ratio * 100).toFixed(2))}%`;
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
  els.run.disabled = value || !ready || !sourcePixels;
  els.stop.disabled = !value;
  els.upload.disabled = value;
  els.run.textContent = value ? "Running…" : "Run code";
}

function drawGrayscale(canvas, pixels, width, height) {
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext("2d");
  const imageData = context.createImageData(width, height);
  for (let source = 0, target = 0; source < pixels.length; source += 1, target += 4) {
    const value = pixels[source];
    imageData.data[target] = value;
    imageData.data[target + 1] = value;
    imageData.data[target + 2] = value;
    imageData.data[target + 3] = 255;
  }
  context.putImageData(imageData, 0, 0);
}

function startWorker() {
  ready = false;
  setRunning(false);
  setStatus("Starting local Python WebAssembly…");
  worker = new Worker("./worker.js?v=20260826-1", { type: "module" });
  worker.addEventListener("message", (event) => {
    if (event.data.type === "ready") {
      ready = true;
      setRunning(false);
      setStatus(`Python ready · ${(event.data.milliseconds / 1000).toFixed(1)} s initial load`);
      runCode();
      return;
    }
    if (event.data.type === "result") {
      drawGrayscale(els.compressed, event.data.compressed, imageWidth, imageHeight);
      drawGrayscale(els.originalSpectrum, event.data.originalSpectrum, imageWidth, imageHeight);
      drawGrayscale(els.compressedSpectrum, event.data.compressedSpectrum, imageWidth, imageHeight);
      els.kept.textContent = `${event.data.kept.toLocaleString()} / ${event.data.total.toLocaleString()}`;
      els.rmse.textContent = event.data.rmse.toFixed(2);
      els.runTime.textContent = `Python ${(event.data.milliseconds).toFixed(0)} ms`;
      els.expandCompressed.disabled = false;
      setStatus("Executed locally in Python WebAssembly");
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
  if (!ready || running || !sourcePixels) return;
  setRunning(true);
  setStatus("Running NumPy 2D FFT…");
  const pixels = sourcePixels.slice();
  worker.postMessage({
    type: "run",
    code: els.code.value,
    pixels: pixels.buffer,
    width: imageWidth,
    height: imageHeight,
    ratio: selectedRatio(),
  }, [pixels.buffer]);
}

async function loadSourceImage(source, label) {
  const image = new Image();
  image.src = source;
  await image.decode();
  const scale = Math.min(1, Math.sqrt(MAX_IMAGE_PIXELS / (image.naturalWidth * image.naturalHeight)));
  imageWidth = Math.max(1, Math.round(image.naturalWidth * scale));
  imageHeight = Math.max(1, Math.round(image.naturalHeight * scale));
  const canvas = document.createElement("canvas");
  canvas.width = imageWidth;
  canvas.height = imageHeight;
  const context = canvas.getContext("2d", { willReadFrequently: true });
  context.drawImage(image, 0, 0, imageWidth, imageHeight);
  const rgba = context.getImageData(0, 0, imageWidth, imageHeight).data;
  sourcePixels = new Uint8Array(imageWidth * imageHeight);
  for (let source = 0, target = 0; source < rgba.length; source += 4, target += 1) {
    sourcePixels[target] = Math.round(0.2126 * rgba[source] + 0.7152 * rgba[source + 1] + 0.0722 * rgba[source + 2]);
  }
  drawGrayscale(els.original, sourcePixels, imageWidth, imageHeight);
  els.sourceName.textContent = `${label} · ${imageWidth}×${imageHeight} · click either image to expand`;
  els.expandOriginal.disabled = false;
  els.expandCompressed.disabled = true;
  els.kept.textContent = "—";
  els.rmse.textContent = "—";
  els.runTime.textContent = "—";
  setRunning(false);
}

async function loadUserImage(file) {
  if (!file) throw new Error("Choose an image file.");
  if (file.size > 25 * 1024 * 1024) throw new Error("Choose an image smaller than 25 MB.");
  const url = URL.createObjectURL(file);
  try {
    await loadSourceImage(url, file.name);
  } finally {
    URL.revokeObjectURL(url);
  }
  setStatus(`Loaded ${file.name} locally${imageWidth * imageHeight >= MAX_IMAGE_PIXELS ? " · resized for browser processing" : ""}`);
  runCode();
}

function openLightbox(source, title, trigger) {
  if (!source.width || !source.height) return;
  lightboxTrigger = trigger;
  els.expanded.width = source.width;
  els.expanded.height = source.height;
  els.expanded.getContext("2d").drawImage(source, 0, 0);
  els.lightboxTitle.textContent = title;
  els.lightbox.hidden = false;
  document.body.classList.add("lightbox-open");
  els.closeLightbox.focus();
}

function closeLightbox() {
  if (els.lightbox.hidden) return;
  els.lightbox.hidden = true;
  document.body.classList.remove("lightbox-open");
  lightboxTrigger?.focus();
  lightboxTrigger = null;
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
  if (file) void loadUserImage(file).catch((error) => setStatus(error.message, true));
});
els.expandOriginal.addEventListener("click", () => openLightbox(els.original, "Original image", els.expandOriginal));
els.expandCompressed.addEventListener("click", () => openLightbox(els.compressed, `${formatRatio(selectedRatio())} removed`, els.expandCompressed));
els.closeLightbox.addEventListener("click", closeLightbox);
els.lightbox.addEventListener("click", (event) => { if (event.target === els.lightbox) closeLightbox(); });
window.addEventListener("keydown", (event) => { if (event.key === "Escape") closeLightbox(); });

updateRatioLabel();
loadSourceImage("./husky.jpg", "Built-in husky").then(() => { if (ready) runCode(); }).catch((error) => setStatus(error.message, true));
startWorker();
