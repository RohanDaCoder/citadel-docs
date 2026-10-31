#!/usr/bin/env python3
"""Check every require("<path>") in the pack resolves to a real .luau
file, and flag any top-level require cycles (lazy requires inside
functions are the sanctioned cycle-breaker)."""
import re
import sys
from pathlib import Path

ROOT = Path("/home/z/my-project/scripts/onixmg_citadel/pack")
REQUIRE = re.compile(r'require\("([^"]+)"\)')
FUNC_BODY = re.compile(r"\bfunction\b")  # rough: requires after this line may be lazy

files = sorted(ROOT.rglob("*.luau"))
rel = {str(f.relative_to(ROOT)) for f in files}

errors = []
graph = {}  # file -> set of top-level requires
for f in files:
    r = str(f.relative_to(ROOT))
    lines = f.read_text(encoding="utf-8").splitlines()
    deps = set()
    lazy = set()
    depth = 0  # block depth of top level (0 = top level)
    # a line is top-level when it has no leading whitespace and is not
    # inside a function; approximate with indentation + function tracking
    inside = 0
    for line in lines:
        stripped = line.strip()
        for m in REQUIRE.finditer(line):
            target = m.group(1) + ".luau"
            if target not in rel:
                errors.append(f"{r}: require(\"{m.group(1)}\") -> no such file")
            elif inside == 0:
                deps.add(target)
            else:
                lazy.add(target)
        # crude block tracking: function/do/then open, end closes
        if inside == 0:
            if re.match(r"^(local\s+)?function\b", stripped) or stripped.endswith("do") or stripped.endswith("then"):
                inside = 1
        else:
            if re.match(r"^(local\s+)?function\b", stripped) or stripped.endswith("do") or stripped.endswith("then"):
                inside += 1
            if re.match(r"^end\b", stripped):
                inside -= 1
    graph[r] = deps

# top-level cycle detection (DFS)
def find_cycle(start):
    stack, seen = [start], set()
    path = []
    def dfs(node):
        path.append(node)
        for dep in sorted(graph.get(node, ())):
            if dep == start:
                return path + [dep]
            if dep not in seen:
                seen.add(dep)
                r = dfs(dep)
                if r:
                    return r
        path.pop()
        return None
    return dfs(start)

cycles = []
for f in sorted(graph):
    c = find_cycle(f)
    if c:
        cycles.append(" -> ".join(c))

print(f"files: {len(files)}")
print(f"require errors: {len(errors)}")
for e in errors:
    print("  " + e)
print(f"top-level cycles: {len(cycles)}")
for c in cycles:
    print("  " + c)
sys.exit(1 if errors or cycles else 0)
