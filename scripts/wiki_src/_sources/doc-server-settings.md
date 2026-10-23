# SOURCE: Server settings

```yaml
# citadel.yml
mode: lite              # "full" = Citadel plays the game, "lite" = the packs are the game
packs: packs            # where the packs are, relative to this folder
bind:                   # what to listen on; each line left out is this default
  java: 0.0.0.0:25565
  packs: 0.0.0.0:25566  # resource packs over HTTP; give a second server on one machine its own
  bedrock: 0.0.0.0:19132    # Bedrock over RakNet (UDP); "" turns it off
  nethernet: 0.0.0.0:19132  # Bedrock over NetherNet (TCP signaling, the same number as RakNet on UDP); "" turns it off
game: a0.1.0            # the game version, "1.8.9" (the default) or "a0.1.0"
world_dir: worlds/a0    # the world folder; a world keeps the game it was written by
operators:              # players with every permission, by uuid (Minefort writes the owner here)
  - 069a79f4-44e9-4726-a5be-fca90e38aaf5
online_mode: true       # check each player with Mojang, as vanilla does; this is the default
nethernet_tls:          # the certificate for Bedrock clients that dial HTTPS; not used behind a proxy with a forwarding secret
  cert: fullchain.pem
  key: privkey.pem
store_dir: data/store   # where `stores` keeps its files when no platform store was named; this is the default
```
A player’s identity comes from one of three places:
- Behind a proxy with `MODERN_FORWARDING_SECRET`: the proxy signs it.
- No proxy, `online_mode: true`: Citadel checks with Mojang.
- `online_mode: false`: nobody is checked, and the log warns at start.
Anyone can join with any name, an operator’s too.
Every key is optional, and so is the file. With no `packs` key, a `packs`
folder beside the world is used when one exists. An unknown key or mode
stops the server.
The mode is decided in this order:
1. a `--full` or `--lite` flag
2. this file
3. what the packs agree on in their own manifests
4. survival, when there are no packs.
## World
`world` says where a chunk comes from.
- `world = "script"`: `world.on_generate` makes the chunks. A chunk it does
not fill is air.
- `world = "overworld"`: Citadel’s terrain, with biomes, hills, caves, ores,
trees and sea level 63. Scripts only add to it (`world.on_populate`).
`seed` pins the map.
- `world = "hub"`: any other name is a world folder in the pack,
`<pack>/hub`, made once from a build or a vanilla world. The server reads
it chunk by chunk and saves player changes into it. A chunk the folder
lacks comes from `world.on_generate`, or is air.
`citadel import builds/lobby.schem <pack>/hub --at -186,48,-236 --spawn 0.5,65,0.5
`
Generate a map too big to make live into that folder ahead of time, with
the pack’s `world.on_generate`:
`citadel generate <pack> --from -4096,-6144 --to 4095,6143 # block corners; --threads n
`
It runs one script per core, and any map size fits in memory. Chunks
already in the folder are kept, so a stopped run continues.
`parts.define` declares a named part whose generator runs on request.
Build mode edits the folder by hand (see “Named parts”).
`citadel generate <pack> --part tower-3 # one part's generator, into the folder
citadel parts <pack> # every part: clean, modified, kept or orphaned, and who edited it
`
- **no `world` key**: the scripts are asked first. A chunk no script filled
is overworld terrain on a full server and air on a lite server.
**Chunks nobody is near are unloaded.** Every ten seconds the server drops
chunks beyond the view distance of all players and entities. When someone
returns, a stored world loads the chunk from disk (a changed chunk waits for
its save). A `script` world calls `on_generate` again.
So **`on_generate` must make the same blocks every time**. Draw from a hash
of the position, never `math.random`. A script-world chunk changed live
(`world.set_block`, `world.fill`) stays in memory.
**Where the world is.** A full server keeps its world in `world/`, beside
the server’s `citadel.yml`, with or without packs: the world is the
server’s, and a pack that is removed does not take the map with it. A lite
server keeps it in the first pack, `<pack>/data/world`. A dimension is a
folder beside the main world (`world_dungeon`). `world_dir` in the server’s
`citadel.yml` names another place.
The world’s `level.json` keeps the seed, spawn, time and weather of the first
run. Changing `seed` does nothing to an existing world. Delete the world
folder for a new map.
With no `spawn_point`, a `world: overworld` pack takes the first grass block above
sea level, ring by ring out from (0, 0). It searches once and stores the
result in `level.json`. With no `world` key, the spawn is the origin.
The chunks around the spawn are generated before the port opens.
## Terrain
`terrain` sets the overworld’s step list. Only `game: a0.1.0` has one.
Without `terrain`, the world uses the original game’s steps.
```yaml
game: a0.1.0
world: overworld
terrain:
  snow: true              # Alpha's snowy world: a frozen sea, snow on every open column
  steps:                  # the whole populate list, in order, in place of the jar's
    - { step: dungeons, count: 8 }
    - { step: clay, block: clay, size: 32, count: 10 }
    - { step: ore, block: coal_ore, size: 16, count: 20, below: 128 }
    - { step: ore, block: diamond_ore, size: 7, count: 4, below: 16 }   # four times the jar's
    - { step: trees, bonus: 10, big: 10 }
    - { step: patch, block: dandelion, count: 2 }
    - { step: patch, block: poppy, count: 1, chance: 2 }
    - { step: reeds, count: 10 }
    - { step: cactus, count: 1 }
    - { step: springs, fluid: water, count: 50, bound: 120, nesting: 1 }
    - { step: springs, fluid: lava, count: 20, bound: 112, nesting: 2 }
    - { step: snow }
```
| step | what it places |
| --- | --- |
| `dungeons` | `count` tries at a cobblestone room with a spawner and up to two chests |
| `clay` | `count` blobs of `block`, `size` long, into sand that starts under water |
| `ore` | `count` veins of `block`, `size` long, into stone below y `below` |
| `trees` | trees on the surface; one chunk in `bonus` gets one more, one in `big` grows big trees |
| `patch` | a patch of 64 tries at `block` — `count` times, or with `chance: n` one time in n |
| `reeds` | `count` clumps of sugar cane beside water |
| `cactus` | `count` clumps of cactus on sand |
| `springs` | `count` fluid sources in stone walls; `nesting` pushes them deeper |
| `snow` | a snow layer on every open column — in a `snow: true` world only |
`game.terrain` prints the original list. Start an edit from it.
- Order matters: moving or removing a step changes everything after it.
- A block must be one the game can name.
- A size or a bound must be at least 1.
- An unknown key stops the server.
- The list is stored in `level.json`. Like `seed`, a later edit changes
nothing for an existing world.
- `terrain` on a 1.8.9 world stops the server.
