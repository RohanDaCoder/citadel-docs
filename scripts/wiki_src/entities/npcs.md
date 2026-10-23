---
title: NPCs
section: entities
order: 4
description: world.npc and the Npc API — skins, name tags, poses, walking, holding items, armour and riding — plus world.puppet, a mob body with no mind of its own that the script moves.
tags: [entities, npcs, puppets, skins, poses, riding]
---
# NPCs

> **In short:** `world.npc{...}` places a player-shaped entity every client
> from 1.8 sees: skin, name tag, poses, walking, items in hand, armour,
> riding. The engine removes a script's NPCs when the script ends or reloads —
> a mob survives that, an NPC does not. `world.puppet{...}` places a mob's
> body with no mind of its own that the script moves.

## Making an NPC

`world.npc{...}` takes the options in one table: name, place, rotation and
skin. The skin has three forms, and the name has a length limit:

```luau
local n = world.npc{ name = "Dealer", at = vec3(0.5, 65, 4.5), rotation = { yaw = 180, pitch = 0 },
                     skin = "Notch" }   -- a player's name; the engine looks the skin up
--   skin = { value = "...", signature = "..." } is the raw profile property, for a skin no account wears
--   leave skin out, or write false, for the default skin; any other value is an error
```

| Option | What it is |
| --- | --- |
| `name` | at most 16 characters. |
| `at`, `rotation` | where it stands and which way it faces; set them later and the NPC moves. |
| `skin` | a player's name (the engine looks the skin up), `{ value = ..., signature = ... }` (the raw profile property), or left out / `false` for the default skin. Any other value is an error. |

- **Leave `name` out and the NPC has no name tag** from 1.8 on. A 1.7 client still shows a tag with an engine-made name.
- A `skin` given as a player's name costs two calls to Mojang. The NPC shows its own skin until the answer arrives. If no account has that name, the log says so.
- An NPC stays in the tab list for two seconds after it appears, then leaves it.

## The Npc API

Every call and field on the handle [`world.npc`](/ref/World/npc) returns, as
the docs list them:

```luau
n.id                   -- entity id, what players.on_click reports in hit.entity_id
n.name                 -- "" for one made with no name
n.at, n.rotation   -- live; set them and the NPC moves
n:look_at(pos)         -- turns head and body toward a point
n:swing()              -- the arm animation
n:hold("paper")        -- item in the main hand; n:hold(nil) or n:hold(false) empties it; errors on an unknown item
n:say("Place your bets.", "light_purple")   -- a chat line "<Dealer> ..." to the room (just the words with no name); text
n:walk{ path = { vec3(4.5, 65, 0.5), vec3(4.5, 65, 9.5) }, speed = 1.4, loop = true }
--   walks the points by itself, facing where it goes; speed in blocks a second
n.walking              -- true until the last point (never, with loop); n:walk(nil) stops it
n.pose = "sleeping"    -- "standing", "crouching", "sleeping" (flat on its back), "swimming" (flat on its front); live
n:wear{ head = "iron_helmet", chest = { item = "leather_chestplate", dye = colors.red } }   -- see "armour"
n:ride(car, { seat = 2 }) -> boolean   -- sits as player:ride does; false when that seat is taken
n:dismount()           -- gets off where it sits
n.riding               -- boolean, live
n:destroy()
```

The calls in table form:

| Call | Returns | Purpose |
| --- | --- | --- |
| `npc:look_at(pos)` | — | Turn head and body toward a point |
| `npc:swing()` | — | The arm animation |
| `npc:hold(item)` | — | Item in the main hand; `nil`/`false` empties it |
| `npc:say(text, color?)` | — | A chat line `"<name> ..."` to the room |
| `npc:walk{ path, speed, loop }` | — | Walk the points by itself |
| `npc:wear(pieces)` | — | Armour, head first |
| `npc:ride(thing, { seat = n })` | `boolean` | Sit as `player:ride` does; `false` when the seat is taken |
| `npc:dismount()` | — | Get off where it sits |
| `npc:move(at, rotation?)` | — | Set position and rotation together |
| `npc:destroy()` | — | Remove the NPC |

