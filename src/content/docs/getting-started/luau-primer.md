---
title: 'Luau primer'
description: 'The Luau language in one page, for developers coming from JavaScript, Python or Java — syntax, tables as objects, types, strict mode, and the parts of standard Lua that Citadel leaves out.'
---

:::note[In short]
Citadel packs are written in **Luau**, Roblox's typed dialect of
Lua 5.1. If you know JavaScript the shape will look familiar: first-class
functions, tables used as objects and arrays, closures everywhere. This page
covers the syntax you will meet in every Citadel example, plus the standard
library that is and is not there.
:::

## Values and syntax essentials

```luau
-- Comments start with --. Block comments: --[[ ... ]]

local n = 42                  -- numbers: doubles
local s = "double or 'single' quotes"
local b = true                -- true / false / nil (nil is "absent")
local pos = vec3(1, 2, 3)     -- engine values are plain calls

-- ~= is "not equal"; .. concatenates strings
if n ~= 0 and s ~= "" then print("no") end

-- Blocks close with keywords, not braces:
for i = 1, 10 do end          -- inclusive range
for i = 10, 1, -1 do end      -- with a step
while b do break end          -- break exists; continue exists in Luau
repeat local x = 1 until x == 1
```

The `if` **expression** — Luau's ternary:

```luau
local block = if mix(x, 0, z) < 0.3 then "mossy_cobblestone" else "cobblestone"
```

## Tables are the one data structure

There are no classes and no arrays — tables do both jobs:

```luau
local list = { "red", "green", "blue" }   -- 1-indexed arrays
list[1] == "red"                           -- arrays start at ONE

local opts = {                             -- dictionaries (string keys)
    count = 40,
    spread = 2,
    color = colors.red,                    -- trailing comma allowed
}

local nested = {                           -- nested tables build any shape
    from = vec3(0, 64, 0),
    to = vec3(8, 70, 8),
    on_enter = function(player) end,
}
```

Table keys with dots, array indexes with brackets. Functions are values:
stored in tables, passed as arguments — that is how every `on_*` callback in
the API works.

```luau
local function greet(name) return "hi " .. name end
world.on_generate(function(chunk)          -- anonymous function argument
    chunk:fill(chunk.min, chunk.max, "stone")
end)
```

The colon `chunk:fill(...)` is method-call syntax — it passes `chunk` itself as
a hidden first argument. That is why the API reads `player:teleport(pos)` for
methods but `players.list()` for plain functions.

## Types and `--!strict`

Luau has an optional type system. Put `--!strict` at the top of every file —
with Citadel's definitions file it type-checks the entire API (see
[Tooling](/getting-started/tooling/)):

```luau
--!strict

local count: number = 0
local function total(prices: { number }): number
    local sum = 0
    for _, p in prices do sum += p end     -- += exists in Luau
    return sum
end

-- Optional values carry ?: a nil is allowed
local function find(id: string): Player?
    return nil
end

-- String unions read like the docs write them
local face: "north" | "south" | "east" | "west" = "north"

-- Table types, as the API's options tables are typed
local opts: { count: number?, spread: number? } = { count = 3 }
```

Compound assignments (`+=`, `-=`, `..=`), string interpolation with backticks
(`` `hi {name}` `), and generalized iteration (`for _, v in table do` without
`pairs`/`ipairs`) are Luau additions you will see throughout the samples.

## What is *not* there

Citadel's Luau is sandboxed to the pack, and a few Lua/Roblox staples are
deliberately absent:

- `loadstring` is not there — a pack cannot run text as code. `require` reads
  only files **inside the pack**.
- `getfenv` and `setfenv` are not there.
- There is no `os` / `io` access: files, time and network all go through the
  engine's own globals (`storage`, `stores`, `http`, `time`).

`require` resolves from the pack root, caches by canonical file path, rejects
cycles, and rejects symlinks that lead outside the pack. A module returning
`nil` is cached as `true`. Details in [Runtime](/concepts/runtime/).

## Patterns you will see in every pack

Event subscription with cancellation:

```luau
local conn = players.on_click(function(player, hit) end)
conn:cancel()          -- stop the subscription
```

Options tables instead of long argument lists (calls with more than three
inputs take an options table, and **an unknown field is an error**):

```luau
fx.particle("dust", pos, { count = 40, spread = 2, color = colors.lime })
```

`nil` vs `false` for optional overrides — a distinction the whole API uses
(see [Conventions](/concepts/conventions/#nil-false-and-true)):

```luau
player.visible = false    -- hidden from everyone
player.visible = nil      -- back to the default (visible)
```

## See also

- [Conventions](/concepts/conventions/) — the API's rules for options, colours,
  positions and text.
- [Tooling](/getting-started/tooling/) — `luau-lsp` and the definitions file.
- [The event model](/concepts/events/) — callbacks, connections, asks.
