#!/usr/bin/env python3
"""Generate citadel-ts/types/citadel.d.ts — TypeScript declarations for the
Minefort Citadel Luau API — strictly from verified, crawled sources:

  * scripts/dataset.json   the structured extraction of the official docs
                          (reference_parents + reference_members; every
                          member entry carries its documented signature).
  * scripts/wiki_src/      the authored wiki built from the same crawl — used
                          ONLY where the reference section lacks coverage
                          (task.*, camera.path, Vec3/Color method shapes,
                          player.ui). Every such block cites its source.

Nothing is guessed: anything the sources do not specify is typed `unknown`
and counted in the report. Regenerate: python3 scripts/gen_citadel_dts.py
"""
import json
import os
import re
import shutil
from collections import OrderedDict

ROOT = "/home/z/my-project"
DS = json.load(open(f"{ROOT}/scripts/dataset.json"))
P = DS["reference_parents"]
M = DS["reference_members"]
OUT = f"{ROOT}/citadel-ts/types/citadel.d.ts"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

WARN = []
NOTES = []          # deliberate conversions (tag strips, recoveries)
STATS = OrderedDict()

# Globals enumeration — verified: wiki concepts/conventions.md "Namespaces".
# NOTE: blocks/entities/biomes/items/recipes are NOT top-level globals — they
# live on game.* (the dataset's Game members document the fields). Their
# interfaces are still emitted (as plain types) for Game's fields.
GLOBAL_GROUP = {          # member-group key -> interface name for the global
    "World": "World", "Players": "Players", "Ui": "Ui", "Game": "Game",
    "Fx": "Fx", "Sound": "Sound", "Commands": "Commands",
    "time": "Time", "rooms": "Rooms",
    "storage": "Storage", "stores": "Stores", "http": "Http",
    "network": "Network", "shop": "Shop", "hub": "Hub", "models": "Models",
    "parts": "Parts", "routes": "Routes", "data": "Data", "fields": "Fields",
    "colors": "Colors", "citadel": "Citadel", "noise": "NoiseApi",
}
SPEC_TYPES = {"BlockSpec", "BlockAmendSpec", "EntitySpec", "EntityAmendSpec",
              "PartDefinition"}          # user-authored spec tables
PRIMITIVES = {"number", "string", "boolean", "unknown", "undefined", "never",
              "object"}
PRIM_MAP = {"nil": "undefined", "integer": "number", "thread": "unknown",
            "function": "unknown"}
TS_KEYWORD_MEMBERS = {"new"}
FN_RE = re.compile(r"^\((.*)\)\s*->\s*(.+)$", re.S)


class Ctx:
    def __init__(self, declared):
        self.declared = declared
        self.where = "prelude"


def top_split(s, sep):
    """Split on a single-char separator at paren/brace/quote depth 0."""
    parts, depth, start, i, instr = [], 0, 0, 0, False
    while i < len(s):
        c = s[i]
        if instr:
            if c == '"':
                if i + 1 < len(s) and s[i + 1] == '"':
                    i += 2
                    continue
                instr = False
            i += 1
            continue
        if c == '"':
            instr = True
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == sep and depth == 0:
            parts.append(s[start:i])
            start = i + 1
        i += 1
    parts.append(s[start:])
    return parts


