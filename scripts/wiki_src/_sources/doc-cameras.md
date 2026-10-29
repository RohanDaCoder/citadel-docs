# SOURCE: Cameras

A camera is a value you put on a player. There are four kinds, and `camera.path` (below) eases from shot to shot:
```luau
local cut = camera.fixed{ at = vec3(0, 80, 30), look_at = vec3(0, 64, 0) }    -- no mouse; look_at = player works too
local window = camera.fixed{ from = car_cam }    -- look out of a display, an npc, an entity
local look = camera.free{ at = vec3(0, 70, 0) }    -- the mouse looks around from `at`
local orbit = camera.orbit{ follow = car, distance = 6, height = 1.6 }    -- the mouse circles `follow`
local chase = camera.chase{ follow = car, distance = 5, height = 3, pitch = 12 }    -- behind and above `follow`, turning with it; no mouse
player.camera = orbit
tween(cut, { at = vec3(0, 70, -10) }, { duration = 4, easing = "in_out" })    -- its fields tween
player.camera = nil    -- their own eyes again
```
- `cam.look_at = nil` removes the point or thing a camera looks at. `false`
does the same. Reading `look_at` returns the point or target handle; reading
`follow` returns the followed handle. A removed target reads `nil`.
- Each mode exposes only its relevant fields. `fixed{ from = target }` exposes
`from`; `fixed{ at = point }` exposes `at` and `look_at`; `free` exposes `at`;
`orbit` and `chase` expose `follow`, `distance` and `height`, and `chase` adds
`pitch`. `mode` and `from` are read-only. Ineffective fields are errors.
- `fixed` takes either `from` or `at` with optional `look_at`. Combining them
is an error. Distances must be finite and nonnegative, and angles/heights finite.
- **fixed** works in every mode. A player or thing as `look_at` (a model
too) is followed by its head. The player still walks and sees their own body: set
`player.speed = 0` for a cutscene. Do not use `gamemode = 3`.
- **free** and **orbit** seat the player, hidden and locked, on an engine seat. `orbit`
puts the eyes `distance` blocks behind `follow` (anything with an id),
`height` over its feet, opposite the look direction, and in front of walls.
Both need 1.19.4 (`player:supports("display")`). `free` means mouse look
from a point, not free flight. Because these modes need the player’s seat,
assigning either while riding is an error. The previous ride and camera
remain intact. Use `chase` while riding, or dismount before assigning one.
Likewise, `player:ride` while a free/orbit camera is active is an error;
clear `player.camera` or switch to `chase` first.
- **chase** is the view from behind a car. The engine keeps the eyes
`distance` blocks behind `follow` (a model, a vehicle, an npc, a player),
`height` over it, looking the way it heads and `pitch` degrees down, and in
front of walls. It moves with `follow` in the same step, so `follow` does
not shake in the view. **Use this to follow a thing a pack moves. Do not
move a display of your own behind it and look out of that**: the two are
sent as two things and drift against each other. A barrier does not pull
it in. 1.19.4 and later.
- A chase camera is aimed as its `follow` is. Submit the target’s current
position; the engine keeps its picture, seats and camera moving together.
Custom physics needs no future-position simulation or client timing constants.
- Chase and orbit move as their `follow` moves, with its `glide` and
`lead`. Smooth movement needs Java 1.20.2 or later.
- For the driver’s own eyes, seat them: `player:ride(car, { locked = true })`
and `player.camera = nil`. A chase camera and a seat go together: the body
is in the car and the view is behind it.
- `player.eye` is where a player’s view is from, as a vec3: the camera they
look out of, or their own eyes.
- One camera can be on many players. A change (`cam.at`, `cam.distance`,
`cam.follow = other`) shows on all of them next tick.
- Ending the camera, or leaving the room, gives back body, feet and eyes.
- Free/orbit cameras hide the body independently of potion effects. Ending
one preserves those effects and any ride assigned after the camera’s seat.
- Destroying a camera’s source or follow/look-at target ends the camera
automatically. A remote camera keeps terrain loaded around both the view
and the player’s body, including when looking out of another player.
- Creating a target and assigning its camera in the same callback needs no
delay. The engine spawns the target before selecting it and switches to a
replacement camera before removing the previous one.
- A server cannot set the field of view, force third person or hide the
hotbar.
`camera.path` is a fixed camera that eases from shot to shot. Each shot
after the first takes its own `duration`, or the path’s (5 seconds by
default). It returns the camera and a handle with `cancel()`.
```luau
local cam, run = camera.path({
    { at = vec3(0, 80, 30), look_at = vec3(0, 64, 0) },
    { at = vec3(40, 70, -10), look_at = vec3(0, 64, 0), duration = 5 },
    { at = vec3(10, 66, -20), look_at = vec3(0, 65, 0), duration = 3, easing = "out" },
}, { easing = "in_out", on_done = function() player.camera = nil player.speed = 1 end })
player.speed = 0
player.camera = cam
```
A shot `{ at = player }` is the player’s eyes, looking where they look. A
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
- A camera moves 20 times a second. From 1.20.2 the client glides between
moves.
