const ANIMATION_NS_PER_SECOND = 0.2;
const LIGHT_SPEED = 299792458;
const TIME_WINDOW_NS = 1;
const SPACE_WINDOW_M = 0.25;
const DEFAULT_OMEGA = 2 * Math.PI * 2.4;
const DEFAULT_K = DEFAULT_OMEGA * 1e9 / LIGHT_SPEED;

const COLORS = {
  ink: [0.094, 0.153, 0.141, 1],
  muted: [0.40, 0.451, 0.435, 1],
  grid: [0.91, 0.92, 0.90, 1],
  blue: [0.0, 0.447, 0.698, 1],
};

class LineRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.gl = canvas.getContext('webgl', { antialias: true, alpha: true, preserveDrawingBuffer: true });
    if (!this.gl) throw new Error('WebGL is not supported by this browser.');
    const vertex = `
      attribute vec2 a_position;
      void main() { gl_Position = vec4(a_position, 0.0, 1.0); }
    `;
    const fragment = `
      precision mediump float;
      uniform vec4 u_color;
      void main() { gl_FragColor = u_color; }
    `;
    const gl = this.gl;
    this.program = gl.createProgram();
    gl.attachShader(this.program, this.compile(gl.VERTEX_SHADER, vertex));
    gl.attachShader(this.program, this.compile(gl.FRAGMENT_SHADER, fragment));
    gl.linkProgram(this.program);
    if (!gl.getProgramParameter(this.program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(this.program));
    this.buffer = gl.createBuffer();
    this.position = gl.getAttribLocation(this.program, 'a_position');
    this.color = gl.getUniformLocation(this.program, 'u_color');
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
    return dpr;
  }

  clear() {
    this.gl.clearColor(1, 1, 1, 1);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
  }

  draw(vertices, color, mode = this.gl.LINE_STRIP, thickness = 1) {
    if (!vertices.length) return;
    const gl = this.gl;
    gl.useProgram(this.program);
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer);
    gl.enableVertexAttribArray(this.position);
    gl.vertexAttribPointer(this.position, 2, gl.FLOAT, false, 0, 0);
    gl.uniform4fv(this.color, color);
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const radius = thickness > 1 ? Math.max(1, Math.round((thickness * dpr - 1) / 2)) : 0;
    const offsets = radius ? [[0, 0], [-radius, 0], [radius, 0], [0, -radius], [0, radius], [-radius, -radius], [radius, -radius], [-radius, radius], [radius, radius]] : [[0, 0]];
    for (const [dx, dy] of offsets) {
      const shifted = (dx || dy) ? vertices.map((v, i) => v + (i % 2 === 0 ? 2 * dx / this.canvas.width : 2 * dy / this.canvas.height)) : vertices;
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(shifted), gl.DYNAMIC_DRAW);
      gl.drawArrays(mode, 0, vertices.length / 2);
    }
  }
}

class FieldRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.gl = canvas.getContext('webgl', { antialias: true, alpha: false, preserveDrawingBuffer: true });
    if (!this.gl) throw new Error('WebGL is not supported by this browser.');
    const vertex = `
      attribute vec2 a_position;
      varying vec2 v_position;
      void main() { v_position = a_position; gl_Position = vec4(a_position, 0.0, 1.0); }
    `;
    const fragment = `
      precision highp float;
      varying vec2 v_position;
      uniform float u_omega;
      uniform float u_k;
      vec3 negativeColor = vec3(0.0, 0.447, 0.698);
      vec3 zeroColor = vec3(1.0, 1.0, 1.0);
      vec3 positiveColor = vec3(0.835, 0.369, 0.0);
      void main() {
        float timeNs = (v_position.x + 1.0) * 0.5;
        float spaceM = (v_position.y + 1.0) * 0.125;
        float value = cos(u_omega * timeNs - u_k * spaceM);
        vec3 color = value < 0.0 ? mix(zeroColor, negativeColor, abs(value)) : mix(zeroColor, positiveColor, abs(value));
        gl_FragColor = vec4(color, 1.0);
      }
    `;
    const gl = this.gl;
    const compile = (type, source) => {
      const shader = gl.createShader(type);
      gl.shaderSource(shader, source);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(shader));
      return shader;
    };
    this.program = gl.createProgram();
    gl.attachShader(this.program, compile(gl.VERTEX_SHADER, vertex));
    gl.attachShader(this.program, compile(gl.FRAGMENT_SHADER, fragment));
    gl.linkProgram(this.program);
    if (!gl.getProgramParameter(this.program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(this.program));
    gl.useProgram(this.program);
    const position = gl.getAttribLocation(this.program, 'a_position');
    const buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(position);
    gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);
    this.omega = gl.getUniformLocation(this.program, 'u_omega');
    this.k = gl.getUniformLocation(this.program, 'u_k');
  }

  render(omega, k) {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const width = Math.max(1, Math.round(this.canvas.clientWidth * dpr));
    const height = Math.max(1, Math.round(this.canvas.clientHeight * dpr));
    if (this.canvas.width !== width || this.canvas.height !== height) {
      this.canvas.width = width;
      this.canvas.height = height;
    }
    this.gl.viewport(0, 0, width, height);
    this.gl.useProgram(this.program);
    this.gl.uniform1f(this.omega, omega);
    this.gl.uniform1f(this.k, k);
    this.gl.drawArrays(this.gl.TRIANGLES, 0, 6);
  }
}

const state = { timeNs: 0, omega: DEFAULT_OMEGA, k: DEFAULT_K, lockDispersion: true, playing: false, lastFrame: 0 };
const fieldRenderer = new FieldRenderer(document.querySelector('#field-canvas'));
const sliceRenderer = new LineRenderer(document.querySelector('#slice-canvas'));
const timeSlider = document.querySelector('#time-slider');
const omegaSlider = document.querySelector('#omega-slider');
const kSlider = document.querySelector('#k-slider');
const lockDispersion = document.querySelector('#lock-dispersion');
const playButton = document.querySelector('#play-button');
const els = {
  time: document.querySelector('#time-output'),
  omega: document.querySelector('#omega-output'),
  k: document.querySelector('#k-output'),
  status: document.querySelector('#wave-status'),
  values: document.querySelector('#wave-values'),
  marker: document.querySelector('#current-time-line'),
  markerLabel: document.querySelector('#current-time-label'),
  sliceTime: document.querySelector('#slice-time'),
};

function mapX(value, min, max, left, right) { return left + (value - min) / (max - min) * (right - left); }
function mapY(value, min, max, bottom, top) { return bottom + (value - min) / (max - min) * (top - bottom); }
function segment(x1, y1, x2, y2) { return [x1, y1, x2, y2]; }

function drawSlice() {
  sliceRenderer.resize();
  sliceRenderer.clear();
  const gl = sliceRenderer.gl;
  const left = -0.86;
  const right = 0.95;
  const bottom = -0.80;
  const top = 0.88;
  const grid = [];
  for (const x of [0, 0.0625, 0.125, 0.1875, 0.25]) {
    const px = mapX(x, 0, SPACE_WINDOW_M, left, right);
    grid.push(...segment(px, bottom, px, top));
  }
  for (const y of [-1, -0.5, 0.5, 1]) {
    const py = mapY(y, -1.2, 1.2, bottom, top);
    grid.push(...segment(left, py, right, py));
  }
  sliceRenderer.draw(grid, COLORS.grid, gl.LINES);
  const zeroY = mapY(0, -1.2, 1.2, bottom, top);
  sliceRenderer.draw([...segment(left, zeroY, right, zeroY), ...segment(left, bottom, left, top)], COLORS.muted, gl.LINES);
  sliceRenderer.draw([
    right - 0.035, zeroY + 0.035, right, zeroY,
    right - 0.035, zeroY - 0.035, right, zeroY,
    left - 0.018, top - 0.055, left, top,
    left + 0.018, top - 0.055, left, top,
  ], COLORS.muted, gl.LINES);

  const curve = [];
  for (let i = 0; i <= 600; i += 1) {
    const xMeters = SPACE_WINDOW_M * i / 600;
    const field = Math.cos(state.omega * state.timeNs - state.k * xMeters);
    curve.push(mapX(xMeters, 0, SPACE_WINDOW_M, left, right), mapY(field, -1.2, 1.2, bottom, top));
  }
  sliceRenderer.draw(curve, COLORS.blue, gl.LINE_STRIP, 3);
}