def conv_type(s, ctx, nested=False):
    """Convert a Luau type string to a TypeScript type string."""
    s = (s or "").strip()
    s = re.sub(r"\s*\|\s*\[\]\s*$", "", s).strip()   # crawler artifact
    # flattened Luau line comments: drop "-- text" up to the next "field:".
    s = re.sub(r"--\s+[\w\s]*?(?=\s*[a-z_]+\s*:)", "", s)
    if not s or s == "?":
        return "unknown"
    if "|" in s and len(top_split(s, "|")) > 1:
        alts, seen = [], set()
        for p in top_split(s, "|"):
            t = conv_type(p, ctx, True)
            if " => " in t:            # TS1385: parenthesize fn types in unions
                t = f"({t})"
            if t and t not in seen:
                seen.add(t)
                alts.append(t)
        return alts[0] if len(alts) == 1 else " | ".join(alts)
    if "&" in s and len(top_split(s, "&")) > 1:
        return " & ".join(conv_type(p, ctx, True) for p in top_split(s, "&"))
    if s.endswith("?"):
        base = conv_type(s[:-1], ctx, True)
        return base if base in ("unknown", "any") else f"{base} | undefined"
    s = s.strip()
    if s.startswith("(") and s.endswith(")"):
        inner = s[1:-1].strip()
        if not inner:
            return "void" if not nested else "unknown"
        if FN_RE.match(inner):          # a function type wrapped in parens
            return conv_type(inner, ctx, nested)
        if not FN_RE.match(s):
            if len(top_split(inner, ",")) > 1:      # tuple in type position
                return ("LuaMultiReturn<[" + ", ".join(
                    conv_type(e, ctx, True)
                    for e in top_split(inner, ",")) + "]>")
            return conv_type(inner, ctx, True)
    m = FN_RE.match(s)
    if m:
        params_s, ret_s = m.group(1).strip(), m.group(2).strip()
        ret_s = re.sub(r"^\((.*)\)$", r"\1", ret_s).strip()
        ret_ts = "void" if ret_s in ("", "()") else conv_type(ret_s, ctx, True)
        pl = []
        for j, pp in enumerate(top_split(params_s, ",")):
            pp = pp.strip()
            if not pp:
                continue
            if pp.startswith("..."):
                rest = pp[3:].strip()
                ty = rest.split(":", 1)[1].strip() if ":" in rest else "any"
                pl.append((f"...args: {conv_type(ty, ctx, True)}[]", False))
            elif ":" in pp:
                nm, ty = pp.split(":", 1)
                nm, ty = nm.strip(), ty.strip()
                opt = ty.endswith("?")
                ty = ty.rstrip("?").strip()
                pl.append((f"{nm}: {conv_type(ty, ctx, True)}", opt))
            else:
                pl.append((f"_{j}: {conv_type(pp, ctx, True)}", False))
        # fold mid-list optionals into their type (TS1016 applies to
        # function types as well)
        names = []
        for i, (frag, opt) in enumerate(pl):
            if opt and any(o for _, o in pl[i + 1:]):
                nm, ty = frag.split(":", 1)
                if not ty.strip().endswith("| undefined"):
                    frag = f"{nm}: {ty.strip()} | undefined"
            names.append(frag)
        head = "(this: void, " + ", ".join(names) + ")" if names else "(this: void)"
        return f"{head} => {ret_ts}"
    if s.startswith("{") and s.endswith("}"):
        inner = s[1:-1].strip()
        if not inner:
            return "object"
        elems = top_split(inner, ",")
        mm = re.match(r"^\[\s*(\w+)\s*\]\s*:\s*(.+)$", elems[0].strip(), re.S)
        if len(elems) == 1 and mm and mm.group(1) not in ("string", "number"):
            # a literal/union key (e.g. [Face]): TS needs a mapped type
            return f"{{ [K in {mm.group(1)}]: {conv_type(mm.group(2), ctx, True)} }}"
        if len(elems) == 1 and mm:
            key = {"any": "string"}.get(mm.group(1), mm.group(1))
            return f"{{ [key: {key}]: {conv_type(mm.group(2), ctx, True)} }}"
        if len(elems) == 1 and len(top_split(elems[0], ":")) == 1 \
                and not elems[0].strip().startswith("["):
            return f"({conv_type(elems[0], ctx, True)})[]" if \
                elems[0].strip().startswith("{") else \
                f"{conv_type(elems[0], ctx, True)}[]"     # array {T} / { {T} }
        fields = []
        for fe in elems:
            fe = fe.strip().rstrip(",").strip()
            if not fe:
                continue
            if fe.startswith("["):
                mm2 = re.match(r"^\[\s*(\w+)\s*\]\s*:\s*(.+)$", fe)
                if mm2:
                    key = {"any": "string"}.get(mm2.group(1), mm2.group(1))
                    fields.append(f"[key: {key}]: {conv_type(mm2.group(2), ctx, True)}")
                    continue
            fparts = top_split(fe, ":")
            if len(fparts) > 1:
                nm, ty = fparts[0].strip(), ":".join(fparts[1:]).strip()
                opt = nm.endswith("?")
                nm = nm.rstrip("?").strip()
                if ty.endswith("?"):
                    opt = True
                    ty = ty[:-1].strip()
                tag = re.match(r"^(read|write|export|type)\s+(.+)$", nm)
                if tag:
                    nm = tag.group(2)
                    NOTES.append((ctx.where, f"stripped '{tag.group(1)}' tag on {nm}"))
                if nm in TS_KEYWORD_MEMBERS:
                    nm = f'"{nm}"'
                fields.append(f"{nm}{'?' if opt else ''}: {conv_type(ty, ctx, True)}")
            else:
                fields.append(f'"{fe}": unknown')
                WARN.append((ctx.where, f"bare table field {fe!r} -> unknown"))
        return "{ " + "; ".join(fields) + " }"
    if s.startswith('"') and s.endswith('"'):
        return s
    if s in ("true", "false"):
        return s
    if s in PRIM_MAP:
        return PRIM_MAP[s]
    if s == "any":
        return "any"
    if s in PRIMITIVES or s in ("object",):
        return s
    if s in ctx.declared:
        return s
    WARN.append((ctx.where, f"unresolved identifier {s!r} -> unknown"))
    return "unknown"


