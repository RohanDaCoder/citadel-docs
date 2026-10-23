---
title: "Named parts"
url: /docs/citadel/named-parts
---

# Named parts

```luau
parts.define {
    name = "tower-3",                  -- unique; a path, "downtown/tower-3", nests
    at = vec3(56, 64, 15),             -- where the build's block (0, 0, 0) lands
    detail = 1,                        -- as world.build: 1, or 2 for half blocks
    build = function(b) ... end,       -- exactly a world.build function
}

```
The rules:
- **Nothing runs on load.** `parts.define` only declares the part. A
generator runs on request (`citadel generate`, or `/part generate` in build
mode) or when its code changes. A server boots the stored world and runs no
generator.
- Each word of a name is 1 to 64 letters, digits, `-`, `_` and `.`.
- A duplicate name is an error that names the file of the first definition.
- A part is its whole box, air included. Writing it again clears what the old
box held outside the new box.
- `citadel render` and `citadel check` frame the `b:part`s inside a part by
path, for example `"tower-3/roof"`.
- On a `world: script` pack, `parts.define` logs that parts need a world
folder, and generates nothing.
Each part is in one of four states, kept in `<world>/parts.json`:
| state | means | when its code changes |
| --- | --- | --- |
| **clean** | the box holds exactly what its generator last wrote | written again, by itself |
| **modified** | somebody edited blocks in it since | left alone, and reported: “its code changed” |
| **kept** | somebody chose its blocks: they are in `parts/<name>.schem` in the pack | ignored: the generator no longer owns it |
| **orphaned** | its definition is gone from the pack | reported: keep it, or regenerate it to remove its blocks |
```json
{ "tower-3": {
    "state": "modified",
    "region": [[48, 64, 4], [64, 119, 26]],
    "module": "city.luau",
    "generated": "sha256:…",
    "at": "2026-09-27T14:02:11Z",
    "edits": { "count": 214, "by": { "melvin": 200, "agent:claude": 14 } }
} }

```
**Only people and the agent make edits, never scripts.**
- An edit in build mode counts under the player’s name. An agent edit counts
under `agent:<client>`.
- Either kind makes a clean part modified.
- Blocks your script writes are not edits: `world.set_block` from a callback,
a door it opens, a display, a ride.
- `citadel parts` and `/part` confirm the state against the `generated` hash.
A modified part with every edit undone is clean again.
**You regenerate or keep a whole part.** Hand edits never merge into new
code.
- `regenerate` clears the part and runs its generator. On an orphan, it
removes the blocks.
- `keep` saves the blocks to `parts/<name>.schem` as Sponge v3, the format
`world.schematic` reads. Generating a kept part pastes that file.
- `release` deletes the file and regenerates the part.
**When the code changes.** Saving a `.luau` file reloads the pack. Parts
defined **in that file** then act as the table says.
- A clean part is written again through the tick. Unchanged blocks are
skipped.
- On start, files changed while the server was down count too.
- A change to a module that a part `require`s re-runs nothing.
**Nested and overlapping parts.** A block belongs to the innermost part whose
box holds it.
- Writing a parent leaves its nested parts alone.
- An edit inside a nested part counts against it, not its parent.
- Where parts overlap without nesting, an edit counts against each.
`citadel check` warns (`PART_OVERLAP`): regenerating one rewrites the other.
From the command line, on the world folder:
```sh
citadel generate <pack> --part tower-3      # run one generator into the world; --parts runs every one
citadel parts <pack>                        # every part: state, region, module, edits and who; --json
citadel regenerate <pack> --part tower-3 [--yes] [--render before.png]
citadel keep <pack> --part tower-3          # its blocks become parts/tower-3.schem
citadel release <pack> --part tower-3       # a kept part goes back to its generator

```
- `generate` makes the world folder if it is missing. It writes new and clean
parts, pastes kept parts from their files, and refuses modified parts.
- `regenerate` of a part with hand edits needs `--yes`. Without it, it writes
nothing and says how many blocks of whose edits it would overwrite.
- `--render file.png` writes `file-before.png` and `file-after.png`.
- Stop any server running the pack first, or use `/part` in the game.
- `citadel check` and `citadel render` read the world folder with its hand
edits. The check report has a “part states” section: states, edits,
authors, and code changes.
## Build mode
Build mode works only on a development copy (`citadel.env` is
`"development"`), never on a live instance. A player with the `citadel.build`
permission builds by hand. Every operator has it.
```
/build                          creative and flight, and your clicks change the world; again to stop
/build wand                     the wooden axe: left click the first corner, right click the second
/build pos1, /build pos2        a corner where you stand
/build fill <block>             the selection, filled
/build replace <from> <to>      one block for another in the selection
/build copy                     the selection, held from where you stand
/build paste                    the clipboard, the same way round you as it was copied
/build rotate <90|180|270>      the clipboard, turned about where you stood
/build mirror <x|z>             the clipboard, flipped
/build undo                     your last edit, taken back
/part                           the part you look at: its state, its region, who edited it
/part <name>, /part list        one part by name; every part
/part generate <name>           run a part's generator
/part regenerate [name] [confirm]   throw its hand edits away; asks for "confirm" when there are some
/part keep [name]               its blocks become parts/<name>.schem
/part release [name]            a kept part back to its generator
/part outline                   every part's box nearby, 15 seconds: green clean, amber modified, blue kept, red orphaned

```
- Every block a builder changes, undo included, is an edit under their name.
- Outside build mode, a click on a pack server changes no blocks.
- A place puts the held item’s block, facing as in the game. A pack’s
own block item places the pack’s block.
- Undo is per player, 64 edits deep. One command is one edit of at most one
million blocks.
- Rotate and mirror turn facings, axes and shapes, as `build:rotate` and
`build:mirror` do.
- The outline is particles for the asking player only, on clients from 1.7.