The fields: `n.id` (the entity id), `n.name` (`""` for one made with no
name), `n.at` and `n.rotation` (live; set them and the NPC moves), and —
live — `n.walking`, `n.pose` and `n.riding`.

`n:hold` and `n:wear` take items like any other item call — the armour pieces
are in [Inventory](/wiki/inventory). `n:say` sends a chat line; its text
follows [text formatting](/wiki/ui-basics), and its second argument is a
colour ink.

## Walking

The engine moves a walking NPC along the path the script gives once. It faces
its direction and moves its legs.

- It walks straight between points, at the points' height. Put points up a stair and at each corner.
- It walks through anything. The pack keeps the path clear.
- `n.walking` is true until the last point (never, with `loop`); `n:walk(nil)` stops it.

## Poses

A **pose** stays during a walk or a ride. A client that cannot show a pose
sees the NPC standing. `"standing"` is the default; the other
[`NpcPose`](/ref/NpcPose) values arrive with the client versions:

| pose | shown from |
| --- | --- |
| `"crouching"` | 1.8 |
| `"sleeping"` | 1.8: lying on its back, feet at `at`, head toward the yaw's side (to a quarter turn before 1.14) |
| `"swimming"` | 1.13 |

> **Gotcha:** for a client before 1.14, the engine puts a bed under a
> sleeping NPC, at height 0 in its column. Do not lay a sleeping NPC where
> the pack builds at height 0 in that column.

## Riding

`n:ride(thing, { seat = n })` takes what `player:ride` takes: a vehicle's
seat, a model display's seat, a display, a hitbox, or another NPC.

- Every client, also a later one, sees the NPC seated and moving with the vehicle.
- A client that cannot see the seat (a display needs 1.19.4) sees the NPC standing at the seat, moving with it.
- `ride` stops a walk. `n.at` reads the seat's position.
- An NPC never drives a vehicle — see [Displays and 3D models](/wiki/displays).
- After `n:dismount()`, set `n.at` to move the NPC somewhere else.

`npc:ride` mirrors `player:ride`; the player-side rules — seats, `locked`,
what a mount takes — are in [Movement](/wiki/movement).

## Puppets

A puppet is a mob's body with no mind of its own that the script moves, from
[`world.puppet`](/ref/World/puppet). Its name tag is always shown:

```luau
local p = world.puppet{ kind = "horse", at = vec3(0.5, 65, -100.5), rotation = { yaw = 90 }, name = { "Lightning", color = "gold" } }   -- name is text
p.id, p.name           -- the name tag is always shown; errors when this game has no such mob kind
p.at, p.rotation   -- live
p:destroy()
```

- `kind` is required; it errors when this game has no such mob kind.
- `name` is text: `p.name` reads the name tag's text, which is always shown.
- Displays, model displays, NPCs, puppets and entity handles share `id`, `alive`, `at`, `rotation` and `:move(at, rotation?)` — the shared contract is on [Entity handles](/wiki/entity-handles).

## NPCs and reload

The engine removes a script's NPCs and puppets when the script ends or
reloads. That is the line between an NPC and a mob:

- A mob a pack spawns stays when the script reloads; an NPC does not — see [Mobs and spawning](/wiki/mobs).
- A puppet is a mob's body with no mind of its own; an NPC is player-shaped. Both are placed, moved and removed by the script.

## See also

- [Mobs and spawning](/wiki/mobs) — `world.spawn` and what survives a reload.
- [Entity handles](/wiki/entity-handles) — the shared `id`/`alive`/`at`/`rotation`/`:move` contract.
- [Displays and 3D models](/wiki/displays) — vehicles, seats and what an NPC can ride.
- [Inventory](/wiki/inventory) — items and armour, what `n:hold` and `n:wear` take.
- [Movement](/wiki/movement) — `player:ride`, the calls `npc:ride` mirrors.
