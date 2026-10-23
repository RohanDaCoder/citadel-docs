---
title: Tooling
section: getting-started
order: 3
description: Set up luau-lsp with Citadel's type definitions for autocomplete and strict type checking, and use the citadel CLI to run, check, generate and render packs.
tags: [luau-lsp, types, cli, vscode, tooling]
---
# Tooling

> **In short:** Citadel ships a full type-definitions file, `packs/citadel.d.luau`.
> Point Luau's language server at it and you get autocomplete, signatures and
> strict type checking across the whole API. The `citadel` CLI runs the server,
> analyzes packs, generates world folders and renders builds to images.

## The type definitions file

`packs/citadel.d.luau` types this whole API. Start every script with
`--!strict` and point a language server at that file: misspelt fields, wrong
argument types and unknown options become squiggles before you run anything.

> **Gotcha:** use the standard platform and Luau's **new type solver**
> (luau-lsp 1.70.1 or later). The old solver misresolves several of the API's
> table types.

## Command-line type check

```sh
luau-lsp analyze --platform=standard --flag:LuauSolverV2=true \
  --definitions=packs/citadel.d.luau main.luau
```

Run this in CI or before you ship; it catches the same errors the editor does.

## VS Code setup

With the `luau-lsp` extension installed, set in `.vscode/settings.json`:

```json
{
  "luau-lsp.platform.type": "standard",
  "luau-lsp.types.definitionFiles": ["packs/citadel.d.luau"],
  "luau-lsp.fflags.override": { "LuauSolverV2": "true" }
}
```

## The `citadel` CLI

| Command | What it does |
| --- | --- |
| `citadel --lite --pack ./first` | Run a lite server with one pack. `--full` (or no flag) runs survival. |
| `citadel --packs-dir ./packs` | Run with every pack in a folder. |
| `luau-lsp analyze ...` (above) | Type-check a pack's scripts. |
| `citadel check <pack>` | Frame-check a build: says which named part an edit touched. |
| `citadel render` | Render a build (or one named part) to an image. |
| `citadel generate <pack> --from -4096,-6144 --to 4095,6143` | Pre-generate a world folder from the pack's `world.on_generate`, one script per core; a stopped run continues where it left off. `--threads n` caps cores. |
| `citadel generate <pack> --part tower-3` | Run one named part's generator into the world folder. |
| `citadel parts <pack>` | List every named part: clean, modified, kept or orphaned, and who edited it. |
| `citadel import builds/lobby.schem <pack>/hub --at -186,48,-236 --spawn 0.5,65,0.5` | Import a `.schem` (Sponge or MCEdit) or a vanilla world as a pack's world folder. |

Details on world folders, named parts and build mode are in
[Pack anatomy](/wiki/pack-anatomy) and [Building](/wiki/building).

## Build mode

`/build` and `/part` exist on `citadel.env == "development"` only — the
Minefort workload where an experience is built. They edit a pack's world folder
by hand and mark named parts as modified. See
[Named parts](/wiki/building#named-parts).

## Knowing where your script runs

```luau
print(citadel.version)  -- the engine build, e.g. "0.1.0"
print(citadel.game)     -- the game version from citadel.yml, e.g. "1.8.9"
print(citadel.env)      -- "development", "unlisted" or "published"
```

`citadel.env` is:

- `"development"` on the Minefort workload where an experience is built.
- `"unlisted"` or `"published"` on an experience's instances, by visibility.
- `"published"` on a Minefort server that is not an experience.
- `"development"` anywhere else (including local runs).

Gate debug tools on it:

```luau
if citadel.env == "development" then
    -- builder-only commands, verbose logs, ...
end
```

## Logging

`citadel.log(...)` writes its arguments to the server log under this pack's
name — the one logging call a script has. Errors in callbacks are logged with
file and line automatically.

## See also

- [Pack anatomy](/wiki/pack-anatomy) — the manifest and the folders around it.
- [Luau primer](/wiki/luau-primer) — the language, if Lua is new to you.
- [Limits](/wiki/limits) — what `citadel.budget()` reports and what happens
  when a pack runs long.
