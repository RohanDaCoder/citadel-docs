---
title: "3D models"
url: /docs/citadel/3d-models
---

# 3D models

```luau
local car = models.new("car", function(m)
    local paint = m:material("paint", colors.red, { grain = 0.1 })   -- a colour a display may repaint
    local glass = m:material("glass", "dark_aqua", { alpha = 0.45 }) -- what is behind shows through
    local door = m:texture(30, 16, { tint = paint })                 -- drawn in greys, coloured by paint
    local grille = m:texture(8, 4)                  -- pixel art for one face, drawn as it is
    grille:fill(colors.black)
    grille:rect(1, 1, 6, 2, colors.gray)            -- x, y, w, h, colour
    grille:pixel(0, 0, colors.transparent)          -- a see-through pixel

    local body = m:part("body", { pivot = vec3(0, 6, 0) })
    body:box(vec3(0, 4, -20), vec3(8, 12, 20), paint, {
        faces = { north = grille },                 -- one side wears something else
    })
    local screen = body:part("windscreen")
    screen:box(vec3(0, 12, -6), vec3(8, 18, 2), glass, { rotation = vec3(22.5, 0, 0) })
    local wheel = body:part("wheel_front", { pivot = vec3(8, 4, -12) })
    wheel:box(vec3(6, 0, -16), vec3(10, 8, -8), paint)
    wheel:box(vec3(6, 0, -16), vec3(10, 8, -8), paint, { rotation = vec3(45, 0, 0) })
    body:mirror("x")                                -- the left half, from the right one

    m:animation("drive", {
        length = 1, loop = true,
        wheel_front = { rotation = { [0] = vec3(0, 0, 0), [0.25] = vec3(-90, 0, 0), [0.5] = vec3(-180, 0, 0),
            [0.75] = vec3(-270, 0, 0), [1] = vec3(-360, 0, 0) } },   -- quarter turns: see the rules
        wheel_front_mirrored = { rotation = { [0] = vec3(0, 0, 0), [0.25] = vec3(-90, 0, 0), [0.5] = vec3(-180, 0, 0),
            [0.75] = vec3(-270, 0, 0), [1] = vec3(-360, 0, 0) } },
    })
end)

local d = world.display{
    kind = "model", model = car,
    at = vec3(10.5, 65, 4.5), rotation = { yaw = 90 },      -- degrees, as every entity turns: 0 faces south, 90 west
    scale = 3.5,                             -- 1 draws it at 16 units to the block
    paint = { paint = colors.blue },         -- keys are material names
    fallback = "minecart",                   -- what a client that cannot show it sees; nil shows nothing
    seats = { vec3(0, 7, 2) },               -- optional: where riders sit, in model units; see "vehicles"
}
d:move(vec3(12.5, 65, 4.5), { yaw = 180 })   -- place and turn it in one step, every part together
d:move(at, { forward = forward, up = up })                      -- pointed: nose along forward, roof toward up (a car on a wall)
d.at, d.rotation                             -- live too; each write is a move of its own
d.scale = 2                                  -- live
d.paint = { paint = colors.red }             -- live
d:play("drive")                              -- from the beginning; an unknown name is an error
d:play("drive", { speed = 2 })               -- twice as fast; on the one already playing, the new speed at once
d:stop("drive")                              -- the parts stay where they are
d:destroy()

```
The rules:
- Make models while the pack loads. `models.new` in a callback is an error.
- `rotation.pitch` and `rotation.roll` tip the whole model about its
origin, with parts, animations and seats.
- A rider stays upright. For a car on a wall, hide the driver
(`invisibility`) and use `camera.fixed`.
- **16 units are one block.** The origin is the model’s bottom centre, `+y`
is up, and the front is `-z`.
- A box reaches `-24 .. 24` on every axis: three blocks. For a bigger thing,
set the display’s `scale`.
- `m:texture(w, h, { scroll = "up", speed = 2 })` is a texture that moves
when a block is drawn from the model. See “blocks drawn from a model”.
- A box turns on **one** axis only, in steps of 22.5 degrees, up to 45
either way. Anything else is an error. An octagonal wheel is two boxes,
one turned 45.
- Box corners go in any order and can be fractional. A box’s `pivot`
defaults to its centre.
- Every box is in a part; there is no `m:box`. A part turns around its
`pivot` (default: the model’s origin). `m:part` makes a child of the root,
`part:part` a child of that part.
- `part:mirror("x")` mirrors what the part has so far, pivots, turns and
hitboxes too. A child’s twin is `<name>_mirrored`. Only `"x"` works in this version.
- `part:hitbox(from, to)` is a box a player can hit on a living body that
wears the model. See “a living body”.
- Between two keys, a part turns **the short way round**. Keep each step
under 180 degrees. A wheel is `[0] = 0, [0.1] = -90, [0.2] = -180, ...`:
one key from 0 to 360 does not turn. A `tween` of `rotation` is not like
this: it turns as written, so there `roll = 360` is a full turn.
- `speed` is 0.01 to 100; a value outside is taken as the nearest end. A
speed of 0 does not pause: use `stop`. A new speed applies at once.
- An animation is keys per part: `{ [seconds] = vec3 }` for `rotation`
(degrees about the pivot) and `position` (an offset in model units).
  - Keys can be in any order.
  - An unknown part name is an error that lists the model’s parts.
  - Parts cannot share a track. Write a loop.
- A material is flat unless it has a `grain` (`0..1`: how much darker its
darkest pixel is). `0.1` is a painted panel, `0.4` a tyre. A grained face
has four tones, one pixel per unit. `alpha` below 1 is glass.
- A texture stretches over its face. For fine detail, draw two pixels per
unit.
- With `tint = material`, draw in greys. White is the material’s colour;
darker is a seam or a shadow.
- A mirrored box shows a side texture from the other end. Draw an
asymmetric texture once per side, after the `mirror`.
- `paint` repaints materials by name, and every texture they tint. An
unknown material name is an error that lists the model’s materials.
- Only Java clients from 1.21.4 see a model. Older clients and Bedrock see
`fallback`. A client that loads the resource pack after it joined gets
its models again when the pack is in; the pack does nothing for this.
- A client that turns the resource pack down, or cannot load it, sees
`fallback` from then on, also for the models it already sees.
- `citadel model render <pack dir> <name> --out car.png` draws a model.
Add `--animation drive --at 0.25` for mid-move. No name lists the models.
