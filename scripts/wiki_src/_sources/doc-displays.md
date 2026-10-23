# SOURCE: Displays

- Clients from 1.19.4 see the real display and tween `animate`.
- Older clients see an invisible armor stand holding the `item`, or with
the `text` as a name tag.
- Older clients see nothing for `block` and `hitbox`. Give them a pad.
- A display belongs to its room and ends with the script.
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
d.id                                    -- entity id, what players.on_click reports in hit.entity_id
d.at, d.rotation, d.scale, d.billboard, d.glow   -- live, every kind
d.item, d.canvas, d.context             -- live, item kind (canvas reads back as the map id)
d.text, d.color, d.background, d.line_width, d.shadow    -- live, text kind; background = nil or false for none
d.block                                 -- live, block kind
d.duration                              -- seconds later changes take to play out (1.19.4+); 0
d.glide                                 -- advanced: movement smoothing seconds (1.20.2+); default 0.1
d.lead                                  -- advanced: true enables linear prediction; false by default, nil restores false
d:animate{ at = ..., scale = ..., rotation = { ... }, text = ..., duration = 0.5 }   -- one tweened change
d:destroy()

local h = world.hitbox{ at = vec3(...), width = 1, height = 1, on_click = function(player, button) end }
h.id; h.at; h:destroy()                 -- button is "left" or "right"
```
A hitbox is an invisible clickable box. Its `on_click` fires through
`players.on_click`. Clients below 1.19.4 get no hitbox.
`world.hitbox{ ..., solid = true }` is also a **wall**. A player cannot walk
through it and can stand on it.
- It works anywhere and moves when you write `at`.
- Its size is `width` (x) by `height` by `depth` (z). `depth` defaults to
`width`. `at` is its bottom centre.
- It cannot turn. Build a turning thing from several small walls.
- The engine fills it with cubes of its smallest side, 64 at most, and
warns past 64. Make a thin sheet from blocks.
- Clients from 1.20.5 stop at the exact size. Older clients stop at
one-block cubes.
## Choosing a world object and moving it
| Need | API | Why it exists |
| --- | --- | --- |
| Reusable appearance and named animations | `models.new` | Defines an asset for visuals or simulated entities. |
| A visual controlled by the pack | `world.display` | Places text, an item, a block or a model without simulation. |
| Physics, gameplay hooks or persistence | `game.entities.define` and `world.spawn` | Gives a body behavior independent of its appearance. |
| A mob appearance moved entirely by the pack | `world.puppet` | Uses a mob body without its AI or gameplay simulation. |
| A player-shaped character with a skin and equipment | `world.npc` | Adds avatar-specific behavior. |
| A player or NPC seated on something | `:ride` | Controls attachment and occupancy. |
| A different viewpoint | `player.camera` | Controls the view; `chase` composes with riding. |
| Authored changes over time | `tween` or `camera.path` | A tween animates fields; a camera path sequences shots. |
Displays, model displays, NPCs, puppets and entity handles share `id`, `alive`, `at`,
`rotation` and `:move(at, rotation?)`. `rotation` is a table of degree angles;
partial writes preserve omitted angles. `move` changes position and rotation
in one operation, and validates both before applying either. Entities continue
simulating after a move; changing their position does not clear velocity.
`at` and `rotation` read `nil` when the object is gone. Cleanup can be repeated.
Displays and models also share `scale`: reads return a `vec3`, writes accept a
number or vector. Models preserve their proportions and accept only equal,
positive axes; plain displays can stretch individual axes. Model entities expose
this same scale contract, or `nil` when they have no model. Bodies and NPCs
support yaw/pitch; roll belongs to displays and model displays. Displays also
accept `rotation = { forward = direction, up = roof }`; reads always return
angles. Use angle targets for `tween`: partial targets preserve other axes,
and angles interpolate as written, so `roll = 360` can author a full turn.
Write current positions with `at` or `move`; the engine smooths visual movement.
Use `display:animate{..., duration = seconds}` for an authored display transition,
`tween` for other live fields and `camera.path` for a sequence of camera shots.
`animate` sets the position interpolation time as well as the transform time.
`duration`, `glide` and `lead` are advanced display controls, not requirements
for moving a model or following it with a camera.
## Vehicles
A vehicle is an entity that looks like a model. Seat 1’s keys drive it.
The engine does the driving, gravity, walls and steps:
```luau
local car = game.entities.define {
    name = "car",
    looks = models.car,              -- a model from models.new
    physics = "vehicle",             -- the engine drives it
    size = { 1.6, 1 },               -- its body in blocks: width, height
    seats = { vec3(0, 8, 2), vec3(0, 8, 12) },   -- in model units; seat 1 drives
    speed = 16,                      -- blocks a second at full throttle (12 if left out)
    turn = 90,                       -- degrees a second at speed (90)
    accel = 1,                       -- seconds from standing to top speed (1)
    step = 1,                        -- blocks it climbs without a jump (1)
    scale = 1,                       -- the model's size (1)
    fallback = "minecart",           -- what a client older than 1.21.4 sees
}