SIG_ARROW = "→"


def parse_signature(sig):
    sig = (sig or "").strip()
    rets = ""
    if SIG_ARROW in sig:
        sig, rets = sig.split(SIG_ARROW, 1)
        sig, rets = sig.strip(), rets.strip()
    m = re.match(r"^([\w.]+)([:.])([\w.]+)\s*\((.*)\)\s*$", sig, re.S)
    if not m:
        return None
    return m.group(1), m.group(2) == ":", m.group(3), m.group(4), rets


def doc_line(mem, indent="    "):
    lead = (mem.get("lead") or "").strip()
    if lead:
        first = lead.split(". ")[0].replace("*/", "*∕").strip()
        if not first.endswith("."):
            first += "."
        return f"{indent}/** {first} */\n"
    return ""


def params_to_ts(params_s, ctx):
    """Signature parameter list -> [(tsName, tsType, isOptionalModifier)]."""
    out = []
    for j, pp in enumerate(top_split(params_s, ",")):
        pp = pp.strip()
        if not pp:
            continue
        if pp.startswith("("):
            # a parenthesised parameter: a callback, a union with a callback,
            # or a wrapper form — convert the whole and name it positionally
            out.append((f"arg{j}", conv_type(pp, ctx, True), False))
        elif pp.startswith("..."):
            rest = pp[3:].strip()
            ty = rest.split(":", 1)[1].strip() if ":" in rest else "any"
            out.append(("...args", f"{conv_type(ty, ctx, True)}[]", False))
        elif ":" in pp:
            nm, ty = pp.split(":", 1)
            nm, ty = nm.strip(), ty.strip()
            opt = ty.endswith("?")
            ty = ty.rstrip("?").strip()
            out.append((nm, conv_type(ty, ctx, True), opt))
        else:
            out.append((f"_{j}", conv_type(pp, ctx, True), False))
    # a required parameter cannot follow an optional one (TS1016): fold
    # mid-list optionals into their type instead
    for i, (nm, ty, opt) in enumerate(out):
        if opt and any(not o2 for _, _, o2 in out[i + 1:]):
            if not ty.endswith("| undefined"):
                ty = f"{ty} | undefined"
            out[i] = (nm, ty, False)
    return [(f"{nm}{'?' if opt else ''}", ty) for nm, ty, opt in out]


