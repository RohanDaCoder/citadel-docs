---
title: Displays and models
section: ui
order: 6
description: world.display — floating text, items, blocks, frames and 3D models with live fields, tweening and billboards — plus the models.new system of materials, textures, parts, boxes, named animations and vehicles.
tags: [ui, displays, models, hitbox, billboards, animations, vehicles]
---

# Displays and models

> **In short:** a display is a floating item, text or block with no physics,
> placed by the pack and live-edited field by field. Clients from 1.19.4 see
> the real display; older ones get a stand-in. A 3D model — boxes in a tree of
> named parts, with materials, textures and named animations — shows through
> `world.display{ kind = "model" }` on Java clients from 1.21.4, with a
> `fallback` for everyone else. Vehicles and riding close the page.

## Kinds and versions

[`world.display{}`](/ref/World/display) places a visual without simulation. The
kinds: `"text"`, `"item"`, `"block"`, `"frame"` (a map picture — see
[Canvases](/wiki/canvases)) and `"model"`.

- Clients from 1.19.4 see the real display and tween `animate`. A display
  belongs to its room and ends with the script.
- Older clients see an invisible armor stand holding the `item`, or with the
  `text` as a name tag — and nothing for `block` and `hitbox`. Give them a pad.

```luau
-- every kind takes these
local d = world.display{
    kind = "text",                      -- "item", "text" or "block"
    at = vec3(0.5, 66, 0.5),            -- where it sits
    rotation = { yaw = 0, pitch = 0, roll = 0 },   -- degrees; pitch = 90 lays a text flat on a table
    scale = 1,                          -- or vec3(1, 2, 1); a number is the same on every axis
    billboard = "center",               -- "fixed", "vertical", "horizontal" or "center";
                                        --   text defaults to "center", the rest to "fixed"
    glow = colors.cyan,                 -- outline colour; leave it out, or write false, for none
    -- and a text takes these
    text = "BLACKJACK",                 -- text, see "Text formatting"
    color = colors.white,               -- a colour or a name
    background = color(0, 0, 0),        -- behind the words; leave it out, or write false, for none
    line_width = 200, shadow = false,
}
world.display{ kind = "item", at = vec3(2.5, 66, 0.5),
    item = "paper",                     -- canonical item name; or canvas = c, a world.canvas{}: a filled map of the picture
    context = "frame",                  -- how the item is posed: "frame", "none", "menu", "dropped", "worn", "held", "own_hand"
}
world.display{ kind = "block", at = vec3(4.5, 66, 0.5), block = "lapis_block" }
```

`billboard` is how a display turns toward the viewer: `"fixed"` never turns,
`"vertical"` turns about the up axis, `"horizontal"` tips up and down,
`"center"` does both.

## Live fields and tweening

| Field                                                   | What it is                                                                             |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `d.id`                                                  | Entity id, what `players.on_click` reports in `hit.entity_id`                          |
| `d.at, d.rotation, d.scale, d.billboard, d.glow`        | Live, every kind                                                                       |
| `d.item, d.canvas, d.context`                           | Live, item kind (`canvas` reads back as the map id)                                    |
| `d.text, d.color, d.background, d.line_width, d.shadow` | Live, text kind; `background = nil` or `false` for none                                |
| `d.block`                                               | Live, block kind                                                                       |
| `d.duration`                                            | Seconds later changes take to play out (1.19.4+); 0                                    |
| `d.glide`                                               | Advanced: movement smoothing seconds (1.20.2+); default 0.1                            |
| `d.lead`                                                | Advanced: `true` enables linear prediction; `false` by default, `nil` restores `false` |

```luau
d:animate{ at = ..., scale = ..., rotation = { ... }, text = ..., duration = 0.5 }   -- one tweened change
d:destroy()
```

`animate` makes one tweened change of place, scale, rotation or text over
`duration` seconds (0.5 by default), played by the client; it sets the position
interpolation time as well as the transform time. Use `animate` for an authored
transition, `tween` for other live fields. `duration`, `glide` and `lead` are
advanced controls, not requirements for moving a model.

## Hitboxes and walls

```luau
local h = world.hitbox{ at = vec3(...), width = 1, height = 1, on_click = function(player, button) end }
h.id; h.at; h:destroy()                 -- button is "left" or "right"
```

A hitbox is an invisible clickable box. Its `on_click` fires through
`players.on_click`; clients below 1.19.4 get no hitbox.

[`world.hitbox{ ..., solid = true }`](/ref/World/hitbox) is also a **wall**: a
player cannot walk through it and can stand on it.

- It works anywhere and moves when you write `at`.
- Its size is `width` (x) by `height` by `depth` (z); `depth` defaults to
  `width`; `at` is its bottom centre.
- It cannot turn. Build a turning thing from several small walls.
- The engine fills it with cubes of its smallest side, 64 at most, and warns
  past 64. Make a thin sheet from blocks.
- Clients from 1.20.5 stop at the exact size; older clients stop at one-block
  cubes.