local c = world.spawn(car, vec3(0.5, 65, 0.5))
player:ride(c)                                -- seat 1: W and S throttle, A and D steer
friend:ride(c, { seat = 2, locked = true })   -- locked: sneaking does not get them off
c.driver                                    -- player supplying seat 1 input; nil for an NPC or empty seat
c.riders[2]                                 -- actual occupant, including NPCs; nil means empty
npc:ride(c)                                   -- an npc at the wheel; it does not drive (see npcs)
c.paint = { paint = colors.blue }             -- this car's colours, by material name
c.scale = 1.5
c:play("drive", { speed = 2 })                -- again with another speed only changes the speed
c:stop("drive")
```
- Every tick, before any hook, the engine writes seat 1’s keys into `c.forward` (1 ahead, -1 back),
`c.strafe` (1 left, -1 right) and `c.jumping`. With seat 1 empty, the car
rolls to a stop.
- In `on_steer`, call `base(e)`, then adjust. Or skip `base` and set
`e.velocity` and `e.rotation` yourself:
`on_steer = function(e, base)
 base(e) -- drive as defined
 if e.data.boost then e.velocity = e.velocity * 1.4 end
end
`
A CPU driver (or an npc in seat 1) writes `e.forward` and `e.strafe`, or
the velocity, in this hook.
- `rotation.yaw` works as for every entity: 0 faces south (+z), 90 faces
west. The model’s front (-z) faces that way.
- The model and seats glide two ticks between moves. The rider’s chunks
follow the vehicle.
- Without `locked`, sneaking gets a rider off and fires `players.on_sneak`.
Then `player.riding` is false. `player:dismount()` gets anyone off.
- A seat holds one rider. `player:ride` and `npc:ride` return `false` for a
full seat.
- Creating a model or entity and mounting it in the same callback needs no
`task.wait`. The engine sends spawns before passenger attachments.
- Mounting the current seat again keeps the ride. An occupied, invalid, or
destroyed replacement leaves the current ride intact. Riding cycles are
rejected. Destroying a mount also clears its rider’s locked state.
- To give a player an npc’s car: `npc:dismount()`, move the npc with
`npc.at`, then seat the player.
- Only `physics = "vehicle"` reads `speed`, `turn`, `accel` and `step`, and
it needs `looks`. Anything else is an error at `define`.
## Riding anything else
`player:ride(thing)` also seats a player on a model display, a display, a
hitbox or an npc: anything with an `id` the client sees. The pack moves
these things.
- The player’s feet are 0.6 below the thing’s position. A model display’s
`seats` work as a vehicle’s; with none, seat 1 is the model’s origin.
- A ridden display glides two ticks between moves (1.20.2+), unless the
pack set a `glide` or `duration`.
- Pack-created displays and model displays interpolate the current positions
a pack supplies. This default does not extrapolate past a stop or bounce.
Seats and follow cameras use the same movement timing automatically.
- Smoothing introduces a short visual delay; it cannot remove network latency.
Java 1.20.2 and later interpolate display movement; earlier clients receive
positions using the features they support.
- Advanced overrides: `glide` changes the interpolation duration on a plain
display; `lead = true` enables linear prediction and reduces steady-motion
delay at the cost of possible overshoot at sudden stops. `lead = false`
sends the supplied positions; `nil` restores this default. Supply real
positions, not positions you predicted.
- The rider’s chunks follow the ridden thing, at any distance. Chunks behind
are dropped.
- `player.input` reads keys on foot from 1.21.2. Before 1.21.2, a client
reports keys only while it rides.