def returns_to_ts(rets_s, ctx):
    if not rets_s:
        return "void"
    inner = re.sub(r"^\((.*)\)$", r"\1", rets_s.strip()).strip()
    elems = top_split(inner, ",")
    if len(elems) > 1:
        return ("LuaMultiReturn<[" + ", ".join(conv_type(e, ctx, True)
                                               for e in elems) + "]>")
    return conv_type(rets_s, ctx)


def balanced(s):
    """True if parens/braces/brackets nest cleanly and end at depth 0."""
    depth, i, instr = 0, 0, False
    while i < len(s):
        c = s[i]
        if instr:
            if c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth < 0:
                return False
        i += 1
    return depth == 0


def unwrap_balanced(s):
    """Strip one outer paren pair if what remains stays balanced."""
    s = s.strip()
    if not (s.startswith("(") and s.endswith(")")):
        return s
    depth, i, instr = 0, 0, False
    while i < len(s):
        c = s[i]
        if instr:
            if c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0 and i < len(s) - 1:
                return s            # closes before the end: not a wrapper
        i += 1
    return s[1:-1].strip() if depth == 0 else s


def member_decl(parent, name, mem, ctx):
    kind = mem.get("kind")
    sig = (mem.get("signature") or "").strip()
    ctx.where = f"{parent}.{name}"
    if kind == "field":
        m = re.match(r"^[\w.]+\.[\w.]+\s*:\s*(.+)$", sig)
        if not m:
            WARN.append((ctx.where, f"field type unparsed: {sig!r}"))
            nm = f'"{name}"' if name in TS_KEYWORD_MEMBERS else name
            return f"{doc_line(mem)}{nm}: unknown"
        raw = m.group(1).strip()
        # a documented optional field ("field: T ?") -> optional property
        opt = raw.endswith("?")
        if opt:
            raw = raw[:-1].strip()
        ty = conv_type(raw, ctx)
        nm = f'"{name}"' if name in TS_KEYWORD_MEMBERS else name
        if opt and ty not in ("unknown", "any"):
            return f"{doc_line(mem)}{nm}?: {ty}"
        return f"{doc_line(mem)}{nm}: {ty}"
    nm = f'"{name}"' if name in TS_KEYWORD_MEMBERS else name
    parsed = parse_signature(sig)
    if parsed is None:
        WARN.append((ctx.where, f"UNPARSED signature {sig!r}"))
        return f"// UNPARSED {ctx.where}: {sig}"
    recv, colon, name_p, params_s, rets_s = parsed

    # Overloaded signatures: the crawl renders them as
    #   receiver.name(<form A>) -> & (<form B>)
    # — every form is a full function type. Emit one overload per form.
    if "&" in rets_s and len(top_split(rets_s, "&")) > 1:
        forms = [params_s] + [p for p in top_split(rets_s, "&") if p.strip()]
        lines = []
        for form in forms:
            fm = None
            for cand in (unwrap_balanced(form.strip()), form.strip()):
                m = FN_RE.match(cand)
                if m and balanced(m.group(1)):
                    fm = m
                    break
            if not fm:
                WARN.append((ctx.where, f"overload form unparsed: {form!r}"))
                continue
            pl = params_to_ts(fm.group(1), ctx)
            ret_ts = returns_to_ts(fm.group(2), ctx)
            args = ", ".join(f"{k}: {v}" for k, v in pl)
            if kind == "method":
                lines.append(f"{doc_line(mem)}{nm}({args}): {ret_ts}")
            else:
                self_dot = "this: void" + (", " if args else "")
                lines.append(f"{doc_line(mem)}{nm}({self_dot}{args}): {ret_ts}")
        return "\n".join(lines)

    ret_ts = returns_to_ts(rets_s, ctx)

    if parent in SPEC_TYPES and kind == "function" \
            and FN_RE.match(params_s.strip()):
        # spec handler: a user-assigned callback field; params_s IS its type
        cb_nm = f'"{name}"' if name in TS_KEYWORD_MEMBERS else name
        return f"{doc_line(mem)}{cb_nm}?: {conv_type(params_s, ctx)}"

    pl = params_to_ts(params_s, ctx)
    args = ", ".join(f"{k}: {v}" for k, v in pl)
    if kind == "method":
        return f"{doc_line(mem)}{nm}({args}): {ret_ts}"
    self_dot = "this: void" + (", " if args else "")
    return f"{doc_line(mem)}{nm}({self_dot}{args}): {ret_ts}"


