import { mountPythonHighlighting, showPythonError } from "../python-highlight.js?v=20260826-1";

const PYTHON_CODE = `import numpy as np

# The browser supplies two equally sized grayscale images as raw pixels.
image1 = np.fromfile("/tmp/image1.raw", dtype=np.uint8)
image2 = np.fromfile("/tmp/image2.raw", dtype=np.uint8)
image1 = image1.reshape((image_height, image_width)).astype(float)
image2 = image2.reshape((image_height, image_width)).astype(float)

# Separate each two-dimensional Fourier transform into magnitude and phase.
I1 = np.fft.fft2(image1)
I2 = np.fft.fft2(image2)
magnitude1, phase1 = np.abs(I1), np.angle(I1)
magnitude2, phase2 = np.abs(I2), np.angle(I2)

# Swap phases: I12 uses image 1 magnitude and image 2 phase, and vice versa.
image12 = np.fft.ifft2(magnitude1 * np.exp(1j * phase2)).real
image21 = np.fft.ifft2(magnitude2 * np.exp(1j * phase1)).real

def display_pixels(image):
    low, high = np.percentile(image, [1, 99])
    scaled = 255 * (image - low) / max(high - low, 1e-9)
    return np.clip(scaled, 0, 255).astype(np.uint8).tobytes()

image12_pixels = display_pixels(image12)
image21_pixels = display_pixels(image21)`;

const PROCESS_SIZE = 384;
const MAX_FILE_SIZE = 25 * 1024 * 1024;
const DEFAULT_IMAGES = [
  { source: "./zebra.png", label: "Zebra" },
  { source: "./leopard.png", label: "Leopard" },
];

const els = {
  code: document.querySelector("#python-code"),
  run: document.querySelector("#run-button"),
  stop: document.querySelector("#stop-button"),
  restore: document.querySelector("#restore-button"),
  status: document.querySelector("#runtime-status"),
  uploads: [document.querySelector("#image-1-upload"), document.querySelector("#image-2-upload")],
  titles: [document.querySelector("#image-1-title"), document.querySelector("#image-2-title")],
  sourceCanvases: [document.querySelector("#image-1-canvas"), document.querySelector("#image-2-canvas")],
  resultCanvases: [document.querySelector("#image-12-canvas"), document.querySelector("#image-21-canvas")],
  expandButtons: [
    document.querySelector("#expand-image-1"),
    document.querySelector("#expand-image-2"),
    document.querySelector("#expand-image-12"),
    document.querySelector("#expand-image-21"),
  ],
  summary: document.querySelector("#source-summary"),
  runTime: document.querySelector("#run-time"),
  lightbox: document.querySelector("#image-lightbox"),
  lightboxTitle: document.querySelector("#lightbox-title"),
  closeLightbox: document.querySelector("#close-lightbox"),
  expanded: document.querySelector("#expanded-canvas"),
};

const syncPythonHighlighting = mountPythonHighlighting(els.code);
const slots = [null, null];
let worker;
let ready = false;
let running = false;
let lightboxTrigger = null;

function setStatus(message, isError = false) {
  els.status.value = message;
  els.status.classList.toggle("is-error", isError);
}

function inputsReady() {
  return slots.every(Boolean);
}

function setRunning(value) {
  running = value;
  els.run.disabled = value || !ready || !inputsReady();
  els.stop.disabled = !value;
  els.restore.disabled = value;
  els.uploads.forEach((upload) => { upload.disabled = value; });
  els.run.textContent = value ? "Running…" : "Run code";
}

function drawGrayscale(canvas, pixels) {
  canvas.width = PROCESS_SIZE;
  canvas.height = PROCESS_SIZE;
  const context = canvas.getContext("2d");
  const imageData = context.createImageData(PROCESS_SIZE, PROCESS_SIZE);
  for (let source = 0, target = 0; source < pixels.length; source += 1, target += 4) {
    const value = pixels[source];
    imageData.data[target] = value;
    imageData.data[target + 1] = value;
    imageData.data[target + 2] = value;
    imageData.data[target + 3] = 255;
  }
  context.putImageData(imageData, 0, 0);
}

async function imagePixels(source) {
  const image = new Image();
  image.src = source;
  await image.decode();
  const canvas = document.createElement("canvas");
  canvas.width = PROCESS_SIZE;
  canvas.height = PROCESS_SIZE;
  const context = canvas.getContext("2d", { willReadFrequently: true });
  context.fillStyle = "#fff";
  context.fillRect(0, 0, PROCESS_SIZE, PROCESS_SIZE);
  const scale = Math.min(PROCESS_SIZE / image.naturalWidth, PROCESS_SIZE / image.naturalHeight);
  const width = Math.max(1, Math.round(image.naturalWidth * scale));
  const height = Math.max(1, Math.round(image.naturalHeight * scale));
  context.drawImage(image, Math.round((PROCESS_SIZE - width) / 2), Math.round((PROCESS_SIZE - height) / 2), width, height);
  const rgba = context.getImageData(0, 0, PROCESS_SIZE, PROCESS_SIZE).data;
  const pixels = new Uint8Array(PROCESS_SIZE * PROCESS_SIZE);
  for (let sourceIndex = 0, target = 0; sourceIndex < rgba.length; sourceIndex += 4, target += 1) {
    pixels[target] = Math.round(0.2126 * rgba[sourceIndex] + 0.7152 * rgba[sourceIndex + 1] + 0.0722 * rgba[sourceIndex + 2]);
  }
  return pixels;
}

