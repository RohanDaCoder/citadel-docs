---
title: "Zones and raycasts"
url: /docs/citadel/zones-and-raycasts
---

# Zones and raycasts

```luau
local goal = world.zone{ from = vec3(10, 64, 10), to = vec3(14, 66, 14),
    on_enter = function(player) message(player.name .. " scored", colors.lime) end,
    on_leave = function(player) end }
goal:contains(player)                -- boolean
goal:players()                       -- who is in it now
goal:destroy()

players.near(pos, 8)                 -- every player within eight blocks of a point
players.within(from, to)             -- every player inside a box of blocks, corners included

world.raycast(from, direction, 32)   -- the first block a ray meets within 32 blocks, or nil:
--   { block = vec3, face = "up" | "down" | "north" | "south" | "west" | "east" }
world.raycast(player.at + vec3(0, 1.62, 0), player:look())   -- what the player is looking at

world.sees(from, to)                 -- true when no block stops the line between the two points
world.raycasts(rays, out, n)         -- n lines at once, in buffers; see below
local block, sky, open = world.light_at(pos)   -- block light 0..15, sky light 0..15, open sky
world.path(from, to, { size = { 0.6, 1.95 } })  -- the points a body walks, a list of vec3, or nil

```
- `world.sees` and `world.raycasts` look as a mob looks: a block with a
collision box stops the line, glass and leaves too. Water, lava, grass and
flowers do not.
- `world.raycasts(rays, out, n)`: `rays` is a buffer with six f64 for each
line: from x, y, z, then to x, y, z. `out` gets one f64 for each line: how
far from `from` the first block is that stops it, or -1 when the line is
clear. One call for all the bodies of an `on_think` is much cheaper than one
call each.
- `world.light_at(pos)` gives three values: the block light, the sky light,
and `true` when no block above stops the sky.
- `world.path(from, to, opts)` is the game’s own search for a mob: four ways
from each block, a step up of one block, a fall of at most `fall` blocks. It
gives the middle of each block to walk on, from `from` to the block at `to`.
The options: `size` (a number, or `{ width, height }`; 0.6 by 1.8),
`swim = true` to go through water, `fall` (3), `range` (how far it may go
from the goal; the distance plus 16), `budget` (the most blocks it looks at;
2000). A search that stops early gives the part that came closest. `nil`
when it found no step at all.
- A path costs the pack, not the tick. A short one costs some microseconds; a
long one around a big wall costs more. Ask for a new one when the old one is
old, not each think.
- `from` and `to` are block positions, in either order. Both corners are
inside.
- A player is inside when their feet are.
- Disconnecting inside a zone runs `on_leave`.
- A zone ends with the script.