function signed(value, digits = 2) {
  const normalized = Math.abs(value) < 0.5 * 10 ** -digits ? 0 : value;
  return `${normalized >= 0 ? '+' : '−'}${Math.abs(normalized).toFixed(digits)}`;
}

function render() {
  fieldRenderer.render(state.omega, state.k);
  drawSlice();
  const percent = 7 + 89 * state.timeNs / TIME_WINDOW_NS;
  const frequencyGHz = state.omega / (2 * Math.PI);
  const wavelengthCm = state.k === 0 ? Infinity : 200 * Math.PI / Math.abs(state.k);
  const dispersionError = Math.abs(Math.abs(state.k) - Math.abs(state.omega) * 1e9 / LIGHT_SPEED);
  const onDispersion = dispersionError < 0.15;
  const direction = state.omega === 0 || state.k === 0 ? 'none' : state.omega / state.k > 0 ? '+x' : '−x';
  els.time.value = `${state.timeNs.toFixed(3)} ns`;
  els.omega.value = `${signed(state.omega)} rad/ns`;
  els.k.value = `${signed(state.k)} rad/m`;
  els.status.value = onDispersion ? `Propagation: ${direction}` : 'Off Maxwell dispersion';
  els.status.classList.toggle('is-invalid', !onDispersion);
  els.values.value = `f = ${frequencyGHz.toFixed(2)} GHz · λ = ${Number.isFinite(wavelengthCm) ? `${wavelengthCm.toFixed(2)} cm` : '∞'}`;
  els.marker.style.left = `${percent}%`;
  els.markerLabel.style.left = `${Math.min(90, Math.max(12, percent))}%`;
  els.markerLabel.textContent = `${state.timeNs.toFixed(3)} ns`;
  els.sliceTime.value = `t = ${state.timeNs.toFixed(3)} ns`;
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
  state.timeNs = (state.timeNs + delta * ANIMATION_NS_PER_SECOND) % TIME_WINDOW_NS;
  timeSlider.value = String(state.timeNs);
  render();
  requestAnimationFrame(animate);
}

playButton.addEventListener('click', () => setPlaying(!state.playing));
timeSlider.addEventListener('input', (event) => {
  state.timeNs = Number(event.target.value);
  render();
});
omegaSlider.addEventListener('input', (event) => {
  state.omega = Number(event.target.value);
  if (state.lockDispersion) {
    const direction = state.k < 0 ? -1 : 1;
    state.k = direction * Math.abs(state.omega) * 1e9 / LIGHT_SPEED;
    kSlider.value = String(state.k);
  }
  render();
});
kSlider.addEventListener('input', (event) => {
  state.k = Number(event.target.value);
  if (state.lockDispersion) {
    const omegaSign = state.omega < 0 ? -1 : 1;
    state.omega = omegaSign * Math.abs(state.k) * LIGHT_SPEED / 1e9;
    omegaSlider.value = String(state.omega);
  }
  render();
});
lockDispersion.addEventListener('change', (event) => {
  state.lockDispersion = event.target.checked;
  if (state.lockDispersion) {
    const direction = state.k < 0 ? -1 : 1;
    state.k = direction * Math.abs(state.omega) * 1e9 / LIGHT_SPEED;
    kSlider.value = String(state.k);
  }
  render();
});
window.addEventListener('resize', render);
document.addEventListener('visibilitychange', () => {
  if (document.hidden && state.playing) setPlaying(false);
});

render();
