const COLORS = {
  ink: [0.094, 0.153, 0.141, 1],
  muted: [0.40, 0.451, 0.435, 1],
  grid: [0.875, 0.89, 0.87, 1],
  teal: [0.039, 0.463, 0.431, 1],
  coral: [0.847, 0.388, 0.271, 1],
  gold: [0.851, 0.635, 0.18, 1],
  softTeal: [0.62, 0.80, 0.76, 1],
};

class LineRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.gl = canvas.getContext('webgl', { antialias: true, alpha: true });
    if (!this.gl) throw new Error('WebGL is not supported by this browser.');

    const vertexSource = `
      attribute vec2 a_position;
      uniform float u_pointSize;
      void main() {
        gl_Position = vec4(a_position, 0.0, 1.0);
        gl_PointSize = u_pointSize;
      }
    `;
    const fragmentSource = `
      precision mediump float;
      uniform vec4 u_color;
      uniform bool u_roundPoint;
      void main() {
        if (u_roundPoint) {
          vec2 p = gl_PointCoord - vec2(0.5);
          if (dot(p, p) > 0.25) discard;
        }
        gl_FragColor = u_color;
      }
    `;

    const gl = this.gl;
    const program = gl.createProgram();
    gl.attachShader(program, this.compile(gl.VERTEX_SHADER, vertexSource));
    gl.attachShader(program, this.compile(gl.FRAGMENT_SHADER, fragmentSource));
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
    this.program = program;
    this.buffer = gl.createBuffer();
    this.positionLocation = gl.getAttribLocation(program, 'a_position');
    this.colorLocation = gl.getUniformLocation(program, 'u_color');
    this.pointSizeLocation = gl.getUniformLocation(program, 'u_pointSize');
    this.roundPointLocation = gl.getUniformLocation(program, 'u_roundPoint');
  }

  compile(type, source) {
    const shader = this.gl.createShader(type);
    this.gl.shaderSource(shader, source);
    this.gl.compileShader(shader);
    if (!this.gl.getShaderParameter(shader, this.gl.COMPILE_STATUS)) throw new Error(this.gl.getShaderInfoLog(shader));
    return shader;
  }

  resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const width = Math.max(1, Math.round(this.canvas.clientWidth * dpr));
    const height = Math.max(1, Math.round(this.canvas.clientHeight * dpr));
    if (this.canvas.width !== width || this.canvas.height !== height) {
      this.canvas.width = width;
      this.canvas.height = height;
    }
    this.gl.viewport(0, 0, width, height);
    return { width, height, dpr };
  }

  clear() {
    this.gl.clearColor(0, 0, 0, 0);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
  }

  draw(vertices, color, mode = this.gl.LINE_STRIP, pointSize = 1) {
    if (!vertices.length) return;
    const gl = this.gl;
    gl.useProgram(this.program);
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.DYNAMIC_DRAW);
    gl.enableVertexAttribArray(this.positionLocation);
    gl.vertexAttribPointer(this.positionLocation, 2, gl.FLOAT, false, 0, 0);
    gl.uniform4fv(this.colorLocation, color);
    gl.uniform1f(this.pointSizeLocation, pointSize);
    gl.uniform1i(this.roundPointLocation, mode === gl.POINTS ? 1 : 0);
    gl.drawArrays(mode, 0, vertices.length / 2);
  }
}

const state = {
  time: 0,
  omega: 2,
  phase: Math.PI / 4,
  amplitude: 1,
  showPeriod: false,
  playing: false,
  lastFrame: 0,
};

const timeSlider = document.querySelector('#time-slider');
const frequencySlider = document.querySelector('#frequency-slider');
const phaseSlider = document.querySelector('#phase-slider');
const amplitudeSlider = document.querySelector('#amplitude-slider');
const showPeriodCheckbox = document.querySelector('#show-period');
const playButton = document.querySelector('#play-button');
const flipFrequencyButton = document.querySelector('#flip-frequency');
const phasorCanvas = document.querySelector('#phasor-canvas');
const signalCanvas = document.querySelector('#signal-canvas');
const phasorRenderer = new LineRenderer(phasorCanvas);
const signalRenderer = new LineRenderer(signalCanvas);