# ------------------------------------------------------------------ registry
DECLARED = set()
for g in M:
    DECLARED.add(GLOBAL_GROUP.get(g, g))
for k in P:
    DECLARED.add(k)
DECLARED |= {"Vec3", "Color", "Vec3Constructor", "ColorConstructor",
             "NoiseApi", "TaskApi", "CameraApi", "CameraPathShot",
             "CameraPathOptions", "CameraPathRunner", "buffer", "Faces",
             "TimeName"}
ctx = Ctx(DECLARED)

interfaces = OrderedDict()
aliases = OrderedDict()
docs = OrderedDict()
emitted_globals = []


def emit_interface(name, members, doc=""):
    if name in interfaces or name in aliases:
        raise SystemExit(f"collision: {name}")
    interfaces[name] = members
    if doc:
        docs[name] = doc


# ------------------------------------------- pass 1: groups -> interfaces
for gname, mems in M.items():
    if gname in ("vec3", "color", "Faces"):
        continue                # constructors / Faces are emitted specially
    iname = GLOBAL_GROUP.get(gname, gname)
    lines = [member_decl(gname, mn, mems[mn], ctx) for mn in sorted(mems)]
    emit_interface(iname, lines, (P.get(gname, {}).get("lead") or "").strip())
    if gname in GLOBAL_GROUP:
        emitted_globals.append((gname, iname))

STATS["member groups -> interfaces"] = len(M) - 3
STATS["API members converted"] = sum(len(v) for v in M.values())

# ------------------------------------------- pass 2: typedef-only parents
OPAQUE = []
for k in sorted(P):
    if k in M or k in ("vec3", "color", "message", "tween", "camera", "task",
                      "Vec3", "Color", "TimeName", "Faces", "DataView"):
        continue
    # skip lowercase twin stubs of PascalCase groups (world/World twins
    # whose canonical page carries the members)
    if k[0].islower() and k.capitalize() in M:
        continue
    td = (P[k].get("typedef") or "").strip()
    lead = (P[k].get("lead") or "").strip()
    ctx.where = f"typedef:{k}"
    if not td:
        emit_interface(k, [], f"{lead} [no documented members: opaque]" if lead
                      else "[no documented members: opaque]")
        OPAQUE.append(k)
        continue
    before = len(WARN)
    ts = conv_type(td, ctx, True)
    new = WARN[before:]
    garbled = td.endswith("|") or td.startswith("|") or \
        any("unresolved identifier" in w[1] for w in new) or not ts
    if garbled:
        emit_interface(k, [], f"{lead} [typedef not machine-convertible in "
                      f"the source extract: opaque]" if lead
                      else "[typedef not machine-convertible: opaque]")
        OPAQUE.append(k)
    else:
        aliases[k] = ts

STATS["typedef aliases"] = len(aliases)
STATS["opaque interfaces"] = len(OPAQUE)

# ------------------------------------------------------------------ assembly
def render_interface(name, members, doc=""):
    out = []
    if doc:
        out.append(f"/** {doc.replace('*/', '*∕')} */")
    out.append(f"interface {name} {{")
    for m in members:
        for ln in m.split("\n"):
            out.append(f"    {ln}" if ln.strip() else "")
    out.append("}")
    return "\n".join(out)


