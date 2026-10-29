# SOURCE: Packs

The script runs on every Java client from 1.8 to 26.2 and never sees a
client version. To check a feature, ask `player:supports` (see “Client
versions”).
`packs/citadel.d.luau` types this whole API. Start a script with `--!strict`
and point a language server at that file to catch misspelt fields.
Use the standard platform and Luau’s new type solver (luau-lsp 1.70.1 or
later). For a command-line check:
```sh
luau-lsp analyze --platform=standard --flag:LuauSolverV2=true --definitions=packs/citadel.d.luau main.luau
```
In VS Code, set `luau-lsp.platform.type` to `standard`, add the definitions
file to `luau-lsp.types.definitionFiles`, and set
`luau-lsp.fflags.override` to `{ "LuauSolverV2": "true" }`.
```yaml
name: rave    # also the sound namespace: assets/sounds/kick.ogg -> "rave.kick"
entry: main.luau
motd: Rave by Minefort
spawn_point: [0.5, 65.0, -4.5]
gamemode: 1    # 0 survival, 1 creative, 2 adventure, 3 spectator
game: "1.8.9"    # the content and rules the server simulates; clients older than it are refused
min_client: "1.14"    # refuse clients older than this too (optional; the strictest pack wins)
resource_pack: offered    # or "required": a client that turns the pack down cannot join (1.17+ clients)
mode: lite    # what server this pack is for: "lite" = your scripts are the game, "full" = it adds to survival; left out, the pack runs on either
world: script    # "script" = world.on_generate below, "overworld" = the built-in terrain, "hub" = the world folder <pack>/hub that `citadel import` wrote
seed: 1234    # the overworld map; left out, a new world rolls its own
terrain: { snow: true }    # what an a0.1.0 overworld is made of; see "terrain" below
budget_ms: 2    # this pack's share of a tick, for its tick and event callbacks
view_distance: 12    # chunks sent round each player, 2..32; the farthest pack wins, 6 if none asks
mute: [block.stone.hit]    # vanilla sounds nobody on this server hears (the resource pack plays silence for them)
hide_hud: [hearts, food]    # parts of the game's own HUD nobody on this server sees; see "Layouts"
dialogs: true    # the pack opens dialogs: what they draw with rides in the resource pack; see "Dialogs"
```
Run it: `citadel --lite --pack ./rave`.
## Loading
- The entry script has **5 s** of work between two waits (`task.wait`), and
30 s in all. Past that, the load fails and the log says why.
- Build big scenery once at load and copy it, for example one tree variant
pasted per chunk. Do not loop over every block of every level at load.
## Textures of your own
On Java 1.21.4 and later, a pack’s own items and blocks can have textures.
Set `texture` in `game.items.define` and `game.blocks.define` (below). The
engine adds them to its resource pack. Older clients see the vanilla item or
block. A client that turns the resource pack down sees them too from then on
(`player:supports("resource_pack")` is false). A pack that needs the textures
says so:
```yaml
min_client: "1.21.4"    # the oldest client that draws a pack's own textures
resource_pack: required    # a client that turns the pack down cannot join
```
Every other folder in `<pack>/assets/` (not `sounds`) goes into the resource
pack unchanged (`assets/<pack>/textures/...`).
## Mode
`mode` says **who owns the game**. In a pack manifest, it names the kind of
server the pack is *for*.
- `mode: lite`: your scripts are the game.
- `mode: full`: **Citadel plays survival** (terrain, health, hunger, mining,
inventory, mobs, world rules). A pack cannot ship survival; it *adds* to
it (a shop, a scoreboard, a custom drop).
- **no `mode` key**: the pack runs on either kind of server, like a plugin.
`citadel` with no flags (or `--full`) runs survival with `gamemode: 0` and
the overworld. `--lite` makes the packs own the game. Add packs to either
with `--pack ./shop` or `--packs-dir ./packs`.
- A `--lite` server with no packs does not start survival. It runs with an
empty world and no game, and the log says so. Add a pack and restart.
- With no flag and no server file, the packs’ manifests decide. Packs that
name different modes, or that all name none, stop the server. The message
says how to set one.
- A flag or the server file overrules a pack that names the other mode. The
log names that pack.
