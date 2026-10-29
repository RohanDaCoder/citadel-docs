/** Lightweight tokenizer for Luau / YAML / shell code blocks. */

export interface Token {
  type:
    | "plain"
    | "comment"
    | "string"
    | "number"
    | "keyword"
    | "boolean"
    | "nil"
    | "fn"
    | "api"
    | "operator"
    | "property"
    | "yaml-key"
    | "sh-cmd";
  v: string;
}

const LUAU_KEYWORDS = new Set([
  "and", "break", "do", "else", "elseif", "end", "for", "function", "if",
  "in", "local", "not", "or", "repeat", "return", "then", "until", "while",
  "continue", "type", "export", "self",
]);

const LUAU_LITERALS = new Set(["true", "false", "nil"]);

const CITADEL_API = new Set([
  "world", "players", "ui", "sound", "fx", "vec3", "color", "colors", "time",
  "data", "tween", "fields", "noise", "parts", "game", "camera", "commands",
  "models", "task", "rooms", "routes", "storage", "message", "http", "stores",
  "shop", "network", "hub", "citadel", "math", "table", "string", "os",
  "coroutine", "buffer", "utf8", "print", "error", "assert", "pcall", "xpcall",
  "select", "typeof", "tostring", "tonumber", "ipairs", "pairs", "next",
  "require", "setmetatable", "getmetatable", "rawget", "rawset", "unpack",
]);

const SHELL_CMDS = new Set([
  "citadel", "cd", "ls", "mkdir", "touch", "cat", "echo", "curl", "git",
  "npm", "bun", "node", "python", "chmod", "mv", "cp", "rm", "nano", "code",
  "tar", "unzip", "wget", "sudo", "export", "source",
]);

function pushPlain(tokens: Token[], text: string) {
  if (text) tokens.push({ type: "plain", v: text });
}

export function tokenizeLuau(code: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;
  let plain = "";

  const flush = () => {
    pushPlain(tokens, plain);
    plain = "";
  };

  while (i < code.length) {
    const ch = code[i];
    const rest = code.slice(i);

    // line comment
    if (ch === "-" && code[i + 1] === "-") {
      let end = code.indexOf("\n", i);
      if (end === -1) end = code.length;
      // long comment --[==[ ... ]==]
      const longOpen = /^--\[(=*)\[/.exec(rest);
      if (longOpen) {
        const closer = `]${longOpen[1]}]`;
        const endLong = code.indexOf(closer, i + longOpen[0].length);
        const stop = endLong === -1 ? code.length : endLong + closer.length;
        flush();
        tokens.push({ type: "comment", v: code.slice(i, stop) });
        i = stop;
        continue;
      }
      flush();
      tokens.push({ type: "comment", v: code.slice(i, end) });
      i = end;
      continue;
    }

    // strings
    if (ch === '"' || ch === "'") {
      let j = i + 1;
      while (j < code.length && code[j] !== ch) {
        if (code[j] === "\\") j++;
        if (code[j] === "\n") break;
        j++;
      }
      flush();
      tokens.push({ type: "string", v: code.slice(i, Math.min(j + 1, code.length)) });
      i = j + 1;
      continue;
    }

    // long string [[...]]
    if (ch === "[" && (code[i + 1] === "[" || code[i + 1] === "=")) {
      const m = /^\[(=*)\[/.exec(rest);
      if (m) {
        const closer = `]${m[1]}]`;
        const end = code.indexOf(closer, i + m[0].length);
        const stop = end === -1 ? code.length : end + closer.length;
        flush();
        tokens.push({ type: "string", v: code.slice(i, stop) });
        i = stop;
        continue;
      }
    }

    // numbers
    if (/[0-9]/.test(ch) && !/[a-zA-Z0-9_]/.test(code[i - 1] || " ")) {
      const m = /^(0x[0-9a-fA-F]+|[0-9]*\.?[0-9]+([eE][+-]?[0-9]+)?)/.exec(rest);
      if (m) {
        flush();
        tokens.push({ type: "number", v: m[0] });
        i += m[0].length;
        continue;
      }
    }

    // identifiers
    if (/[a-zA-Z_]/.test(ch)) {
      const m = /^[a-zA-Z_][a-zA-Z0-9_]*/.exec(rest);
      if (m) {
        const word = m[0];
        const after = code.slice(i + word.length).match(/^\s*\(/);
        const prevChar = (() => {
          let k = i - 1;
          while (k >= 0 && /\s/.test(code[k])) k--;
          return k >= 0 ? code[k] : "";
        })();
        flush();
        if (LUAU_KEYWORDS.has(word)) {
          tokens.push({ type: "keyword", v: word });
        } else if (LUAU_LITERALS.has(word)) {
          tokens.push({ type: "boolean", v: word });
        } else if (CITADEL_API.has(word)) {
          tokens.push({ type: "api", v: word });
        } else if (after) {
          tokens.push({ type: "fn", v: word });
        } else if (prevChar === "." || prevChar === ":") {
          tokens.push({ type: "property", v: word });
        } else {
          tokens.push({ type: "plain", v: word });
        }
        i += word.length;
        continue;
      }
    }

    // operators
    if (/[=+\-*/%<>~#{}()[\];:,.]/.test(ch)) {
      flush();
      tokens.push({ type: "operator", v: ch });
      i++;
      continue;
    }

    plain += ch;
    i++;
  }
  flush();
  return tokens;
}

export function tokenizeYaml(code: string): Token[] {
  const tokens: Token[] = [];
  for (const line of code.split("\n")) {
    const commentIdx = line.indexOf("#");
    const m = /^(\s*)([A-Za-z0-9_.-]+)(:)(.*)$/.exec(line);
    if (m) {
      pushPlain(tokens, m[1]);
      tokens.push({ type: "yaml-key", v: m[2] });
      tokens.push({ type: "operator", v: ":" });
      const value = m[4];
      if (value) {
        const vc = value.indexOf("#");
        if (vc >= 0) {
          pushPlain(tokens, value.slice(0, vc));
          tokens.push({ type: "comment", v: value.slice(vc) });
        } else {
          pushPlain(tokens, value);
        }
      }
    } else if (commentIdx === 0) {
      tokens.push({ type: "comment", v: line });
    } else {
      pushPlain(tokens, line);
    }
    tokens.push({ type: "plain", v: "\n" });
  }
  return tokens;
}

export function tokenizeShell(code: string): Token[] {
  const tokens: Token[] = [];
  for (const line of code.split("\n")) {
    const trimmed = line.trim();
    if (trimmed.startsWith("#")) {
      tokens.push({ type: "comment", v: line });
      tokens.push({ type: "plain", v: "\n" });
      continue;
    }
    const m = /^(\s*)([a-zA-Z_][a-zA-Z0-9_.-]*)(.*)$/.exec(line);
    if (m && SHELL_CMDS.has(m[2])) {
      pushPlain(tokens, m[1]);
      tokens.push({ type: "sh-cmd", v: m[2] });
      pushPlain(tokens, m[3]);
    } else {
      pushPlain(tokens, line);
    }
    tokens.push({ type: "plain", v: "\n" });
  }
  return tokens;
}

export function tokenizeCode(code: string, lang: string): Token[] {
  switch (lang) {
    case "luau":
    case "lua":
      return tokenizeLuau(code);
    case "yaml":
    case "yml":
      return tokenizeYaml(code);
    case "sh":
    case "bash":
    case "shell":
    case "zsh":
      return tokenizeShell(code);
    default:
      return [{ type: "plain", v: code }];
  }
}
