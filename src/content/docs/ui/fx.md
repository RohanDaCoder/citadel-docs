---
title: 'Particles and lasers'
description: 'fx.particle — particles at points, one call or many, with count, spread, velocity, speed and dust colour and size — and the beam pattern: dust along a line, redrawn every other tick, tweenable into a laser.'
---

:::note[In short]
particles at points: a burst, a trail, or a laser drawn as a
line of dust. One call, [`fx.particle`](/ref/Fx/particle/), serves a room — a
name, a point or a list of points, and an options table. Dust alone takes a
colour and a size, which is what a beam or laser is made of. Particles fade
on their own, so a beam that stays is redrawn every other tick.
:::

## The call

Particles live on the `fx` global — Minecraft's particle packet, for a room
(`fx`, or `room.fx` in another room):

```luau
fx.particle(name, pos, { count = 1, spread = 0, velocity = nil, speed = 0, color = nil, size = 1 })
```

| Option     | Default | What it is                                                                                |
| ---------- | ------- | ----------------------------------------------------------------------------------------- |
| `count`    | 1       | Particles at each point                                                                   |
| `spread`   | 0       | A random box this many blocks out from each point; a number or a vec3 (one size per axis) |
| `velocity` | nil     | A vec3: one particle that moves along it                                                  |
| `speed`    | 0       | With `velocity`, scales it (1); without it, how fast the particles scatter — 0 is still   |
| `color`    | nil     | `dust` only                                                                               |
| `size`     | 1       | `dust` only, 0.5 to 4                                                                     |

`name` is the particle: `dust`, `end_rod`, `explosion`, `firework`, `flame`,
`note` or `totem_of_undying`. Any other name sends nothing.

## Points and who sees them

`pos` is a vec3, or a list of vec3s, with the same particle at every point.
Each point is sent only to players in the same room within 64 blocks of its
origin in 3D, including the boundary, before spread or velocity.

## Velocity against count and spread

- `count` particles appear at each point, in a random box `spread` blocks out
  from it.
- `velocity` (a vec3) sends one particle that moves along it. It cannot go with
  `count` above 1 or with `spread`.
- `color` and `size` (0.5 to 4) are for `dust` only. Dust is white and size 1
  unless they say.

:::caution[Gotcha]
`color` or `size` on any other particle is an error.
:::

## Version behaviour

- A client whose version lacks a particle does not get it.
- Before 1.13, dust is one particle a point, in its colour, with no count,
  spread or size.
- 1.7 shows dust only.

## Beams

Dust at points along a line, in one call:

```luau
-- a beam: dust at points along a line, in one call
local points = {}
for i = 0, 7 do points[i + 1] = from:lerp(to, i / 7) end
fx.particle("dust", points, { color = colors.red, size = 1.5 })

fx.particle("flame", pos, { velocity = vec3(0, 1, 0), speed = 0.5 })        -- a jet
fx.particle("firework", pos, { count = 40, spread = 2, speed = 0.05 })       -- a burst
fx.particle("totem_of_undying", at + vec3(0.5, 0.5, 0.5), { count = 12, spread = 0.4, speed = 0.3 })   -- a pickup burst
```

Particles fade on their own. A beam that stays is drawn again every other tick:

```luau
local beam = { from = vec3(0.5, 76, 0.5), to = vec3(0.5, 66, 0.5), color = colors.cyan }
local conn = time.on_tick(function(tick)
    if tick % 2 ~= 0 then return end
    local points = {}
    for i = 0, 7 do points[i + 1] = beam.from:lerp(beam.to, i / 7) end
    fx.particle("dust", points, { color = beam.color, size = 2 })
end)
tween(beam, { to = beam.to + vec3(4, 0, 0) }, { duration = 1 })   -- its fields are plain; set or tween them
conn:cancel()                                                     -- and it is gone
```

The beam's fields are plain values: set or tween them (a laser that sweeps),
and `conn:cancel()` takes the beam away.

## See also

- [Sound](/ui/sound/) — the other room-wide effect, `sound.play` and streams.
- [UI basics](/ui/ui-basics/) — colour spellings for `color`.
- [Client versions](/appendix/client-versions/) — what old clients get.
- [Coin rush guide](/guides/guide-coin-rush/) — pickup particles in a working pack.
