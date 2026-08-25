const COLORS = {
  ink: [0.094, 0.153, 0.141, 1],
  muted: [0.40, 0.451, 0.435, 1],
  grid: [0.875, 0.89, 0.87, 1],
  teal: [0.0, 0.447, 0.698, 1],
  coral: [0.835, 0.369, 0.0, 1],
  gold: [0.902, 0.624, 0.0, 1],
  softTeal: [0.65, 0.82, 0.91, 1],
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

  draw(vertices, color, mode = this.gl.LINE_STRIP, pointSize = 1, thickness = 1) {
    if (!vertices.length) return;
    const gl = this.gl;
    gl.useProgram(this.program);
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer);
    gl.enableVertexAttribArray(this.positionLocation);
    gl.vertexAttribPointer(this.positionLocation, 2, gl.FLOAT, false, 0, 0);
    gl.uniform4fv(this.colorLocation, color);
    gl.uniform1f(this.pointSizeLocation, pointSize);
    gl.uniform1i(this.roundPointLocation, mode === gl.POINTS ? 1 : 0);

    const isLine = mode === gl.LINE_STRIP || mode === gl.LINES;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const radius = isLine && thickness > 1 ? Math.max(1, Math.round((thickness * dpr - 1) / 2)) : 0;
    const offsets = radius
      ? [[0, 0], [-radius, 0], [radius, 0], [0, -radius], [0, radius], [-radius, -radius], [radius, -radius], [-radius, radius], [radius, radius]]
      : [[0, 0]];

    for (const [dx, dy] of offsets) {
      const shifted = (dx || dy)
        ? vertices.map((value, index) => value + (index % 2 === 0 ? 2 * dx / this.canvas.width : 2 * dy / this.canvas.height))
        : vertices;
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(shifted), gl.DYNAMIC_DRAW);
      gl.drawArrays(mode, 0, vertices.length / 2);
    }
  }
}

const state = {
  time: 0,
  omega: 2,
  phase: Math.PI / 4,
  amplitude: 1,
  showPeriod: false,
  view: 'complex',
  playing: false,
  lastFrame: 0,
};

const timeSlider = document.querySelector('#time-slider');
const frequencySlider = document.querySelector('#frequency-slider');
const phaseSlider = document.querySelector('#phase-slider');
const amplitudeSlider = document.querySelector('#amplitude-slider');
const showPeriodCheckbox = document.querySelector('#show-period');
const viewControls = document.querySelectorAll('input[name="phasor-view"]');
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
  mainEquation: document.querySelector('#main-equation'),
  phasorLabel: document.querySelector('#phasor-label'),
  conjugateLabel: document.querySelector('#conjugate-label'),
  resultLabel: document.querySelector('#result-label'),
  phasorHeading: document.querySelector('#phasor-heading'),
  primaryLegend: document.querySelector('#primary-legend'),
  secondaryLegend: document.querySelector('#secondary-legend'),
  cancellationNote: document.querySelector('#cancellation-note'),
  phasorTimeLabel: document.querySelector('#phasor-time-label'),
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

function positionLabel(element, point, offset = 'translate(8px, -22px)') {
  element.style.left = `${(point[0] + 1) * 50}%`;
  element.style.top = `${(1 - point[1]) * 50}%`;
  element.style.transform = offset;
}

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
  phasorRenderer.draw(circle, COLORS.softTeal, gl.LINE_STRIP, 1, 2);

  const theta = state.omega * state.time + state.phase;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);

  const drawArrow = (x, y, angle, color, thickness = 3) => {
    const end = map(x, y);
    const arrowSize = Math.min(0.09, Math.max(0.035, Math.hypot(x, y) * 0.12));
    const left = map(x - arrowSize * Math.cos(angle - 0.55), y - arrowSize * Math.sin(angle - 0.55));
    const right = map(x - arrowSize * Math.cos(angle + 0.55), y - arrowSize * Math.sin(angle + 0.55));
    phasorRenderer.draw([0, 0, ...end], color, gl.LINES, 1, thickness);
    phasorRenderer.draw([...left, ...end, ...right], color, gl.LINE_STRIP, 1, thickness);
    phasorRenderer.draw(end, color, gl.POINTS, 10 * dpr);
    return end;
  };

  if (state.view === 'complex') {
    const initial = map(radius * Math.cos(state.phase), radius * Math.sin(state.phase));
    phasorRenderer.draw([0, 0, ...initial], COLORS.gold, gl.LINES, 1, 2);
    const end = drawArrow(radius * Math.cos(theta), radius * Math.sin(theta), theta, COLORS.teal);
    phasorRenderer.draw(initial, COLORS.gold, gl.POINTS, 8 * dpr);
    positionLabel(els.phasorLabel, end);
    return;
  }

  const halfRadius = radius / 2;
  const first = {
    x: halfRadius * Math.cos(theta),
    y: halfRadius * Math.sin(theta),
    angle: theta,
  };
  const secondAngle = state.view === 'real' ? -theta : Math.PI - theta;
  const second = {
    x: halfRadius * Math.cos(secondAngle),
    y: halfRadius * Math.sin(secondAngle),
    angle: secondAngle,
  };
  const firstEnd = drawArrow(first.x, first.y, first.angle, COLORS.teal);
  const secondEnd = drawArrow(second.x, second.y, second.angle, COLORS.coral);
  const sum = { x: first.x + second.x, y: first.y + second.y };
  const sumAngle = Math.atan2(sum.y, sum.x);
  const sumEnd = drawArrow(sum.x, sum.y, sumAngle, COLORS.gold, 4);

  // Complete the vector parallelogram so the cancellation is visible geometrically.
  phasorRenderer.draw([
    ...firstEnd, ...sumEnd,
    ...secondEnd, ...sumEnd,
  ], COLORS.muted, gl.LINES, 1, 1);

  positionLabel(els.phasorLabel, firstEnd);
  positionLabel(els.conjugateLabel, secondEnd, 'translate(8px, 5px)');
  positionLabel(els.resultLabel, sumEnd, 'translate(8px, -22px)');
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
  signalRenderer.draw(real, COLORS.teal, gl.LINE_STRIP, 1, 3);
  signalRenderer.draw(imaginary, COLORS.coral, gl.LINE_STRIP, 1, 3);

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
    ], COLORS.gold, gl.LINES, 1, 2);
  }
}

