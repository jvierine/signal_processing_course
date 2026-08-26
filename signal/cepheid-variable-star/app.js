const STARTER_CODE = `import numpy as np

# Irregular brightness measurements of a real Cepheid star.
d = np.loadtxt("/tmp/lcb1.dat")
good = np.where(np.abs(d[:, 2]) < 1.0)[0]
m_t = d[good, 0]
m_mag = d[good, 1]

# Fold all observations into one fundamental period.
T = 13.124349
m_modulo_t = np.mod(m_t, T)

# Estimate 21 Fourier-series coefficients from the data.
N = 10
k_idx = np.arange(-N, N + 1)
A = np.zeros((len(m_mag), len(k_idx)), dtype=complex)
for ki, k in enumerate(k_idx):
    A[:, ki] = np.exp(1j * (2 * np.pi / T) * k * m_modulo_t)

S = np.linalg.inv(A.conj().T @ A)
c_k = S @ A.conj().T @ m_mag

# Evaluate the Fourier-series model over one period.
model_t = np.linspace(0, T, 400)
model = np.zeros(len(model_t), dtype=complex)
for ki, k in enumerate(k_idx):
    # TODO: replace 0.0 with the kth Fourier-series component.
    model += 0.0

# Values returned to the browser plots and task checker.
prediction = np.interp(m_modulo_t, model_t, model.real)
fit_rmse = float(np.sqrt(np.mean((prediction - m_mag) ** 2)))
coefficient_count = len(c_k)
raw_time_bytes = np.asarray(m_t, dtype=np.float32).tobytes()
phase_time_bytes = np.asarray(m_modulo_t, dtype=np.float32).tobytes()
magnitude_bytes = np.asarray(m_mag, dtype=np.float32).tobytes()
model_time_bytes = np.asarray(model_t, dtype=np.float32).tobytes()
model_value_bytes = np.asarray(model.real, dtype=np.float32).tobytes()`;

const els = {
  code:document.querySelector("#python-code"), run:document.querySelector("#run-button"), reset:document.querySelector("#reset-button"), stop:document.querySelector("#stop-button"), status:document.querySelector("#runtime-status"), raw:document.querySelector("#raw-canvas"), model:document.querySelector("#model-canvas"), period:document.querySelector("#period-value"), coefficients:document.querySelector("#coefficient-value"), rmse:document.querySelector("#rmse-value"), runTime:document.querySelector("#run-time")
};
const COLORS = { ink:"#182724", muted:"#66736f", grid:"#e8e9e4", blue:"#0072b2", orange:"#d55e00" };
let worker;
let ready = false;
let running = false;
let latestResult;

function floatArray(bytes) { return new Float32Array(bytes.buffer, bytes.byteOffset, bytes.byteLength / 4); }
function setStatus(text, kind="") { els.status.value=text; els.status.className=kind; }
function setRunning(value) { running=value; els.run.disabled=value || !ready; els.stop.disabled=!value; els.run.textContent=value ? "Running…" : "Run code"; }

