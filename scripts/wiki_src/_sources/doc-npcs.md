# SOURCE: NPCs

```luau
local n = world.npc{ name = "Dealer", at = vec3(0.5, 65, 4.5), rotation = { yaw = 180, pitch = 0 },
                     skin = "Notch" }   -- a player's name; the engine looks the skin up
--   skin = { value = "...", signature = "..." } is the raw profile property, for a skin no account wears
--   leave skin out, or write false, for the default skin; any other value is an error
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

local p = world.puppet{ kind = "horse", at = vec3(0.5, 65, -100.5), rotation = { yaw = 90 }, name = { "Lightning", color = "gold" } }   -- name is text
p.id, p.name           -- the name tag is always shown; errors when this game has no such mob kind
p.at, p.rotation   -- live
p:destroy()
```

- A name is at most 16 characters.
- **Leave `name` out and the NPC has no name tag** from 1.8 on. A 1.7 client still shows a tag with an engine-made name.
- An NPC stays in the tab list for two seconds after it appears, then leaves it.
- A `skin` given as a player’s name costs two calls to Mojang. The NPC shows its own skin until the answer arrives. If no account has that name, the log says so.
- The engine removes a script’s NPCs and puppets when the script ends or reloads.
  **Walking.** The engine moves a walking NPC along the path the script gives
  once. It faces its direction and moves its legs.
- It walks straight between points, at the points’ height. Put points up a stair and at each corner.
- It walks through anything. The pack keeps the path clear.
  A **pose** stays during a walk or a ride. A client that cannot show a pose
  sees the NPC standing:
  | pose | shown from | | --- | --- |
  | `"crouching"` | 1.8 |
  | `"sleeping"` | 1.8: lying on its back, feet at `at`, head toward the yaw’s side (to a quarter turn before 1.14) |
  | `"swimming"` | 1.13 |
  For a client before 1.14, the engine puts a bed under a sleeping NPC, at
  height 0 in its column. Do not lay a sleeping NPC where the pack builds at
  height 0 in that column.
  **Riding.** `n:ride(thing, { seat = n })` takes what `player:ride` takes: a
  vehicle’s seat, a model display’s seat, a display, a hitbox, or another NPC.
- Every client, also a later one, sees the NPC seated and moving with the vehicle.
- A client that cannot see the seat (a display needs 1.19.4) sees the NPC standing at the seat, moving with it.
- `ride` stops a walk. `n.at` reads the seat’s position.
- An NPC never drives a vehicle (see “vehicles”).
- After `n:dismount()`, set `n.at` to move the NPC somewhere else.
