// Syntax smoke test for the Citadel pack's .luau files.
// luaparse is a Lua parser; the pack's only Luau-only syntax is
// generalized iteration (`for ... in <table> do`), which we rewrite to
// pairs(<table>) before parsing. Catches anything else: unbalanced
// blocks, bad tables, typos. Run: NODE_PATH=/tmp/luacheck/node_modules node this
const fs = require("fs");
const path = require("path");
const luaparse = require("luaparse");

const ROOT = "/home/z/my-project/scripts/onixmg_citadel/pack";

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) walk(path.join(dir, e.name), out);
    else if (e.name.endsWith(".luau")) out.push(path.join(dir, e.name));
  }
  return out;
}

// for a, b in <expr> do  ->  for a, b in pairs(<expr>) do
// (skip numeric for, which has no `in`; skip real pairs/ipairs calls)
function generalize(src) {
  return src.replace(
    /\bfor\s+([A-Za-z_][\w\s,]*?)\s+in\s+(.+?)\s+do\b/g,
    (m, names, expr) => {
      if (/^(pairs|ipairs|next)\s*\(/.test(expr)) return m;
      return `for ${names} in pairs(${expr}) do`;
    }
  );
}

let ok = 0;
const bad = [];
for (const f of walk(ROOT).sort()) {
  const src = fs.readFileSync(f, "utf8");
  try {
    luaparse.parse(generalize(src), { luaVersion: "5.3" });
    ok++;
  } catch (e) {
    bad.push(`${path.relative(ROOT, f)}: ${e.message}`);
  }
}
console.log(`parsed OK: ${ok}`);
for (const b of bad) console.log("ERROR " + b);
process.exit(bad.length ? 1 : 0);
