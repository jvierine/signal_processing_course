import { loadPyodide } from "../vendor/pyodide/pyodide.mjs";

const PYODIDE_URL = "../vendor/pyodide/";
let pyodide;

const ready = (async () => {
  const started = performance.now();
  pyodide = await loadPyodide({ indexURL: PYODIDE_URL });
  await pyodide.loadPackage("numpy");
  postMessage({ type: "ready", milliseconds: performance.now() - started });
})().catch((error) => postMessage({ type: "error", message: error.message || String(error) }));

function asUint8(value) {
  if (value instanceof Uint8Array) return value;
  const converted = value.toJs ? value.toJs() : value;
  if (value.destroy) value.destroy();
  return converted instanceof Uint8Array ? converted : new Uint8Array(converted);
}

self.addEventListener("message", async (event) => {
  if (event.data.type !== "run") return;
  await ready;
  const started = performance.now();
  try {
    pyodide.FS.writeFile("/tmp/image.raw", new Uint8Array(event.data.pixels));
    pyodide.globals.set("image_width", event.data.width);
    pyodide.globals.set("image_height", event.data.height);
    pyodide.globals.set("compression_ratio", event.data.ratio);
    await pyodide.runPythonAsync(event.data.code);

    const compressed = asUint8(pyodide.globals.get("compressed_pixels"));
    const originalSpectrum = asUint8(pyodide.globals.get("original_spectrum"));
    const compressedSpectrum = asUint8(pyodide.globals.get("compressed_spectrum"));
    const kept = Number(pyodide.globals.get("kept_count"));
    const total = Number(pyodide.globals.get("total_count"));
    const rmse = Number(pyodide.globals.get("reconstruction_rmse"));

    postMessage({
      type: "result",
      compressed,
      originalSpectrum,
      compressedSpectrum,
      kept,
      total,
      rmse,
      milliseconds: performance.now() - started,
    }, [compressed.buffer, originalSpectrum.buffer, compressedSpectrum.buffer]);
  } catch (error) {
    postMessage({ type: "error", message: error.message || String(error) });
  }
});