const els = {
  timeOutput: document.querySelector('#time-output'),
  frequencyOutput: document.querySelector('#frequency-output'),
  phaseOutput: document.querySelector('#phase-output'),
  amplitudeOutput: document.querySelector('#amplitude-output'),
  periodOutput: document.querySelector('#period-output'),
  realOutput: document.querySelector('#real-output'),
  imagOutput: document.querySelector('#imag-output'),
  equation: document.querySelector('#live-equation'),
  phasorLabel: document.querySelector('#phasor-label'),
  timeMarkerLabel: document.querySelector('#time-marker-label'),
  periodLabel: document.querySelector('#period-label'),
};

function signed(value, digits = 2) {
  const threshold = 0.5 * 10 ** -digits;
  const normalized = Math.abs(value) < threshold ? 0 : value;
  return `${normalized >= 0 ? '+' : '−'}${Math.abs(normalized).toFixed(digits)}`;
}

function clipX(value, min, max, left = -1, right = 1) {
  return left + ((value - min) / (max - min)) * (right - left);
}

function clipY(value, min, max, bottom = -1, top = 1) {
  return bottom + ((value - min) / (max - min)) * (top - bottom);
}

function line(x1, y1, x2, y2) { return [x1, y1, x2, y2]; }

function drawPhasor() {
  const { width, height } = phasorRenderer.resize();
  phasorRenderer.clear();
  const gl = phasorRenderer.gl;
  const aspect = width / height;
  const sx = aspect < 1 ? 0.82 : 0.82 / aspect;
  const sy = aspect > 1 ? 0.82 : 0.82 * aspect;

  const map = (x, y) => [x * sx, y * sy];
  const grid = [];
  for (const q of [-0.5, 0.5]) {
    grid.push(...map(-1.15, q), ...map(1.15, q));
    grid.push(...map(q, -1.15), ...map(q, 1.15));
  }
  phasorRenderer.draw(grid, COLORS.grid, gl.LINES);
  phasorRenderer.draw([...map(-1.18, 0), ...map(1.18, 0), ...map(0, -1.18), ...map(0, 1.18)], COLORS.muted, gl.LINES);
  phasorRenderer.draw([
    ...map(1.09, 0.045), ...map(1.18, 0),
    ...map(1.09, -0.045), ...map(1.18, 0),
    ...map(-0.045, 1.09), ...map(0, 1.18),
    ...map(0.045, 1.09), ...map(0, 1.18),
  ], COLORS.muted, gl.LINES);

  const radius = state.amplitude / 2;
  const circle = [];
  for (let i = 0; i <= 160; i += 1) {
    const a = i / 160 * Math.PI * 2;
    circle.push(...map(radius * Math.cos(a), radius * Math.sin(a)));
  }
  phasorRenderer.draw(circle, COLORS.softTeal);

  const initial = map(radius * Math.cos(state.phase), radius * Math.sin(state.phase));
  phasorRenderer.draw([0, 0, ...initial], COLORS.gold, gl.LINES);

  const theta = state.omega * state.time + state.phase;
  const x = radius * Math.cos(theta);
  const y = radius * Math.sin(theta);
  const end = map(x, y);
  phasorRenderer.draw([0, 0, ...end], COLORS.teal, gl.LINES);

  const arrowSize = Math.min(0.09, Math.max(0.035, radius * 0.12));
  const left = map(x - arrowSize * Math.cos(theta - 0.55), y - arrowSize * Math.sin(theta - 0.55));
  const right = map(x - arrowSize * Math.cos(theta + 0.55), y - arrowSize * Math.sin(theta + 0.55));
  phasorRenderer.draw([...left, ...end, ...right], COLORS.teal);
  phasorRenderer.draw(initial, COLORS.gold, gl.POINTS, 8 * Math.min(window.devicePixelRatio || 1, 2));
  phasorRenderer.draw(end, COLORS.teal, gl.POINTS, 11 * Math.min(window.devicePixelRatio || 1, 2));

  els.phasorLabel.style.left = `${(end[0] + 1) * 50}%`;
  els.phasorLabel.style.top = `${(1 - end[1]) * 50}%`;
}