function drawPlot(canvas, x, y, options={}) {
  const dpr=Math.min(devicePixelRatio || 1,2); const width=Math.max(1,Math.round(canvas.clientWidth*dpr)); const height=Math.max(1,Math.round(canvas.clientHeight*dpr));
  canvas.width=width; canvas.height=height; const ctx=canvas.getContext("2d"); ctx.scale(dpr,dpr);
  const w=width/dpr,h=height/dpr,left=42,right=10,top=10,bottom=27;
  const xMin=options.xMin ?? Math.min(...x), xMax=options.xMax ?? Math.max(...x); const allY=options.lineY ? [...y,...options.lineY] : y; const yMin=options.yMin ?? Math.min(...allY), yMax=options.yMax ?? Math.max(...allY);
  const px=v=>left+(v-xMin)/(xMax-xMin)*(w-left-right); const py=v=>top+(yMax-v)/(yMax-yMin)*(h-top-bottom);
  ctx.fillStyle="#fff"; ctx.fillRect(0,0,w,h); ctx.strokeStyle=COLORS.grid; ctx.lineWidth=1;
  ctx.font="10px system-ui"; ctx.fillStyle=COLORS.muted; ctx.textAlign="center"; ctx.textBaseline="top";
  for(let i=0;i<=4;i++){const xv=xMin+(xMax-xMin)*i/4;const xp=px(xv);ctx.beginPath();ctx.moveTo(xp,top);ctx.lineTo(xp,h-bottom);ctx.stroke();ctx.fillText(xv.toFixed(options.xDigits ?? 0),xp,h-bottom+5);}
  ctx.textAlign="right";ctx.textBaseline="middle";
  for(let i=0;i<=4;i++){const yv=yMin+(yMax-yMin)*i/4;const yp=py(yv);ctx.beginPath();ctx.moveTo(left,yp);ctx.lineTo(w-right,yp);ctx.stroke();ctx.fillText(yv.toFixed(2),left-5,yp);}
  ctx.strokeStyle=COLORS.ink;ctx.lineWidth=1.4;ctx.beginPath();ctx.moveTo(left,h-bottom);ctx.lineTo(w-right,h-bottom);ctx.moveTo(w-right-6,h-bottom-4);ctx.lineTo(w-right,h-bottom);ctx.lineTo(w-right-6,h-bottom+4);ctx.moveTo(left,h-bottom);ctx.lineTo(left,top);ctx.moveTo(left-4,top+6);ctx.lineTo(left,top);ctx.lineTo(left+4,top+6);ctx.stroke();
  if(options.lineX){ctx.strokeStyle=COLORS.blue;ctx.lineWidth=2.5;ctx.beginPath();options.lineX.forEach((v,i)=>{const xp=px(v),yp=py(options.lineY[i]);i?ctx.lineTo(xp,yp):ctx.moveTo(xp,yp);});ctx.stroke();}
  ctx.fillStyle=COLORS.orange; for(let i=0;i<x.length;i++){ctx.beginPath();ctx.arc(px(x[i]),py(y[i]),2.5,0,2*Math.PI);ctx.fill();}
  ctx.fillStyle=COLORS.ink;ctx.font="italic 10px Georgia";ctx.textAlign="right";ctx.textBaseline="bottom";ctx.fillText(options.xLabel || "Time (days)",w-right,h-2);ctx.save();ctx.translate(11,top);ctx.rotate(-Math.PI/2);ctx.textAlign="right";ctx.fillText("Relative magnitude",0,0);ctx.restore();
}

function render(result){latestResult=result;const raw=floatArray(result.rawTime),phase=floatArray(result.phaseTime),mag=floatArray(result.magnitude),modelT=floatArray(result.modelTime),modelV=floatArray(result.modelValue);drawPlot(els.raw,raw,mag,{xDigits:0,xLabel:"Observation time (days)"});drawPlot(els.model,phase,mag,{xMin:0,xMax:result.period,xDigits:1,xLabel:"Phase time (days)",lineX:modelT,lineY:modelV,yMin:-.35,yMax:.6});els.period.textContent=`${result.period.toFixed(3)} days`;els.coefficients.textContent=String(result.coefficientCount);els.rmse.textContent=result.rmse.toFixed(3);els.runTime.textContent=`Python ${result.milliseconds.toFixed(0)} ms`;setStatus(result.rmse<.05?"Task complete · the Fourier model matches the data":"Complete the TODO line and run again",result.rmse<.05?"is-success":"");}

function startWorker(){ready=false;setRunning(false);setStatus("Starting local Python WebAssembly…");worker=new Worker("./worker.js?v=20260826-1",{type:"module"});worker.addEventListener("message",event=>{if(event.data.type==="ready"){ready=true;setRunning(false);setStatus(`Python ready · ${(event.data.milliseconds/1000).toFixed(1)} s initial load`);runCode();return;}if(event.data.type==="result"){render(event.data);setRunning(false);return;}if(event.data.type==="error"){setStatus(event.data.message,"is-error");setRunning(false);}});worker.addEventListener("error",event=>{setStatus(event.message || "Python worker failed to start","is-error");setRunning(false);});}
function runCode(){if(!ready || running)return;setRunning(true);setStatus("Running Fourier-series fit…");worker.postMessage({type:"run",code:els.code.value});}
els.code.value=STARTER_CODE;els.run.addEventListener("click",runCode);els.reset.addEventListener("click",()=>{els.code.value=STARTER_CODE;runCode();});els.stop.addEventListener("click",()=>{worker.terminate();setStatus("Python stopped · restarting…");startWorker();});window.addEventListener("resize",()=>{if(latestResult)render(latestResult);});startWorker();
