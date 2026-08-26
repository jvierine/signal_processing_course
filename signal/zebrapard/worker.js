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
    pyodide.FS.writeFile("/tmp/image1.raw", new Uint8Array(event.data.image1));
    pyodide.FS.writeFile("/tmp/image2.raw", new Uint8Array(event.data.image2));
    pyodide.globals.set("image_width", event.data.width);
    pyodide.globals.set("image_height", event.data.height);
    await pyodide.runPythonAsync(event.data.code);

    const image12 = asUint8(pyodide.globals.get("image12_pixels"));
    const image21 = asUint8(pyodide.globals.get("image21_pixels"));
    postMessage({
      type: "result",
      image12,
      image21,
      milliseconds: performance.now() - started,
    }, [image12.buffer, image21.buffer]);
  } catch (error) {
    postMessage({ type: "error", message: error.message || String(error) });
  }
});