## Choosing a world object and moving it

| Need                                                | API                                      | Why it exists                                                |
| --------------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------ |
| Reusable appearance and named animations            | `models.new`                             | Defines an asset for visuals or simulated entities.          |
| A visual controlled by the pack                     | `world.display`                          | Places text, an item, a block or a model without simulation. |
| Physics, gameplay hooks or persistence              | `game.entities.define` and `world.spawn` | Gives a body behavior independent of its appearance.         |
| A mob appearance moved entirely by the pack         | `world.puppet`                           | Uses a mob body without its AI or gameplay simulation.       |
| A player-shaped character with a skin and equipment | `world.npc`                              | Adds avatar-specific behavior.                               |
| A player or NPC seated on something                 | `:ride`                                  | Controls attachment and occupancy.                           |
| A different viewpoint                               | `player.camera`                          | Controls the view; `chase` composes with riding.             |
| Authored changes over time                          | `tween` or `camera.path`                 | A tween animates fields; a camera path sequences shots.      |

Displays, model displays, NPCs, puppets and entity handles share `id`, `alive`,
`at`, `rotation` and `:move(at, rotation?)` — a table of degree angles, where
partial writes preserve omitted angles; `move` changes position and rotation in
one operation, validating both before applying either. `at` and `rotation` read
`nil` when the object is gone; cleanup can be repeated.

Displays and models also share `scale`: reads return a `vec3`, writes accept a
number or vector. Models preserve their proportions and accept only equal,
positive axes; plain displays can stretch individual axes. Displays also accept
`rotation = { forward = direction, up = roof }`; reads always return angles. Use
angle targets for `tween`: partial targets preserve other axes, and angles
interpolate as written, so `roll = 360` can author a full turn. Write current
positions with `at` or `move`; the engine smooths visual movement.

## Vehicles and riding

A vehicle is an entity that looks like a model. Seat 1's keys drive it; the
engine does the driving, gravity, walls and steps. `game.entities.define` with
`physics = "vehicle"` makes one:

| Field      | What it is                                        |
| ---------- | ------------------------------------------------- |
| `looks`    | A model from `models.new`                         |
| `physics`  | `"vehicle"` — the engine drives it                |
| `size`     | Its body in blocks: width, height                 |
| `seats`    | In model units; seat 1 drives                     |
| `speed`    | Blocks a second at full throttle (12 if left out) |
| `turn`     | Degrees a second at speed (90)                    |
| `accel`    | Seconds from standing to top speed (1)            |
| `step`     | Blocks it climbs without a jump (1)               |
| `scale`    | The model's size (1)                              |
| `fallback` | What a client older than 1.21.4 sees              |

```luau
local c = world.spawn(car, vec3(0.5, 65, 0.5))    -- a car defined as above
player:ride(c)                                -- seat 1: W and S throttle, A and D steer
friend:ride(c, { seat = 2, locked = true })   -- locked: sneaking does not get them off
c.driver          -- player supplying seat 1 input; nil for an NPC or empty seat
c.riders[2]       -- actual occupant, including NPCs; nil means empty
c.paint = { paint = colors.blue }   -- this car's colours, by material name
c.scale = 1.5
c:play("drive", { speed = 2 })      -- again with another speed only changes the speed
c:stop("drive")
```

- Every tick, before any hook, the engine writes seat 1's keys into `c.forward`
  (1 ahead, -1 back), `c.strafe` (1 left, -1 right) and `c.jumping`; with seat 1
  empty, the car rolls to a stop.
- In `on_steer`, call `base(e)`, then adjust — or skip `base` and set
  `e.velocity` and `e.rotation` yourself. A CPU driver (or an npc in seat 1)
  writes `e.forward` and `e.strafe`, or the velocity, in this hook:

```luau
on_steer = function(e, base)
    base(e)                                    -- drive as defined
    if e.data.boost then e.velocity = e.velocity * 1.4 end
end
```

- `rotation.yaw` works as for every entity: 0 faces south (+z), 90 west; the
  model's front (-z) faces that way.
- Without `locked`, sneaking gets a rider off and fires `players.on_sneak`;
  `player:dismount()` gets anyone off. A seat holds one rider: `player:ride`
  and `npc:ride` return `false` for a full seat.
- Only `physics = "vehicle"` reads `speed`, `turn`, `accel` and `step`, and it
  needs `looks`. Anything else is an error at `define`.

`player:ride(thing)` also seats a player on a model display, a display, a
hitbox or an npc: anything with an `id` the client sees; the pack moves these
things. The player's feet are 0.6 below the thing's position. A model display's
`seats` work as a vehicle's; with none, seat 1 is the model's origin. A ridden
display glides two ticks between moves (1.20.2+), unless the pack set a `glide`
or `duration`; the rider's chunks follow the ridden thing, at any distance. A
rider stays upright — for a car on a wall, hide the driver (`invisibility`) and
use `camera.fixed`.

## 3D models