function updateSummary() {
  if (!inputsReady()) return;
  els.summary.textContent = `${slots[0].label} + ${slots[1].label} · ${PROCESS_SIZE}×${PROCESS_SIZE} grayscale`;
}

function invalidateResults() {
  els.expandButtons[2].disabled = true;
  els.expandButtons[3].disabled = true;
  els.resultCanvases.forEach((canvas) => {
    canvas.width = PROCESS_SIZE;
    canvas.height = PROCESS_SIZE;
    canvas.getContext("2d").clearRect(0, 0, PROCESS_SIZE, PROCESS_SIZE);
  });
  els.runTime.textContent = "—";
}

async function setImage(slotIndex, source, label) {
  const pixels = await imagePixels(source);
  slots[slotIndex] = { pixels, label };
  drawGrayscale(els.sourceCanvases[slotIndex], pixels);
  els.titles[slotIndex].textContent = `Image ${slotIndex + 1} · ${label}`;
  els.expandButtons[slotIndex].disabled = false;
  invalidateResults();
  updateSummary();
  setRunning(false);
}

async function restoreDefaults() {
  setStatus("Loading zebra and leopard…");
  await Promise.all(DEFAULT_IMAGES.map((image, index) => setImage(index, image.source, image.label)));
  setStatus("Zebra and leopard ready");
  runCode();
}

async function loadUserImage(slotIndex, file) {
  if (!file) return;
  if (file.size > MAX_FILE_SIZE) throw new Error("Choose an image smaller than 25 MB.");
  const source = URL.createObjectURL(file);
  try {
    await setImage(slotIndex, source, file.name);
  } finally {
    URL.revokeObjectURL(source);
  }
  setStatus(`Loaded ${file.name} locally as image ${slotIndex + 1}`);
  runCode();
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
      drawGrayscale(els.resultCanvases[0], event.data.image12);
      drawGrayscale(els.resultCanvases[1], event.data.image21);
      els.expandButtons[2].disabled = false;
      els.expandButtons[3].disabled = false;
      els.runTime.textContent = `Python ${event.data.milliseconds.toFixed(0)} ms`;
      setStatus("Phases swapped locally in Python WebAssembly");
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
  if (!ready || running || !inputsReady()) return;
  setRunning(true);
  invalidateResults();
  setStatus("Swapping Fourier magnitude and phase…");
  const image1 = slots[0].pixels.slice();
  const image2 = slots[1].pixels.slice();
  worker.postMessage({
    type: "run",
    code: els.code.value,
    image1: image1.buffer,
    image2: image2.buffer,
    width: PROCESS_SIZE,
    height: PROCESS_SIZE,
  }, [image1.buffer, image2.buffer]);
}

function openLightbox(canvas, title, trigger) {
  if (!canvas.width || !canvas.height || trigger.disabled) return;
  lightboxTrigger = trigger;
  els.expanded.width = canvas.width;
  els.expanded.height = canvas.height;
  els.expanded.getContext("2d").drawImage(canvas, 0, 0);
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
els.restore.addEventListener("click", () => { void restoreDefaults().catch((error) => setStatus(error.message, true)); });
els.uploads.forEach((upload, index) => {
  upload.addEventListener("change", () => {
    const file = upload.files?.[0];
    upload.value = "";
    if (file) void loadUserImage(index, file).catch((error) => setStatus(error.message, true));
  });
});

const lightboxSources = [
  { canvas: els.sourceCanvases[0], title: () => els.titles[0].textContent },
  { canvas: els.sourceCanvases[1], title: () => els.titles[1].textContent },
  { canvas: els.resultCanvases[0], title: () => "Magnitude 1 + phase 2" },
  { canvas: els.resultCanvases[1], title: () => "Magnitude 2 + phase 1" },
];
els.expandButtons.forEach((button, index) => {
  button.addEventListener("click", () => openLightbox(lightboxSources[index].canvas, lightboxSources[index].title(), button));
});
els.closeLightbox.addEventListener("click", closeLightbox);
els.lightbox.addEventListener("click", (event) => { if (event.target === els.lightbox) closeLightbox(); });
window.addEventListener("keydown", (event) => { if (event.key === "Escape") closeLightbox(); });

void restoreDefaults().catch((error) => setStatus(error.message, true));
startWorker();