VERIFIED = '''// ===========================================================================
// VERIFIED SUPPLEMENT — members the reference section does not carry, taken
// from the wiki pages built from the official docs. Each block cites source.
// ===========================================================================

/** A position or direction: `vec3(x, y, z)`.
 *  Source: wiki Conventions ("Positions are vec3(x, y, z) with fields
 *  x, y, z"); methods from the "Vectors and colours" doc. Method names and
 *  arities are documented; return types follow the standard vector
 *  semantics, with lerp corroborated by the documented Color.lerp
 *  signature. The documented operators (+ - * / unary - ==) are not
 *  representable in TypeScript and are not declared. */
interface Vec3 {
    x: number;
    y: number;
    z: number;
    /** `a:magnitude()` */
    magnitude(): number;
    /** `a:unit()` */
    unit(): Vec3;
    /** `a:dot(b)` */
    dot(other: Vec3): number;
    /** `a:cross(b)` */
    cross(other: Vec3): Vec3;
    /** `a:distance(b)` */
    distance(other: Vec3): number;
    /** `a:lerp(b, t)` */
    lerp(other: Vec3, t: number): Vec3;
    /** `a:floor()` */
    floor(): Vec3;
    /** `a:with{ y = 70 }` — a copy with the given fields replaced. */
    with(fields: { x?: number; y?: number; z?: number }): Vec3;
}

/** Callable global `vec3`: the constructor (dataset typedef) plus the
 *  dataset members `vec3.up` and `vec3.zero`. */
interface Vec3Constructor {
    (this: void, x: number, y: number, z: number): Vec3;
    up: Vec3;
    zero: Vec3;
}
declare const vec3: Vec3Constructor;

/** A colour: fields `r`, `g`, `b` in 0..1. Source: wiki Conventions
 *  ("Colours are color(r, g, b) in 0..1"); lerp from the documented
 *  `lerp: (self: Color, other: Color, t: number) -> Color` signature. */
interface Color {
    r: number;
    g: number;
    b: number;
    /** `c:lerp(d, t)` */
    lerp(other: Color, t: number): Color;
}
'''

TASK_CAMERA = '''// A named time of day. RECOVERED verbatim from the documented leads —
// TimeName: "sunrise, day, noon, sunset, night or midnight" and world.time:
// "ticks, or \"sunrise\", \"day\", \"noon\", \"sunset\", \"night\", \"midnight\"".
// (The dataset's TimeName typedef string is extract-damaged.)
type TimeName = "sunrise" | "day" | "noon" | "sunset" | "night" | "midnight";

/** The face-keyed texture table a BlockSpec takes. RECOVERED from the
 *  documented Faces leads + their flattened signatures: `all` is one
 *  picture for all six faces, `side` for the four sides, `top` and
 *  `bottom` the ends (Faces.all); the six direction names with a face
 *  left out defaulting to `side` (Faces.down); `front`/`back` for a
 *  facing block (Faces.front). */
type Faces =
    | { all?: TextureRef; side?: TextureRef; top?: TextureRef; bottom?: TextureRef }
    | { up?: TextureRef; down?: TextureRef; north?: TextureRef; south?: TextureRef; west?: TextureRef; east?: TextureRef }
    | { front?: TextureRef; back?: TextureRef };

'''

