---
title: "Particles and lasers"
url: /docs/citadel/particles-and-lasers
---

# Particles and lasers

```luau
fx.particle(name, pos, { count = 1, spread = 0, velocity = nil, speed = 0, color = nil, size = 1 })

```
- `name` is the particle: `dust`, `end_rod`, `explosion`, `firework`,
`flame`, `note` or `totem_of_undying`. Any other name sends nothing.
- `pos` is a vec3, or a list of vec3s, with the same particle at every point.
Each point is sent only to players in the same room within 64 blocks of
its origin in 3D, including the boundary, before spread or velocity.
- `count` particles appear at each point, in a random box `spread` blocks
out from it. `spread` is a number or a vec3 (one size per axis).
- `velocity` (a vec3) sends one particle that moves along it. It cannot go
with `count` above 1 or with `spread`. `speed` scales it and is 1 with a
velocity.
- Without `velocity`, `speed` is how fast the particles scatter. 0 is still.
- `color` and `size` (0.5 to 4) are for `dust` only. Dust is white and size
1 unless they say. On any other particle they are an error.
- A client whose version lacks a particle does not get it. Before 1.13,
dust is one particle a point, in its colour, with no count, spread or
size. 1.7 shows dust only.
```luau
-- a beam: dust at points along a line, in one call
local points = {}
for i = 0, 7 do points[i + 1] = from:lerp(to, i / 7) end
fx.particle("dust", points, { color = colors.red, size = 1.5 })

fx.particle("flame", pos, { velocity = vec3(0, 1, 0), speed = 0.5 })        -- a jet
fx.particle("firework", pos, { count = 40, spread = 2, speed = 0.05 })       -- a burst

```
Particles fade on their own. A beam that stays is drawn again every other
tick:
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
