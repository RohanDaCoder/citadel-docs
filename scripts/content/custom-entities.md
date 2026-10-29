---
title: "Custom entities"
url: /docs/citadel/custom-entities
---

# Custom entities

Every entity has an `on_steer` and an `on_tick` hook. Three calls reach them:
**amend** the game’s own entity, **define** your own, and **spawn** it.
## Amending the game’s own
```luau
game.entities.amend("pig", {
    on_steer = function(e, base)
        base(e)            -- vanilla wander
        e.jumping = true   -- but always jumping
    end,
})

```
The amend also changes **pigs already in the world**, with no respawn.
- `base` is the behaviour you wrap: vanilla’s, or the previous pack’s.
- Wrapped behavior runs first by default. To replace it, pass `{ replace = true }` as the third argument and omit `base`.
- `base` makes a *decision*. What you assign after it wins. Two calls act as one.
- An amend changes **hooks** only. It refuses the keys `size`, `looks`, `physics`, `max_health`, `speed` and `persist`. For an entity that looks different, use `define`.
- You can amend only **the game’s own** content. A name with a colon is refused.
## Defining one of your own
```luau
local rocket = game.entities.define {
    name = "rocket", looks = "tnt", physics = "falling", size = 0.98,
    on_tick = function(e)
        e.velocity = e.velocity + vec3(0, 0.12, 0)
        e.data.fuse = (e.data.fuse or 60) - 1
        if e.data.fuse <= 0 then
            local at = e.at
            e:destroy()
            world.explode(at, 4)
        end
    end,
}

local it = world.spawn(rocket, vec3(8.5, 66, 8.5), { fuse = 40 })

```
| field | what it is |
| --- | --- |
| `name` | your name for the kind. The engine adds the namespace: `"rocket"` becomes `"rave:rocket"`. You cannot use another pack’s namespace. Lower case letters, digits and underscores. |
| `looks` | a shape the client **already draws**: `"pig"`, `"tnt"`, `"item"`, `"falling_block"`, `"none"`. Two forms take a payload: `{ entity = "falling_block", block = "sand" }` and `{ entity = "item", item = "diamond" }`. A name that this game’s oldest client does not know is refused, never replaced. |
| `physics` | the movement order: `"living"`, `"falling"`, `"item"`, `"none"`. Not a table of numbers; the game version sets those. `"living"` is a body with health: see “a living body”. |
| `size` | one number, or `{ width, height }`. Depth equals width, so a third number is an error. |
| `persist` | `"save"`: it comes back with the chunk, `e.data` included. Or `"despawn"`, the default. |
| `looks = models.x` | a model a pack made, with `seats`, `scale` and `fallback` next to it. See “vehicles”. |
| `physics = "vehicle"` | the engine drives it by seat 1’s keys, with `speed`, `turn`, `accel`, `step`. See “vehicles”. |
- Call `define` and `amend` **while your pack loads**.
- A world opened without your pack **quarantines** your entities: nothing ticks or shows them, and saves keep them unchanged. Install the pack again and they continue.
## A living body
With `physics = "living"` the entity is a real living thing. It falls, walks,
steps up half a block, swims, and takes fall damage, with the numbers of the
game version. It has health, players can hit it, and it dies. It has no
mind of its own: it moves only as your hooks say.
```luau
local sheep = game.entities.define {
    name = "fluffy", looks = "sheep", physics = "living", size = { 0.9, 1.3 },
    max_health = 8,                       -- 20 if you leave it out
    speed = 3,                            -- blocks a second at forward = 1
    drops = { { item = "white_wool", count = { 1, 3 } }, { item = "mutton" }, { item = "diamond", chance = 0.05 } },
    sounds = { hurt = "entity.sheep.hurt", death = "entity.sheep.death", ambient = "entity.sheep.ambient" },
    on_steer = function(e)
        e.forward = 1                     -- walk
        e.rotation = { yaw = -90 }        -- east
        e.jumping = e.data.stuck == true  -- jump when you ask it to
    end,
    on_damage = function(e, amount, by)
        if by then e.data.angry_at = by.name end
    end,
    on_remove = function(e, why)          -- why is "killed" after a death
    end,
}
world.spawn(sheep, vec3(8.5, 66, 8.5))

```
| field | what it is |
| --- | --- |
| `max_health` | the most health it has, and what it starts with. A whole number from 1 to 1024. 20 by default. `e.max_health` reads it. |
| `speed` | how fast it walks at `forward = 1`, in blocks a second. By default, the game’s own mob walk (about 3). |
| `drops` | what it leaves when it dies. Each row is `{ item = "stick", count = 2 }`. `count = { 1, 3 }` gives a random count. `chance = 0.05` leaves the row after one death in twenty; without it, after every death. A row can be a pack item. `false` or nil: nothing. |
| `sounds` | `{ hurt = ..., death = ..., ambient = ... }`, each a vanilla sound or `"<pack>.<file>"`. Each one is optional. |
| `can_fly` | `true`: it may fly, and it takes no fall damage. Your pack sets `e.flying` to take off and to land. See “flying and swimming”. |
- These five keys need `physics = "living"`. On another physics they are an error.
- Steer with the intent fields: `e.forward`, `e.strafe` (-1 to 1), `e.jumping` and `e.rotation.yaw`. A body keeps its intent until you change it. For AI, write them from `on_think`: see “a brain: on_think”.
- Writing `e.velocity` still works. It is a push by hand.
- A whole block needs a jump: set `e.jumping`, as a mob does.
- A player’s hit hurts it as a mob: the same damage, knockback, a red flash and a short time in which a second hit does not land. Arrows, falls, fire, lava and drowning hurt it too.
- With `looks = models.x`, the model flashes red too, for half a second, on clients from 1.21.4. It stays red while it dies. Older clients do not see the model flash.
- `on_damage(e, amount, by)` is asked before a player’s hit lands. `by` is that player. Answer `"ignore"` to stop the hit. Other damage lands without the question.
- At 0 health it dies as a mob: it falls over, leaves its `drops`, and is gone a second later. `on_remove` gets `"killed"`, and `world.on_entity_death` fires.
- With `looks = models.x` clients from 1.19.4 can hit it: the engine gives it an invisible hitbox of its `size`. Older clients cannot hit a model. A long model needs hit volumes: see “hit volumes”.
### Hit volumes
A body’s `size` is one square box. A long animal is much longer than that,
so a player who swings at its head or tail hits nothing. Give the model
hit volumes with `part:hitbox(from, to)`, in model units like a box:
```luau
local rex = models.new("rex", function(m)
    local skin = m:material("skin", colors.green)
    local body = m:part("body")
    body:box(vec3(-4, 6, -8), vec3(4, 16, 8), skin)
    body:hitbox(vec3(-4, 6, -8), vec3(4, 16, 8))          -- the body
    local head = body:part("head")
    head:box(vec3(-3, 10, -20), vec3(3, 16, -8), skin)
    head:hitbox(vec3(-3, 10, -20), vec3(3, 16, -8))       -- the head, in front (-z)
    local tail = body:part("tail")
    tail:box(vec3(-2, 8, 8), vec3(2, 12, 24), skin)
    tail:hitbox(vec3(-2, 8, 8), vec3(2, 12, 16))          -- the tail, in two parts:
    tail:hitbox(vec3(-2, 8, 16), vec3(2, 12, 24))         -- a hitbox is square from above
end)
local t_rex = game.entities.define {
    name = "rex", looks = rex, scale = 4, physics = "living", size = { 3.2, 5.5 },
}

```
- A hit on any volume is a hit on the body: the same damage, `on_damage` and death.
- The engine measures reach and aim to the volume a player hit, not to the body’s feet.
- A volume turns with the body’s yaw and tips with its pitch. It does not move with an animation: it stays where the part is at rest.
- A volume is square from above: as wide as its longer side. Split a long thin part into several volumes.
- A model with no volumes is hit on one box of the body’s `size`.
- Each volume is an entity on the client. A body that stands still sends nothing; a body that moves or turns sends one move a tick for each volume that moved.
- With `persist = "despawn"` (the default) it goes away when no player is near, as a mob does. With `"save"` it stays, with its health and `data`.
### Flying and swimming
A body with `can_fly = true` walks like any body and flies when `e.flying` is
true. This bird walks, takes off, flies to a perch and lands:
```luau
local perch = vec3(20.5, 75, 8.5)
local bird = game.entities.define {
    name = "bird", looks = models.bird, physics = "living", size = { 0.5, 0.6 },
    speed = 6, can_fly = true,
    on_steer = function(e)
        local to = perch - e.at
        local far = math.sqrt(to.x * to.x + to.z * to.z)
        e.rotation = { yaw = math.deg(math.atan2(-to.x, to.z)), pitch = 0 }
        if e.data.landed then
            e.forward = 0                           -- sits on the perch
        elseif e.age < 60 then
            e.forward = 0.5                         -- walks first
        elseif far > 1 then
            e.flying = true                         -- takes off, flies to it
            e.forward = 1
            e.rotation = { pitch = math.deg(-math.atan2(to.y, far)) }
        else
            e.flying = false                        -- drops onto the perch
            e.forward = 0
            e.data.landed = true
        end
    end,
}

```
- `e.flying = true`: no gravity. `forward` and `strafe` move it along its look, `rotation.pitch` included: a negative pitch climbs, a positive one dives. At `forward = 1` it flies at its `speed` (by default the game’s own air speed, about 4 blocks a second). With `forward = 0` it slows down and hovers.
- On the ground and still flying, it walks at its walk speed; a pitch up lifts it off.
- `e.flying = false`: it falls, lands, and walks again.
- A body with `can_fly` never takes fall damage, as the game’s own fliers do, also when you move it with `e.velocity`.
- `e.flying = true` on a body without `can_fly` is an error. `e.flying` reads `false` there.
- **In water** every body swims along its look. A pitch up rises as fast as a jump in water does, a pitch down dives. At pitch 0 it swims and sinks as a mob does. Its speed in water is the game’s swim speed, not `speed`. A flying body does not sink in water.
- `e.in_water` is `true` while it is in water: a crocodile can walk on land and swim when it is in.
- Clients see the pitch: a `looks = models.x` model tips with it (clients from 1.19.4); a vanilla look turns its head.
## A brain: on_think
AI is pack code. The engine gives the numbers and applies the answers. It
does not walk to a point or attack for you.
Use `on_think` for AI, not `on_steer`. The engine waits for `on_steer` two
milliseconds each tick, and a slow pack loses that decision. The engine never
waits for `on_think`, and it never loses its answer.
```luau
--!native
local zombie = game.entities.define {
    name = "walker", looks = "zombie", physics = "living", size = { 0.6, 1.95 },
    think_every = 0.25,                 -- seconds; each body thinks 4 times a second
    on_think = function(b)              -- one call for all the due bodies of this kind
        for i = 0, b.n - 1 do
            local o = i * 8             -- body i of a column is at byte i * 8
            local dx = buffer.readf64(b.player_x, o) - buffer.readf64(b.x, o)
            local dz = buffer.readf64(b.player_z, o) - buffer.readf64(b.z, o)
            buffer.writef64(b.yaw, o, math.deg(math.atan2(-dx, dz)))
            buffer.writef64(b.forward, o, if buffer.readf64(b.player, o) ~= 0 then 1 else 0)
        end
    end,
}

```
- `b.n` is the number of bodies in this call. Each other field of `b` is a
`buffer` with one number (an f64, 8 bytes) for each body. Body `i` is at
byte `i * 8`, for `i` from 0 to `b.n - 1`. A yes or no is 1 or 0. An id of
nothing is 0.
- The engine sends the bodies after a tick. The answer goes on the bodies at
the start of the next tick that has it: one tick later, or more for a slow
pack. An answer is never dropped. A slow pack is never switched off.
- To change a value, write a new one. A value that you do not change stays
as the body has it. A body keeps its intent until you change it.
- `think_every` is seconds, above 0 and at most 60. Without it, each body
thinks each tick. The engine spreads the bodies of a kind over the ticks.
- An event makes a body think on the next tick, also when it is not due.
- `b` and its buffers are the same table and buffers in each call. Their
numbers change. Keep your own memory in a table by `id`.
- `on_think` cannot wait: `task.wait` in it is an error.
- `on_think` is for `define`. `amend` refuses it. A kind without it costs
nothing.
- `--!native` at the top of the file makes this loop fast where the server
allows native code. The buffers are the form native code reads fastest.
| column | what it is |
| --- | --- |
| `id` | the entity id, as `e.id` and `world.entities()` give it |
| `x`, `y`, `z` | where its feet are |
| `health`, `age` | its health, and the ticks it has lived |
| `on_ground`, `in_water` | 1 or 0 |
| `hurt` | the damage it took since its last think; 0 for none |
| `hurt_by` | the id of the player whose hit it was; 0 for none |
| `landed` | 1: it came down on the ground after it was in the air |
| `blocked` | 1: it walked into a wall |
| `water` | 1: it went into water; -1: it came out; 0: neither |
| `touched` | the id of a player it began to touch; 0 for none |
| `player` | the id of the nearest player in survival or adventure; 0 for none |
| `player_x`, `player_y`, `player_z`, `player_dist` | where that player’s feet are, and how far |
| `yaw`, `pitch` | where it looks. Write to turn it. |
| `forward`, `strafe` | its intent, -1 to 1. Write to walk. |
| `jumping`, `flying` | its intent, 1 or 0. `flying` is for a body with `can_fly`. |
| `vx`, `vy`, `vz` | its velocity. Write to push it by hand. |
- Each event is in one think only. The next think has it at 0 again.
- `citadel.budget().asks.kinds.think` counts the bodies: `asks` sent,
`answered` applied, `late` applied more than one tick after they were
sent. `missed` stays 0.
- Use `on_steer` only for an answer in the same tick, such as a vehicle that
turns on a key. It can miss.
- Outside a hook, `e.forward`, `e.strafe`, `e.jumping` and `e.flying` on a
world handle change the body at once.
### A small steering library
The engine has no `move_to`. Copy this into your pack and change it as you
need. It turns smoothly, follows the points of `world.path`, jumps when a
wall blocks it, and aims a flier up or down.
```luau
--!native
-- steer.luau
local steer = {}

-- `from` turned toward `to` by at most `step` degrees.
function steer.turn(from: number, to: number, step: number): number
    local d = (to - from + 180) % 360 - 180
    return from + math.clamp(d, -step, step)
end

-- The yaw that looks from (x, z) to (tx, tz).
function steer.yaw(x: number, z: number, tx: number, tz: number): number
    return math.deg(math.atan2(-(tx - x), tz - z))
end

-- The pitch that flies up `dy` over `far` blocks: negative climbs.
function steer.pitch(dy: number, far: number): number
    return -math.deg(math.atan2(dy, far))
end

-- Body i of `b` walks the route { points = world.path(...), at = 1 }.
-- false when it is at the end.
function steer.follow(b, i: number, route, turn: number?): boolean
    local o = i * 8
    local x, y, z = buffer.readf64(b.x, o), buffer.readf64(b.y, o), buffer.readf64(b.z, o)
    local p = route.points[route.at]
    while p and (p.x - x) ^ 2 + (p.z - z) ^ 2 < 0.3 and math.abs(p.y - y) < 1 do
        route.at += 1
        p = route.points[route.at]
    end
    if not p then
        buffer.writef64(b.forward, o, 0)
        return false
    end
    local yaw = steer.turn(buffer.readf64(b.yaw, o), steer.yaw(x, z, p.x, p.z), turn or 45)
    buffer.writef64(b.yaw, o, yaw)
    buffer.writef64(b.forward, o, 1)
    local up = p.y > y + 0.5 or buffer.readf64(b.blocked, o) == 1
    buffer.writef64(b.jumping, o, if up then 1 else 0)
    return true
end

-- A flier of `b` aims at (tx, ty, tz): it flies there and looks up or down.
function steer.fly(b, i: number, tx: number, ty: number, tz: number)
    local o = i * 8
    local x, y, z = buffer.readf64(b.x, o), buffer.readf64(b.y, o), buffer.readf64(b.z, o)
    local far = math.sqrt((tx - x) ^ 2 + (tz - z) ^ 2)
    buffer.writef64(b.flying, o, 1)
    buffer.writef64(b.yaw, o, steer.turn(buffer.readf64(b.yaw, o), steer.yaw(x, z, tx, tz), 30))
    buffer.writef64(b.pitch, o, steer.pitch(ty - y, far))
    buffer.writef64(b.forward, o, if far > 1 then 1 else 0)
end

return steer

```
A chaser with it. It asks for a new path each second, or when it has none:
```luau
local steer = require("steer")
local routes = {}                       -- by body id
local chaser = game.entities.define {
    name = "chaser", looks = "zombie", physics = "living", size = { 0.6, 1.95 },
    think_every = 0.1,
    on_think = function(b)
        for i = 0, b.n - 1 do
            local o = i * 8
            local id = buffer.readf64(b.id, o)
            local r, age = routes[id], buffer.readf64(b.age, o)
            if buffer.readf64(b.player, o) == 0 then
                buffer.writef64(b.forward, o, 0)
            elseif not r or age > r.renew then
                local from = vec3(buffer.readf64(b.x, o), buffer.readf64(b.y, o), buffer.readf64(b.z, o))
                local to = vec3(buffer.readf64(b.player_x, o), buffer.readf64(b.player_y, o), buffer.readf64(b.player_z, o))
                routes[id] = { points = world.path(from, to, { size = { 0.6, 1.95 } }) or {}, at = 1, renew = age + 20 }
            end
            if routes[id] then steer.follow(b, i, routes[id]) end
        end
    end,
    on_remove = function(e) routes[e.id] = nil end,
}

```
## The handle
`world.spawn` returns a handle, `world.entities()` lists handles, and each
hook gets one:
`e.data` is a [data view](#data-views) for a **pack-defined entity**, including
one with `physics = "living"`. Nested writes persist through both callback and
world handles. It saves with the chunk only when the kind has `persist = "save"`.
Reading or assigning `.data` on a **built-in entity**, including an amended one,
raises an error: its engine-owned state is not a pack data record. Keep temporary
state for built-in entities in a pack table keyed by entity id; ids do not provide
a persistent identity across server restarts.
## Selecting entities
`world.entities()` with no argument returns all entities. For a local query,
give a position and a radius. You can also filter by kind:
```luau
local cows = world.entities {
    near = vec3(8, 65, 8),
    radius = 16,
    kind = "cow",
}
for _, cow in cows do
    cow:push(vec3(0, 0.1, 0))
end

local allCows = world.entities { kind = "cow" }

```
- `near` and `radius` go together. They select a sphere, boundary included.
- Results are handles in ascending id order. Queued spawns are included; removed entities are not.
- `kind` is the handle’s canonical name, with the pack namespace for a custom kind.
- Invalid options, a negative radius and non-finite numbers raise an error. An unknown kind returns an empty list.
- `entity:nearby(radius)` measures horizontal distance and excludes the entity itself.
`game.entities` gives a mob’s native behaviour values:
- Profiles are read-only. A write raises an error.
- A special behaviour without a shared profile returns `nil`.
- Profiles run no callbacks. To change gameplay, use `game.entities.amend(name, hooks)` and `game.entities.define(spec)`.
## What a missed deadline means here
Your hooks run outside the tick. Each tick, the engine sends your pack **one
batch** with all your due entities. It waits two milliseconds, then applies
the answers: `on_steer` before physics, `on_tick` after. The contract:
- **a hook reads the entity as it was at the start of that tick**; and
- **For custom kinds or `{ replace = true }`, a missed deadline keeps the last intent.** The entity keeps steering the
same way. The miss is counted at
`citadel.budget().asks.kinds["entity"].missed`.
| hook | a missed deadline means |
| --- | --- |
| `on_steer`, `on_tick` | Default amendments continue wrapped behavior. Custom kinds and explicit replacements keep their last intent; physics runs anyway. |
| `on_think` | nothing is missed: the engine does not wait. A slow answer lands on a later tick. See “a brain: on_think”. |
| `on_damage` | **`"take"`**: the damage lands. A busy pack must not make its own entities invulnerable. |
| `on_spawn`, `on_load`, `on_remove` | the engine never waits on these. They are notifications, and their return value is not read. |
`on_remove` does **not** fire when your pack is removed.
A reload is not a missed deadline. If the new script no longer amends a kind,
the kind gets its wrapped behaviour back. Your own kinds, fuses included, keep
moving through a reload.
## Two packs on one kind
Use `game.entities.amend(name, hooks, { priority = 10, replace = false })`.
Amendments run from lower to higher integer priority, regardless of pack name
or load order. Priority defaults to `0`. Two packs amending the same kind at
the same priority produce a load error naming both packs; choose distinct
priorities explicitly.
By default, wrapped behavior runs first, even if the hook omits `base` or
misses its deadline. Calling `base(e)` remains supported and never runs it
twice. Set `replace = true` explicitly to allow the hook to suppress the
wrapped steering/tick behavior; with this option, calling `base(e)` opts back
into it. The same options work with `game.entities.pig:amend(hooks, options)`.
Custom kinds made with `define` retain their existing `base` behavior.
