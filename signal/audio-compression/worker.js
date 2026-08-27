import { loadPyodide } from "../vendor/pyodide/pyodide.mjs";

const PYODIDE_URL = "../vendor/pyodide/";
let pyodide;

const ready = (async () => {
  const started = performance.now();
  pyodide = await loadPyodide({ indexURL: PYODIDE_URL });
  await pyodide.loadPackage("numpy");
  postMessage({ type: "ready", milliseconds: performance.now() - started });
})().catch((error) => postMessage({ type: "error", message: error.message || String(error) }));

function asFloat32(value) {
  if (value instanceof Float32Array) return value;
  const converted = value.toJs ? value.toJs() : value;
  if (value.destroy) value.destroy();
  return converted instanceof Float32Array ? converted : new Float32Array(converted);
}

self.addEventListener("message", async (event) => {
  if (event.data.type !== "run") return;
  await ready;
  const started = performance.now();
  try {
    pyodide.FS.writeFile("/tmp/audio.raw", new Uint8Array(event.data.samples));
    pyodide.globals.set("compression_ratio", event.data.ratio);
    await pyodide.runPythonAsync(event.data.code);

    const compressed = asFloat32(pyodide.globals.get("compressed_samples"));
    const originalSpectrum = asFloat32(pyodide.globals.get("original_spectrum_db"));
    const compressedSpectrum = asFloat32(pyodide.globals.get("compressed_spectrum_db"));
    const kept = Number(pyodide.globals.get("kept_count"));
    const total = Number(pyodide.globals.get("total_count"));
    const snr = Number(pyodide.globals.get("reconstruction_snr"));
    const reduction = Number(pyodide.globals.get("storage_reduction"));

    postMessage({
      type: "result",
      compressed,
      originalSpectrum,
      compressedSpectrum,
      kept,
      total,
      snr,
      reduction,
      milliseconds: performance.now() - started,
    }, [compressed.buffer, originalSpectrum.buffer, compressedSpectrum.buffer]);
  } catch (error) {
    postMessage({ type: "error", message: error.message || String(error) });
  }
});
