---
title: 'Movement and cameras'
description: 'Moving players — teleport, move_to, travel, push, and the writable speed, scale and reach — riding and seats, body rotation, the four camera modes with camera.path easing, and the input events a pack can read.'
---

:::note[In short]
the pack moves a player with `player:teleport`, `player:push`,
`player:move_to` (another room) and `player:travel` (another world of the
group); the body has writable `speed`, `scale` and `reach`. A player can
ride anything with an id the client sees. The camera system — `fixed`,
`free`, `orbit`, `chase` and the easing `camera.path` — replaces what they
look out of, for cutscenes and follow shots. Clicks and held keys arrive as
events.
:::

## Teleporting, and between worlds

Three calls move a player outright, at three scales.

| Call                                                      | Effect                                                        |
| --------------------------------------------------------- | ------------------------------------------------------------- |
| [`player:teleport(pos, rotation?)`](/ref/Player/teleport/) | To a position; yaw and pitch left out keep the way they face. |
| [`player:move_to(room)`](/ref/Player/move_to/)             | To another room; the client swaps worlds in place.            |
| [`player:travel(dimension, pos?)`](/ref/Player/travel/)    | To another world of the group, at `pos` or its spawn.         |

```luau
player:teleport(vec3(0.5, 65, 0.5))              -- rotation left out: keeps facing
player:teleport(SPAWN, { yaw = 0, pitch = 0 })   -- faces south, level
player:move_to(room)                              -- the client swaps worlds in place
```

Rotation is a `BodyRotation` in degrees: 0 yaw faces south, 90 west; positive
pitch tips down. `player.room` is nil while the player moves between rooms;
rooms compare by identity. Rooms and dimensions are covered in
[Rooms and dimensions](/concepts/rooms-and-dimensions/).

## Pushing and the body

| Field                               | Meaning                                                                                                                               |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| [`player.speed`](/ref/Player/speed/) | Walk speed as a multiple of normal; 0 pins them.                                                                                      |
| [`player.scale`](/ref/Player/scale/) | 1/16 to 16; 1.20.5 and later, older clients stay as they are.                                                                         |
| [`player.reach`](/ref/Player/reach/) | How far a block can be clicked or dug, 0 to 64 blocks (4.5 by default); 1.20.5 and later. Measured from the camera when there is one. |
| `player.can_fly`                    | May fly in a mode that cannot.                                                                                                        |

[`player:push(velocity)`](/ref/Player/push/) is a shove in blocks per tick, on
top of what they are doing.

:::caution[Gotcha]
Numeric settings such as `player.speed`, `player.scale` and
`player.reach` require a number; `nil` does not reset them.
:::

The anticheat rule watches what each Java client claims. `player:push` and a
movement effect (`speed`, `jump_boost`, `levitation`, `slow_falling`,
`dolphins_grace`) exempt the player while they last, and `player:teleport` is
always allowed. A pack that moves players in any other way turns `anticheat`
off: `world.rules{ anticheat = false }` (see
[World state](/world/world-state/)).

## Looking

- `player.rotation` — degrees: `yaw` sideways, `pitch` up or down; live, read
  only.
- [`player:look()`](/ref/Player/look/) — the unit vector the player faces.
- [`player:look_at(pos)`](/ref/Player/look_at/) — turns the player's head to a
  point, where they stand.
- `player.eye` — where the player's view is from, as a vec3: the camera they
  look out of, or their own eyes.

## Riding

| Call                                            | Effect                                                               |
| ----------------------------------------------- | -------------------------------------------------------------------- |
| [`player:ride(thing, opts?)`](/ref/Player/ride/) | Seats the player; `opts` is `{ seat = number?, locked = boolean? }`. |
| [`player:dismount()`](/ref/Player/dismount/)     | Gets the player off; sneaking does the same, as off a horse.         |

- Seat 1 drives a vehicle; `locked` keeps a sneak from getting them off.
- `ride` returns `false` when somebody sits in that seat; it keeps the current
  ride on failure.
- It works immediately after creating the target. Repeating the same ride
  keeps the seat; no delay or extra movement is needed.
- `player.sitting` is true while the player sits on something; live.

```luau
player:ride(c)                                -- seat 1: W and S throttle, A and D steer
friend:ride(c, { seat = 2, locked = true })   -- locked: sneaking does not get them off
```

`player:ride(thing)` seats a player on anything with an `id` the client sees —
a vehicle, a model display, a display, a hitbox, an npc. The pack moves these
things; see [Displays](/ui/displays/) for seats, vehicles and ridden
displays.

### Cameras and seats

`free` and `orbit` cameras seat the player, hidden and locked, on an engine
seat — so the two systems collide:

- Assigning `free` or `orbit` while the player rides is an error. The previous
  ride and camera remain intact.
- `player:ride` while a `free`/`orbit` camera is active is an error; clear
  `player.camera` or switch to `chase` first.
- For the driver's own eyes, seat them — `player:ride(car, { locked = true })`
  and `player.camera = nil`. A chase camera and a seat go together: the body
  is in the car and the view is behind it.

## The camera system

