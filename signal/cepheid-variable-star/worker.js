import { loadPyodide } from "../vendor/pyodide/pyodide.mjs";

const PYODIDE_URL = "../vendor/pyodide/";
let pyodide;

const ready = (async () => {
  const started = performance.now();
  const dataResponse = await fetch(new URL("./lcb1.dat", import.meta.url));
  if (!dataResponse.ok) throw new Error("Could not load the Cepheid observations.");
  const data = await dataResponse.text();
  pyodide = await loadPyodide({ indexURL: PYODIDE_URL });
  await pyodide.loadPackage("numpy");
  pyodide.FS.writeFile("/tmp/lcb1.dat", data);
  postMessage({ type: "ready", milliseconds: performance.now() - started });
})().catch((error) => postMessage({ type: "error", message: error.message || String(error) }));

function bytes(name) {
  const value = pyodide.globals.get(name);
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
    await pyodide.runPythonAsync(event.data.code);
    const rawTime = bytes("raw_time_bytes");
    const phaseTime = bytes("phase_time_bytes");
    const magnitude = bytes("magnitude_bytes");
    const modelTime = bytes("model_time_bytes");
    const modelValue = bytes("model_value_bytes");
    const rmse = Number(pyodide.globals.get("fit_rmse"));
    const period = Number(pyodide.globals.get("T"));
    const coefficientCount = Number(pyodide.globals.get("coefficient_count"));
    postMessage({ type:"result", rawTime, phaseTime, magnitude, modelTime, modelValue, rmse, period, coefficientCount, milliseconds:performance.now()-started }, [rawTime.buffer, phaseTime.buffer, magnitude.buffer, modelTime.buffer, modelValue.buffer]);
  } catch (error) {
    postMessage({ type:"error", message:error.message || String(error) });
  }
});
