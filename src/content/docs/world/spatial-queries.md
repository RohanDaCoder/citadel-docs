---
title: 'Zones, raycasts and paths'
description: 'Querying space — trigger zones with on_enter/on_leave, single and batched raycasts, line-of-sight checks, the mob pathfinder, light at a position, and nearby-player queries.'
---

:::note[In short]
the world answers three kinds of spatial question. **Zones**
watch a box and tell you who entered. **Raycasts** ask what a line hits —
one at a time or a thousand in buffers. **`world.path`** asks how a mob
walks from A to B. Around them: `world.sees` for line-of-sight,
`world.light_at` for light, `players.near`/`players.within` for proximity.
:::

## Zones

```luau
local goal = world.zone{
    from = vec3(10, 64, 10), to = vec3(14, 66, 14),
    on_enter = function(player) message(player.name .. " scored", colors.lime) end,
    on_leave = function(player) end,
}
goal:contains(player)     -- boolean
goal:players()            -- who is in it now
goal:destroy()
```

The rules:

- `from` and `to` are block positions, in either order; both corners are
  inside.
- A player is inside when their **feet** are.
- Disconnecting inside a zone runs `on_leave`.
- A zone ends with the script — make it again on reload.

## Raycasts

```luau
world.raycast(from, direction, 32)   -- the first block a ray meets within 32 blocks, or nil:
--   { block = vec3, face = "up" | "down" | "north" | "south" | "west" | "east" }
world.raycast(player.at + vec3(0, 1.62, 0), player:look())   -- what the player is looking at
```

- Returns the block position and the face the ray came in through; `nil` for
  no hit.
- The ray starts at `from` and runs along `direction` up to `max` blocks.

`world.sees(from, to)` answers the binary question — true when no block stops
the line between the two points:

- It looks as a mob looks: a block with a **collision box** stops the line —
  glass and leaves too. Water, lava, grass and flowers do not.

## Batched raycasts

`world.raycasts(rays, out, n)` casts `n` lines at once, through buffers:

- `rays` is a buffer with **six f64 for each line**: from x, y, z, then to
  x, y, z.
- `out` gets **one f64 for each line**: how far from `from` the first
  stopping block is, or `-1` when the line is clear.

:::tip
one call for all the bodies of an `on_think` is much cheaper than
one `world.raycast` each. The same collision rules apply as `sees`.
:::

## Pathfinding

`world.path(from, to, opts)` is the game's own search for a mob:

```luau
local points = world.path(from, to, { size = { 0.6, 1.95 } })
-- the points a body walks, a list of vec3, or nil
```

| Option | Meaning | Default |
| --- | --- | --- |
| `size` | A number, or `{ width, height }` | 0.6 by 1.8 |
| `swim` | `true` to go through water | off |
| `fall` | The most blocks it may fall | 3 |
| `range` | How far it may go from the goal | the distance plus 16 |
| `budget` | The most blocks it looks at | 2000 |

- The search takes four ways from each block, a step up of one block, a fall
  of at most `fall` blocks. It gives the middle of each block to walk on,
  from `from` to the block at `to`.
- A search that stops early gives the part that came closest. `nil` when it
  found no step at all.
- A path costs the pack, not the tick: a short one costs microseconds; a long
  one around a big wall costs more. Ask for a new one when the old one is
  old, not each think.

## Light

```luau
local block, sky, open = world.light_at(pos)
-- block light 0..15, sky light 0..15, and true when no block above stops the sky
```

`world.light` is different — a client-side light *source* a pack places (see
[Displays](/ui/displays/)); `world.light_at` reads the real light of a
position.

## Who is near

```luau
players.near(pos, 8)       -- every player within eight blocks of a point
players.within(from, to)   -- every player inside a box of blocks, corners included
```

Both return handles you can use directly. For a watched area with callbacks,
use a zone; for a one-off check, use these.

## See also

- [Teleport pads](/cookbook/cookbook-teleport-pads/) — zones put to work.
- [Custom entities](/entities/custom-entities/) — `on_think`, where batched
  raycasts pay off.
- [Block reference](/world/block-reference/) — `world.light_at` in context.