A camera is a value you put on a player: `player.camera = cam`, or `nil` or
`false` for their own eyes. There are four kinds, and
[`camera.path`](#camera-paths) eases from shot to shot:

| Mode    | What the player sees                                                                                  | Needs               |
| ------- | ----------------------------------------------------------------------------------------------------- | ------------------- |
| `fixed` | A shot from a point (`at`) or of a target (`from`), with optional `look_at`.                          | works in every mode |
| `free`  | Mouse look from a point — not free flight.                                                            | 1.19.4              |
| `orbit` | The eyes `distance` blocks behind `follow`, `height` over its feet, opposite the look direction.      | 1.19.4              |
| `chase` | The view from behind a car: behind `follow`, `height` over it, heading its way, `pitch` degrees down. | 1.19.4              |

### fixed

- `fixed` takes either `from` or `at` with optional `look_at`. Combining them
  is an error.
- `fixed{ from = target }` exposes `from`; `fixed{ at = point }` exposes `at`
  and `look_at`.
- A player or thing as `look_at` (a model too) is followed by its head.
- The player still walks and sees their own body: set `player.speed = 0` for a
  cutscene. Do not use `gamemode = 3`.

### free and orbit

Both seat the player, hidden and locked, on an engine seat, and both need
1.19.4 (`player:supports("display")`). `free` means mouse look from a point,
not free flight, and exposes `at`. `orbit` puts the eyes `distance` blocks
behind `follow` (anything with an id), `height` over its feet, opposite the
look direction, and in front of walls.

### chase

The engine keeps the eyes `distance` blocks behind `follow` (a model, a
vehicle, an npc, a player), `height` over it, looking the way it heads and
`pitch` degrees down, and in front of walls. It moves with `follow` in the
same step, so `follow` does not shake in the view. 1.19.4 and later.

:::tip
Use this to follow a thing a pack moves. Do not move a display of
your own behind it and look out of that: the two are sent as two things and
drift against each other. A barrier does not pull it in.
:::

A chase camera is aimed as its `follow` is. Submit the target's current
position; the engine keeps its picture, seats and camera moving together.
Custom physics needs no future-position simulation or client timing constants.

Chase and orbit move as their `follow` moves, with its `glide` and `lead`.
Smooth movement needs Java 1.20.2 or later.

### Fields, sharing and lifetime

- Each mode exposes only its relevant fields: `orbit` and `chase` expose
  `follow`, `distance` and `height`, and `chase` adds `pitch`. `mode` and
  `from` are read-only. Ineffective fields are errors.
- Distances must be finite and nonnegative, and angles/heights finite.
- `cam.look_at = nil` removes the point or thing a camera looks at; `false`
  does the same. Reading `look_at` returns the point or target handle; reading
  `follow` returns the followed handle. A removed target reads `nil`.
- One camera can be on many players. A change (`cam.at`, `cam.distance`,
  `cam.follow = other`) shows on all of them next tick.
- Ending the camera, or leaving the room, gives back body, feet and eyes.
- Free/orbit cameras hide the body independently of potion effects. Ending
  one preserves those effects and any ride assigned after the camera's seat.
- Destroying a camera's source or follow/look-at target ends the camera
  automatically. A remote camera keeps terrain loaded around both the view
  and the player's body, including when looking out of another player.
- Creating a target and assigning its camera in the same callback needs no
  delay. The engine spawns the target before selecting it and switches to a
  replacement camera before removing the previous one.

:::note
A server cannot set the field of view, force third person or hide
the hotbar.
:::

## Camera paths

`camera.path` is a fixed camera that eases from shot to shot. Each shot after
the first takes its own `duration`, or the path's (5 seconds by default). It
returns the camera and a handle with `cancel()`.

```luau
local cam, run = camera.path({
    { at = vec3(0, 80, 30), look_at = vec3(0, 64, 0) },
    { at = vec3(40, 70, -10), look_at = vec3(0, 64, 0), duration = 5 },
    { at = vec3(10, 66, -20), look_at = vec3(0, 65, 0), duration = 3, easing = "out" },
}, { easing = "in_out", on_done = function() player.camera = nil player.speed = 1 end })
player.speed = 0
player.camera = cam
```

A shot `{ at = player }` is the player's eyes, looking where they look. A
player or thing in a shot is read when the shot starts:

```luau
camera.path({
    { at = vec3(0, 90, 60), look_at = vec3(0, 64, 0) },     -- over the map
    { at = vec3(4, 67, 4), look_at = player, duration = 4 }, -- down to them, standing there
    { at = player, duration = 2 },                           -- into their eyes
}, { on_done = function() player.camera = nil player.speed = 1 end })
```

- End on `{ at = player }` so removing the camera does not jump.
- To hold a shot, repeat it.

A camera moves 20 times a second. From 1.20.2 the client glides between moves.

## Input: clicks and keys

- One click is one event. A held button repeats every 200 ms — that is not a
  click.
- A left click on the world carries the block under the crosshair, up to five
  blocks from the eyes.
- On a pack server, a click never changes the world.
- `player.input` reads keys on foot from 1.21.2. Before 1.21.2, a client
  reports keys only while it rides.
- The first `players.on_chat` takes over chat in its room. Each line is then
  said once as `<name> text`, unless a listener returns `false`. With several
  packs, each gets every line; it is still said once or not at all.

Clicks arrive through `players.on_click` with a `hit` table — the button, the
slot, and the player, entity, block and face the click met. The event model
and the full catalog are in [The event model](/concepts/events/) and the
[Event catalog](/appendix/event-catalog/).

## See also

- [Displays](/ui/displays/) — vehicles, seats and ridden displays.
- [Rooms and dimensions](/concepts/rooms-and-dimensions/) — `move_to` and `travel` in context.
- [World state](/world/world-state/) — the `anticheat` rule and the rest of `world.rules`.
- [The event model](/concepts/events/) — `on_click`, `on_chat` and connections.
- [Player lifecycle](/players/player-lifecycle/) — join, leave and the session.
