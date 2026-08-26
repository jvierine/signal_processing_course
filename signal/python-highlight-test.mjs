import assert from "node:assert/strict";
import { highlightPython, pythonErrorFeedback } from "./python-highlight.js";

const highlighted = highlightPython(`import numpy as np\n\ndef transform(value=2.5):\n    # keep the phase\n    return np.exp(1j * value) + "<safe>"\n`);
assert.match(highlighted, /python-token-keyword">import<\/span>/);
assert.match(highlighted, /python-token-definition">transform<\/span>/);
assert.match(highlighted, /python-token-number">2\.5<\/span>/);
assert.match(highlighted, /python-token-comment"># keep the phase<\/span>/);
assert.match(highlighted, /python-token-string">"&lt;safe&gt;"<\/span>/);
assert.doesNotMatch(highlighted, /<safe>/);
assert.deepEqual(pythonErrorFeedback('File "<exec>", line 7\n    return +\n            ^\nSyntaxError: invalid syntax'), {
  line: 7,
  message: "SyntaxError on line 7: invalid syntax",
});
console.log("Python syntax highlighting tests passed");