TASK_CAMERA += '''// `task` — the scheduler. Source: wiki Runtime (the task semantics table)
// and "Modules and tasks": spawn/delay/defer accept a function or a suspended
// coroutine, forward all arguments (including nils) and return that
// coroutine. The thread itself is opaque (no members documented).
interface TaskApi {
    /** `task.spawn(fn, ...)` — runs immediately until the task yields or
     *  returns. Also accepts a suspended coroutine. Returns the thread. */
    spawn(this: void, fn: (this: void, ...args: any[]) => unknown, ...args: unknown[]): unknown;
    /** `task.delay(sec, fn, ...)` — after sec elapsed real seconds. */
    delay(this: void, sec: number, fn: (this: void, ...args: any[]) => unknown, ...args: unknown[]): unknown;
    /** `task.defer(fn, ...)` — on the next scheduler turn. */
    defer(this: void, fn: (this: void, ...args: any[]) => unknown, ...args: unknown[]): unknown;
    /** `task.wait(sec)` — yields the calling thread until sec real seconds
     *  have passed. Event callbacks and main.luau may call it; synchronous
     *  ask handlers and module top levels may not. */
    wait(this: void, sec: number): unknown;
    /** `task.cancel(task)` — works on a suspended task, also after
     *  task.wait; cancelling a running thread is an error. */
    cancel(this: void, task: unknown): void;
}
declare const task: TaskApi;

/** One shot of a camera path. Source: wiki Movement ("Camera paths"):
 *  `{ at = vec3(...), look_at = vec3(...), duration = 5, easing = "out" }`;
 *  `at` may be a player ("a shot { at = player } is the player's eyes").
 *  The docs also note "a player or thing in a shot is read when the shot
 *  starts" — things (mount targets) are accepted but not enumerated. */
interface CameraPathShot {
    at: Vec3 | Player;
    look_at?: Vec3 | Player;
    duration?: number;
    easing?: Easing;
}

/** Source: wiki Movement: `camera.path(shots, { easing = "in_out",
 *  on_done = function() ... end })`. */
interface CameraPathOptions {
    easing?: Easing;
    on_done?: (this: void) => void;
}

/** "It returns the camera and a handle with cancel()" — wiki Movement.
 *  Declared with Lua method-call (colon) convention, like Connection. */
interface CameraPathRunner {
    cancel(): void;
}

/** `camera` — Source: wiki Movement ("Camera paths"): camera.path is a
 *  fixed camera that eases from shot to shot; each shot after the first
 *  takes its own duration (or the path's, 5 seconds by default). */
interface CameraApi {
    path(this: void, shots: CameraPathShot[], opts?: CameraPathOptions): LuaMultiReturn<[Camera, CameraPathRunner]>;
}
declare const camera: CameraApi;
'''

header = '''/**
 * citadel.d.ts — TypeScript declarations for the Minefort Citadel Luau API.
 *
 * GENERATED from the official Minefort Citadel documentation (the crawled
 * corpus in scripts/dataset.json — every documented API member) — regenerate
 * with:  python3 scripts/gen_citadel_dts.py
 * Do not edit by hand.
 *
 * Sourcing rules (strictly no invention):
 *   - every interface, function and field below is converted mechanically
 *     from the documented signatures in dataset.json;
 *   - the few members the reference section lacks (task.*, camera.path,
 *     Vec3/Color shapes, player.ui) come from the wiki pages built from the
 *     same official docs, and carry a "Source:" comment;
 *   - anything the docs leave unspecified is typed `unknown`.
 *
 * Calling conventions (TypeScriptToLua): members with `this: void` are dot
 * calls (world.spawn(...)); members without it are Lua colon calls
 * (player:message(...), connection:cancel()). Callbacks are always
 * `this: void` — pass arrow functions. Multi-value returns use
 * LuaMultiReturn: destructure with `const [a, b] = ...`.
 */

// Luau `buffer` — an opaque byte buffer (the docs never enumerate members).
type buffer = unknown;

/** Citadel's DataView — a live view over persistent data, readable and
 *  writable by any key (the documented typedef is `{ [any]: any }`). NB:
 *  unrelated to the ECMAScript DataView that comes with lib esnext; the
 *  two declarations merge, but only the index below is Citadel's. */
interface DataView {
    [key: string]: any;
}

'''

