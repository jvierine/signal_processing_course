const KEYWORDS = new Set([
  "and", "as", "assert", "async", "await", "break", "case", "class", "continue",
  "def", "del", "elif", "else", "except", "False", "finally", "for", "from",
  "global", "if", "import", "in", "is", "lambda", "match", "None", "nonlocal",
  "not", "or", "pass", "raise", "return", "True", "try", "while", "with", "yield",
]);

const BUILTINS = new Set([
  "abs", "all", "any", "bool", "bytes", "complex", "dict", "enumerate", "filter",
  "float", "int", "len", "list", "map", "max", "min", "open", "print", "range",
  "reversed", "round", "set", "slice", "sorted", "str", "sum", "tuple", "type", "zip",
]);

function escapeHtml(value) {
  return value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}

function token(kind, value) {
  return `<span class="python-token-${kind}">${escapeHtml(value)}</span>`;
}

function isIdentifierStart(character) {
  return Boolean(character && /[A-Za-z_]/.test(character));
}

function isIdentifierPart(character) {
  return Boolean(character && /[A-Za-z0-9_]/.test(character));
}

export function highlightPython(source) {
  let highlighted = "";
  let index = 0;
  let previousWord = "";

  while (index < source.length) {
    const character = source[index];

    if (/\s/.test(character)) {
      const start = index++;
      while (index < source.length && /\s/.test(source[index])) index++;
      highlighted += escapeHtml(source.slice(start, index));
      continue;
    }

    if (character === "#") {
      const end = source.indexOf("\n", index);
      const next = end === -1 ? source.length : end;
      highlighted += token("comment", source.slice(index, next));
      index = next;
      continue;
    }

    let prefixLength = 0;
    if ((index === 0 || !isIdentifierPart(source[index - 1])) && isIdentifierStart(character)) {
      const prefix = source.slice(index).match(/^[rRuUbBfF]{1,2}(?=['"])/)?.[0] ?? "";
      prefixLength = prefix.length;
    }
    const quoteIndex = index + prefixLength;
    const quote = source[quoteIndex];
    if (quote === "'" || quote === '"') {
      const start = index;
      const triple = source.slice(quoteIndex, quoteIndex + 3) === quote.repeat(3);
      index = quoteIndex + (triple ? 3 : 1);
      while (index < source.length) {
        if (source[index] === "\\") {
          index = Math.min(source.length, index + 2);
          continue;
        }
        if (triple ? source.slice(index, index + 3) === quote.repeat(3) : source[index] === quote) {
          index += triple ? 3 : 1;
          break;
        }
        if (!triple && source[index] === "\n") break;
        index++;
      }
      highlighted += token("string", source.slice(start, index));
      previousWord = "";
      continue;
    }

    const number = source.slice(index).match(/^(?:0[xX][0-9a-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+|(?:\d[\d_]*(?:\.\d[\d_]*)?|\.\d[\d_]*)(?:[eE][+-]?\d[\d_]*)?[jJ]?)/)?.[0];
    if (number) {
      highlighted += token("number", number);
      index += number.length;
      previousWord = "";
      continue;
    }

    if (isIdentifierStart(character)) {
      const start = index++;
      while (index < source.length && isIdentifierPart(source[index])) index++;
      const word = source.slice(start, index);
      const kind = KEYWORDS.has(word)
        ? "keyword"
        : previousWord === "def" || previousWord === "class"
          ? "definition"
          : BUILTINS.has(word)
            ? "builtin"
            : "name";
      highlighted += kind === "name" ? escapeHtml(word) : token(kind, word);
      previousWord = word;
      continue;
    }

    if (/[+\-*/%@&|^~:=<>!.]/.test(character)) {
      const start = index++;
      while (index < source.length && /[+\-*/%@&|^~:=<>!.]/.test(source[index])) index++;
      highlighted += token("operator", source.slice(start, index));
      previousWord = "";
      continue;
    }

    highlighted += escapeHtml(character);
    previousWord = "";
    index++;
  }

  return highlighted;
}

export function mountPythonHighlighting(textarea) {
  const editor = document.createElement("div");
  editor.className = "python-editor";
  const backdrop = document.createElement("pre");
  backdrop.className = "python-highlight";
  backdrop.setAttribute("aria-hidden", "true");
  const code = document.createElement("code");
  backdrop.append(code);
  textarea.before(editor);
  editor.append(backdrop, textarea);

  const sync = () => {
    code.innerHTML = highlightPython(textarea.value) + (textarea.value.endsWith("\n") ? " " : "");
    backdrop.scrollTop = textarea.scrollTop;
    backdrop.scrollLeft = textarea.scrollLeft;
  };
  textarea.addEventListener("input", sync);
  textarea.addEventListener("scroll", sync);
  sync();
  return sync;
}

export function pythonErrorFeedback(message) {
  const text = String(message || "Python execution failed");
  const line = Number(text.match(/File "<exec>", line (\d+)/)?.[1] ?? text.match(/line (\d+)/i)?.[1]) || null;
  const syntax = text.match(/(?:^|\n)(IndentationError|SyntaxError):\s*([^\n]*)/) ?? text.match(/(IndentationError|SyntaxError):\s*([^\n]*)/);
  if (!syntax) return { line, message: text };
  return {
    line,
    message: `${syntax[1]}${line ? ` on line ${line}` : ""}: ${syntax[2] || "check the highlighted code"}`,
  };
}

export function showPythonError(textarea, message) {
  const feedback = pythonErrorFeedback(message);
  if (feedback.line) {
    const lines = textarea.value.split("\n");
    const start = lines.slice(0, feedback.line - 1).reduce((length, line) => length + line.length + 1, 0);
    const end = start + (lines[feedback.line - 1]?.length ?? 0);
    textarea.focus({ preventScroll: true });
    textarea.setSelectionRange(start, end);
    const lineHeight = Number.parseFloat(getComputedStyle(textarea).lineHeight) || 16;
    textarea.scrollTop = Math.max(0, (feedback.line - 2) * lineHeight);
    textarea.dispatchEvent(new Event("scroll"));
  }
  return feedback.message;
}