function drawSignal() {
  const { dpr } = signalRenderer.resize();
  signalRenderer.clear();
  const gl = signalRenderer.gl;
  const left = -0.88;
  const right = 0.96;
  const bottom = -0.82;
  const top = 0.9;

  const grid = [];
  for (let t = 0; t <= 10; t += 1) {
    const x = clipX(t, 0, 10, left, right);
    grid.push(...line(x, bottom, x, top));
  }
  for (const a of [-2, -1, 1, 2]) {
    const y = clipY(a, -2.4, 2.4, bottom, top);
    grid.push(...line(left, y, right, y));
  }
  signalRenderer.draw(grid, COLORS.grid, gl.LINES);
  const zeroY = clipY(0, -2.4, 2.4, bottom, top);
  signalRenderer.draw([...line(left, zeroY, right, zeroY), ...line(left, bottom, left, top)], COLORS.muted, gl.LINES);
  signalRenderer.draw([
    right - 0.035, zeroY + 0.035, right, zeroY,
    right - 0.035, zeroY - 0.035, right, zeroY,
    left - 0.018, top - 0.055, left, top,
    left + 0.018, top - 0.055, left, top,
  ], COLORS.muted, gl.LINES);

  const real = [];
  const imaginary = [];
  for (let i = 0; i <= 600; i += 1) {
    const t = i / 60;
    const theta = state.omega * t + state.phase;
    const x = clipX(t, 0, 10, left, right);
    real.push(x, clipY(state.amplitude * Math.cos(theta), -2.4, 2.4, bottom, top));
    imaginary.push(x, clipY(state.amplitude * Math.sin(theta), -2.4, 2.4, bottom, top));
  }
  signalRenderer.draw(real, COLORS.teal);
  signalRenderer.draw(imaginary, COLORS.coral);

  const markerX = clipX(state.time, 0, 10, left, right);
  const theta = state.omega * state.time + state.phase;
  const realY = clipY(state.amplitude * Math.cos(theta), -2.4, 2.4, bottom, top);
  const imaginaryY = clipY(state.amplitude * Math.sin(theta), -2.4, 2.4, bottom, top);
  signalRenderer.draw(line(markerX, bottom, markerX, top), COLORS.ink, gl.LINES);
  signalRenderer.draw([markerX, realY], COLORS.teal, gl.POINTS, 10 * dpr);
  signalRenderer.draw([markerX, imaginaryY], COLORS.coral, gl.POINTS, 10 * dpr);

  const markerPercent = (markerX + 1) * 50;
  els.timeMarkerLabel.style.left = `${Math.min(92, Math.max(8, markerPercent))}%`;

  const period = state.omega === 0 ? Infinity : 2 * Math.PI / Math.abs(state.omega);
  const canDrawPeriod = state.showPeriod && Number.isFinite(period) && period <= 10;
  els.periodLabel.hidden = !state.showPeriod;
  if (state.showPeriod) {
    els.periodLabel.textContent = Number.isFinite(period)
      ? `T = ${period.toFixed(2)} s${period > 10 ? ' (outside window)' : ''}`
      : 'No finite period';
    els.periodLabel.style.left = canDrawPeriod ? `${(clipX(period / 2, 0, 10, left, right) + 1) * 50}%` : '50%';
  }
  if (canDrawPeriod) {
    const startX = clipX(0, 0, 10, left, right);
    const endX = clipX(period, 0, 10, left, right);
    const bracketY = top - 0.08;
    signalRenderer.draw([
      ...line(startX, bracketY - 0.04, startX, bracketY + 0.04),
      ...line(startX, bracketY, endX, bracketY),
      ...line(endX, bracketY - 0.04, endX, bracketY + 0.04),
    ], COLORS.gold, gl.LINES);
  }
}

