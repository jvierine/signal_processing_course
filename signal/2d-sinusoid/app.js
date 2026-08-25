const canvas = document.querySelector('#field');
const gl = canvas.getContext('webgl', { antialias: true, alpha: false });

if (!gl) {
  throw new Error('WebGL is not supported by this browser.');
}

const vertexSource = `
  attribute vec2 a_position;
  varying vec2 v_position;
  void main() {
    v_position = a_position;
    gl_Position = vec4(a_position, 0.0, 1.0);
  }
`;

const fragmentSource = `
  precision highp float;
  varying vec2 v_position;
  uniform float u_amplitude;
  uniform float u_phase;
  uniform float u_k;
  uniform float u_l;

  vec3 negativeColor = vec3(0.176, 0.400, 0.533);
  vec3 zeroColor = vec3(1.0, 1.0, 1.0);
  vec3 positiveColor = vec3(0.847, 0.388, 0.271);

  void main() {
    float x = v_position.x * 3.14159265;
    float y = v_position.y * 3.14159265;
    float value = u_amplitude * cos(u_k * x + u_l * y + u_phase);
    float strength = clamp(abs(value) / 2.0, 0.0, 1.0);
    vec3 color = value < 0.0
      ? mix(zeroColor, negativeColor, strength)
      : mix(zeroColor, positiveColor, strength);
    gl_FragColor = vec4(color, 1.0);
  }
`;

function compile(type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(shader));
  return shader;
}

const program = gl.createProgram();
gl.attachShader(program, compile(gl.VERTEX_SHADER, vertexSource));
gl.attachShader(program, compile(gl.FRAGMENT_SHADER, fragmentSource));
gl.linkProgram(program);
if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
gl.useProgram(program);

const position = gl.getAttribLocation(program, 'a_position');
const buffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
gl.enableVertexAttribArray(position);
gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);

const uniforms = {
  amplitude: gl.getUniformLocation(program, 'u_amplitude'),
  phase: gl.getUniformLocation(program, 'u_phase'),
  k: gl.getUniformLocation(program, 'u_k'),
  l: gl.getUniformLocation(program, 'u_l'),
};

const controls = {
  amplitude: document.querySelector('#amplitude'),
  phase: document.querySelector('#phase'),
  k: document.querySelector('#kx'),
  l: document.querySelector('#ly'),
};

const outputs = {
  amplitude: document.querySelector('#amplitude-output'),
  phase: document.querySelector('#phase-output'),
  k: document.querySelector('#kx-output'),
  l: document.querySelector('#ly-output'),
  formula: document.querySelector('#formula-output'),
  min: document.querySelector('#scale-min'),
  max: document.querySelector('#scale-max'),
};

function signed(value, digits = 2) {
  const normalized = Math.abs(value) < 0.5 * 10 ** -digits ? 0 : value;
  return `${normalized >= 0 ? '+' : '−'}${Math.abs(normalized).toFixed(digits)}`;
}

function resize() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const width = Math.max(1, Math.round(canvas.clientWidth * dpr));
  const height = Math.max(1, Math.round(canvas.clientHeight * dpr));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
  gl.viewport(0, 0, width, height);
}

function render() {
  const amplitude = Number(controls.amplitude.value);
  const phase = Number(controls.phase.value);
  const k = Number(controls.k.value);
  const l = Number(controls.l.value);
  const shownPhase = Math.abs(phase) < 0.005 ? 0 : phase;
  const shownL = Math.abs(l) < 0.005 ? 0 : l;
  resize();
  gl.uniform1f(uniforms.amplitude, amplitude);
  gl.uniform1f(uniforms.phase, phase);
  gl.uniform1f(uniforms.k, k);
  gl.uniform1f(uniforms.l, l);
  gl.drawArrays(gl.TRIANGLES, 0, 6);

  outputs.amplitude.value = amplitude.toFixed(2);
  outputs.phase.value = `${signed(phase / Math.PI)}π`;
  outputs.k.value = `${signed(k)} rad/u`;
  outputs.l.value = `${signed(l)} rad/u`;
  outputs.formula.value = `${amplitude.toFixed(2)} cos(${k.toFixed(2)}x ${shownL >= 0 ? '+' : '−'} ${Math.abs(shownL).toFixed(2)}y ${shownPhase >= 0 ? '+' : '−'} ${Math.abs(shownPhase).toFixed(2)})`;
  outputs.min.value = `−${amplitude.toFixed(2)}`;
  outputs.max.value = `+${amplitude.toFixed(2)}`;
}

Object.values(controls).forEach((control) => control.addEventListener('input', render));
window.addEventListener('resize', render);
render();