A model is a 3D shape a pack writes in code: boxes in a tree of named parts.
The engine shows it as item displays that move together.

> **Gotcha:** make models while the pack loads — [`models.new`](/ref/models/new)
> in a callback is an error.

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
```

### Materials and textures

- A material is flat unless it has a `grain` (`0..1`: how much darker its
  darkest pixel is). `0.1` is a painted panel, `0.4` a tyre. A grained face has
  four tones, one pixel per unit. `alpha` below 1 is glass.
- A texture stretches over its face; for fine detail, draw two pixels per unit.
  Its drawing calls are `fill(color)`, `rect(x, y, w, h, color)` and
  `pixel(x, y, color)`; `colors.transparent` makes a see-through pixel.
- With `tint = material`, draw in greys: white is the material's colour, darker
  is a seam or a shadow.
- `m:texture(w, h, { scroll = "up", speed = 2 })` is a texture that moves when
  a block is drawn from the model.
- A mirrored box shows a side texture from the other end. Draw an asymmetric
  texture once per side, after the `mirror`.

### Parts, boxes and mirrors

- **16 units are one block.** The origin is the model's bottom centre, `+y` is
  up, the front is `-z`. A box reaches `-24 .. 24` on every axis: three blocks.
  For a bigger thing, set the display's `scale`.
- A box turns on **one** axis only, in steps of 22.5 degrees, up to 45 either
  way. Anything else is an error. An octagonal wheel is two boxes, one turned 45.
- Box corners go in any order and can be fractional. A box's `pivot` defaults
  to its centre.
- Every box is in a part; there is no `m:box`. A part turns around its `pivot`
  (default: the model's origin). `m:part` makes a child of the root, `part:part`
  a child of that part.
- `part:mirror("x")` mirrors what the part has so far, pivots, turns and
  hitboxes too. A child's twin is `<name>_mirrored`. Only `"x"` works in this
  version.
- `part:hitbox(from, to)` is a box a player can hit on a living body that wears
  the model.

### Animations

An animation is keys per part: `{ [seconds] = vec3 }` for `rotation` (degrees
about the pivot) and `position` (an offset in model units).

- Keys can be in any order. An unknown part name is an error that lists the
  model's parts. Parts cannot share a track — write a loop.
- Between two keys, a part turns **the short way round**. Keep each step under
  180 degrees: a wheel is `[0] = 0, [0.1] = -90, [0.2] = -180, ...` — one key
  from 0 to 360 does not turn. A `tween` of `rotation` is not like this: it
  turns as written, so there `roll = 360` is a full turn.
- `speed` is 0.01 to 100; a value outside is taken as the nearest end. A speed
  of 0 does not pause: use `stop`. A new speed applies at once.

## Model displays

```luau
local d = world.display{
    kind = "model", model = car,
    at = vec3(10.5, 65, 4.5), rotation = { yaw = 90 },      -- degrees, as every entity turns: 0 faces south, 90 west
    scale = 3.5,                             -- 1 draws it at 16 units to the block
    paint = { paint = colors.blue },         -- keys are material names
    fallback = "minecart",                   -- what a client that cannot show it sees; nil shows nothing
    seats = { vec3(0, 7, 2) },               -- optional: where riders sit, in model units; see "vehicles"
}
d:move(vec3(12.5, 65, 4.5), { yaw = 180 })   -- place and turn it in one step, every part together
d:move(at, { forward = forward, up = up })   -- pointed: nose along forward, roof toward up (a car on a wall)
d.at, d.rotation                             -- live too; each write is a move of its own
d.scale = 2                                  -- live
d.paint = { paint = colors.red }             -- live
d:play("drive")                              -- from the beginning; an unknown name is an error
d:play("drive", { speed = 2 })               -- twice as fast; on the one already playing, the new speed at once
d:stop("drive")                              -- the parts stay where they are
d:destroy()
```

- `rotation.pitch` and `rotation.roll` tip the whole model about its origin,
  with parts, animations and seats.
- `paint` repaints materials by name, and every texture they tint. An unknown
  material name is an error that lists the model's materials.
- Only Java clients from 1.21.4 see a model; older clients and Bedrock see
  `fallback`. A client that loads the resource pack after it joined gets its
  models again when the pack is in; the pack does nothing for this.
- A client that turns the resource pack down, or cannot load it, sees
  `fallback` from then on, also for the models it already sees.

> **Tip:** `citadel model render <pack dir> <name> --out car.png` draws a model
> with no client; add `--animation drive --at 0.25` for mid-move. No name lists
> the models.

## See also

- [Canvases and pictures](/wiki/canvases) — the `frame` display kind and map pictures.
- [Custom entities](/wiki/custom-entities) — bodies with physics and gameplay hooks.
- [NPCs](/wiki/npcs) — player-shaped characters, posing and riding.
- [Movement](/wiki/movement) — riding, dismount and cameras in full.
- [Client versions](/appendix/client-versions) — the `display`, `hitbox` and `model` rows.