let equationTimer;
function updateEquation() {
  const theta = state.omega * state.time + state.phase;
  els.equation.innerHTML = `\\(A=${state.amplitude.toFixed(2)},\\quad \\theta=${signed(state.omega)}(${state.time.toFixed(2)})${signed(state.phase)}=${signed(theta)}\\text{ rad}\\)`;
  clearTimeout(equationTimer);
  equationTimer = setTimeout(() => {
    if (window.MathJax?.typesetPromise) window.MathJax.typesetPromise([els.equation]).catch(() => {});
  }, 50);
}

function updateUI(includeEquation = true) {
  const theta = state.omega * state.time + state.phase;
  const real = state.amplitude * Math.cos(theta);
  const imaginary = state.amplitude * Math.sin(theta);
  els.timeOutput.value = `${state.time.toFixed(2)} s`;
  els.frequencyOutput.value = `${signed(state.omega)} rad/s`;
  els.phaseOutput.value = `${signed(state.phase / Math.PI)}π rad`;
  els.amplitudeOutput.value = state.amplitude.toFixed(2);
  const period = state.omega === 0 ? Infinity : 2 * Math.PI / Math.abs(state.omega);
  els.periodOutput.value = Number.isFinite(period) ? `T = ${period.toFixed(2)} s` : 'No finite T';
  els.periodOutput.hidden = !state.showPeriod;
  els.realOutput.textContent = signed(real, 3);
  els.imagOutput.textContent = signed(imaginary, 3);
  els.timeMarkerLabel.textContent = `t = ${state.time.toFixed(2)} s`;

  drawPhasor();
  drawSignal();
  if (includeEquation) updateEquation();
}

function setPlaying(playing) {
  state.playing = playing;
  playButton.setAttribute('aria-pressed', String(playing));
  playButton.setAttribute('aria-label', playing ? 'Pause animation' : 'Play animation');
  if (playing) {
    state.lastFrame = performance.now();
    requestAnimationFrame(animate);
  }
}

function animate(now) {
  if (!state.playing) return;
  const delta = Math.min((now - state.lastFrame) / 1000, 0.1);
  state.lastFrame = now;
  state.time += delta;
  if (state.time > 10) state.time %= 10;
  timeSlider.value = String(state.time);
  updateUI(false);
  requestAnimationFrame(animate);
}

playButton.addEventListener('click', () => setPlaying(!state.playing));
flipFrequencyButton.addEventListener('click', (event) => {
  event.preventDefault();
  event.stopPropagation();
  state.omega = state.omega === 0 ? -2 : -state.omega;
  frequencySlider.value = String(state.omega);
  updateUI();
});
timeSlider.addEventListener('input', (event) => {
  state.time = Number(event.target.value);
  updateUI();
});
frequencySlider.addEventListener('input', (event) => {
  state.omega = Number(event.target.value);
  updateUI();
});
phaseSlider.addEventListener('input', (event) => {
  state.phase = Number(event.target.value);
  updateUI();
});
amplitudeSlider.addEventListener('input', (event) => {
  state.amplitude = Number(event.target.value);
  updateUI();
});
showPeriodCheckbox.addEventListener('change', (event) => {
  state.showPeriod = event.target.checked;
  updateUI(false);
});
window.addEventListener('resize', () => updateUI(false));
window.addEventListener('load', updateEquation);
document.addEventListener('visibilitychange', () => {
  if (document.hidden && state.playing) setPlaying(false);
});

updateUI();