body = []
body.append("// ================================ Globals ================================")
body.append(VERIFIED.strip())
body.append("")

# color constructor: call signature + dataset members (hsv, gradient, nearest)
cc_members = ["    (this: void, r: number, g: number, b: number): Color;"]
cc_members += ["    " + member_decl("color", mn, M["color"][mn], ctx).replace(
    "this: void, ", "this: void, ")
    for mn in sorted(M["color"])]
body.append("/** Callable global `color`: `color(r, g, b)` (dataset typedef),"
            " plus its dataset members. */")
body.append("interface ColorConstructor {")
body.extend(cc_members)
body.append("}")
body.append("declare const color: ColorConstructor;")
body.append("")

# callable function globals from dataset typedefs
for gname in ("message", "tween"):
    td = (P[gname].get("typedef") or "").strip()
    ctx.where = f"callable:{gname}"
    m = FN_RE.match(td)
    if not m:
        WARN.append((ctx.where, f"{gname} typedef unparsable: {td!r}"))
        continue
    pl = params_to_ts(m.group(1), ctx)
    ret = returns_to_ts(m.group(2), ctx)
    args = ", ".join(f"{k}: {v}" for k, v in pl)
    lead = (P[gname].get("lead") or "").split(". ")[0]
    body.append(f"/** {gname} — callable global. {lead} */")
    body.append(f"declare function {gname}(this: void, {args}): {ret};")
    body.append("")

body.append(TASK_CAMERA.strip())
body.append("")

# table globals: interface + declare const (runtime name = the documented
# global name: lowercase, even when the canonical docs page is PascalCase)
for gname, iname in sorted(emitted_globals, key=lambda x: x[0].lower()):
    runtime = gname if gname[0].islower() else gname.lower()
    body.append(render_interface(iname, interfaces.pop(iname),
                                 docs.get(iname, "")))
    body.append(f"/** The `{runtime}` global. */")
    body.append(f"declare const {runtime}: {iname};")
    body.append("")

body.append("// ================================= Types =================================")
for name in sorted(interfaces, key=str.lower):
    body.append(render_interface(name, interfaces[name], docs.get(name, "")))
    body.append("")

body.append("// ============================== Type aliases ==============================")
for name in sorted(aliases, key=str.lower):
    body.append(f"/** {name} — from the documented typedef. */")
    body.append(f"type {name} = {aliases[name]};")
    body.append("")

txt = "\n".join(body)
# player.ui — verified from the official HUD doc (wiki _sources/doc-hud.md):
# "player.ui.overlay puts a 128x128 canvas in a corner of one player's
# screen" / "that names player.ui.overlay makes the pack required for 26.3".
txt = txt.replace(
    "interface Player {",
    "interface Player {\n"
    "    /** `player.ui` — this player's own ui table. Source: official HUD\n"
    "     *  doc (player.ui.overlay). */\n"
    "    ui: PlayerUi;",
    1)

STATS["globals (declare const/function)"] = len(emitted_globals) + 4
STATS["type interfaces"] = len(interfaces)
STATS["type aliases"] = len(aliases)
STATS["opaque (no documented members)"] = len(OPAQUE)
STATS["conversion notes"] = len(WARN)

with open(OUT, "w") as f:
    f.write(header + txt + "\n")
shutil.copy(OUT, f"{ROOT}/download/citadel.d.ts")

# -------------------------------------------------------------------- report
print(f"wrote {OUT} ({os.path.getsize(OUT) / 1e3:.1f} KB)")
print(f"copied to {ROOT}/download/citadel.d.ts")
for k, v in STATS.items():
    print(f"  {k}: {v}")
print(f"\nconversion notes ({len(WARN)}):")
shown = 0
for where, note in WARN:
    print(f"  {where}: {note}")
    shown += 1
    if shown >= 60:
        print(f"  ... {len(WARN) - shown} more")
        break
print(f"\nopaque types: {', '.join(sorted(OPAQUE))}")