let equationTimer;
function updateEquation() {
  const theta = state.omega * state.time + state.phase;
  const real = state.amplitude * Math.cos(theta);
  const imaginary = state.amplitude * Math.sin(theta);
  if (state.view === 'real') {
    els.mainEquation.innerHTML = '\\[\\operatorname{Re}\\{z(t)\\}=\\tfrac12\\left[Xe^{i\\omega t}+X^*e^{-i\\omega t}\\right]=A\\cos(\\omega t+\\phi)\\]';
    els.equation.innerHTML = `\\(\\tfrac12(z+z^*)=(${signed(real)},+0.00i)\\)`;
  } else if (state.view === 'imaginary') {
    els.mainEquation.innerHTML = '\\[\\operatorname{Im}\\{z(t)\\}=\\tfrac1{2i}\\left[Xe^{i\\omega t}-X^*e^{-i\\omega t}\\right]=A\\sin(\\omega t+\\phi)\\]';
    els.equation.innerHTML = `\\(\\tfrac12(z-z^*)=(+0.00,${signed(imaginary)}i)=i\\operatorname{Im}\\{z\\}\\)`;
  } else {
    els.mainEquation.innerHTML = '\\[X=Ae^{i\\phi},\\qquad z(t)=Xe^{i\\omega t}=A e^{i(\\omega t+\\phi)}\\]';
    els.equation.innerHTML = `\\(A=${state.amplitude.toFixed(2)},\\quad \\theta=${signed(state.omega)}(${state.time.toFixed(2)})${signed(state.phase)}=${signed(theta)}\\text{ rad}\\)`;
  }
  clearTimeout(equationTimer);
  equationTimer = setTimeout(() => {
    if (window.MathJax?.typesetPromise) window.MathJax.typesetPromise([els.mainEquation, els.equation]).catch(() => {});
  }, 50);
}

function updateViewLabels(real, imaginary) {
  const isComplex = state.view === 'complex';
  els.conjugateLabel.hidden = isComplex;
  els.resultLabel.hidden = isComplex;
  els.cancellationNote.hidden = isComplex;

  if (isComplex) {
    els.phasorHeading.textContent = 'Phasor position';
    els.phasorLabel.textContent = 'Xeⁱᵠᵗ';
    els.primaryLegend.innerHTML = '<i class="legend-dot current-dot"></i>Current phasor';
    els.secondaryLegend.innerHTML = '<i class="legend-line start-line"></i>Initial phase φ';
    return;
  }

  els.phasorLabel.textContent = '½ Xeⁱᵠᵗ';
  els.primaryLegend.innerHTML = '<i class="legend-line real-line"></i>½ Xeⁱᵠᵗ';
  if (state.view === 'real') {
    els.phasorHeading.textContent = 'Real part from conjugates';
    els.conjugateLabel.textContent = '½ X*e⁻ⁱᵠᵗ';
    els.resultLabel.textContent = 'Re{z}';
    els.secondaryLegend.innerHTML = '<i class="legend-line imaginary-line"></i>½ X*e⁻ⁱᵠᵗ';
    els.cancellationNote.textContent = `Im cancels: ${signed(imaginary / 2, 3)} ${signed(-imaginary / 2, 3)} = 0`;
  } else {
    els.phasorHeading.textContent = 'Imaginary part from conjugates';
    els.conjugateLabel.textContent = '−½ X*e⁻ⁱᵠᵗ';
    els.resultLabel.textContent = 'i Im{z}';
    els.secondaryLegend.innerHTML = '<i class="legend-line imaginary-line"></i>−½ X*e⁻ⁱᵠᵗ';
    els.cancellationNote.textContent = `Re cancels: ${signed(real / 2, 3)} ${signed(-real / 2, 3)} = 0`;
  }
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
  els.phasorTimeLabel.textContent = `t = ${state.time.toFixed(1)} s`;
  updateViewLabels(real, imaginary);

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
viewControls.forEach((control) => control.addEventListener('change', (event) => {
  state.view = event.target.value;
  updateUI();
}));
window.addEventListener('resize', () => updateUI(false));
window.addEventListener('load', updateEquation);
document.addEventListener('visibilitychange', () => {
  if (document.hidden && state.playing) setPlaying(false);
});

updateUI();
