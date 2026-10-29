# SOURCE: Body and movement

```luau
player.speed = 2    -- walk speed as a multiple of normal; 0 pins them, 1 is normal
player.can_fly = true    -- may fly in a mode that cannot (adventure, survival); false takes it back
player.scale = 0.5    -- half size, 1/16 to 16; needs 1.20.5, older clients stay as they are
player.reach = 64    -- how far a block can be clicked or dug, 0..64 (4.5 is vanilla); needs 1.20.5
player.level = 7    -- the number over the experience bar
player.xp = 0.5    -- how full the bar is, 0..1
player:effect("speed", { level = 2, duration = 30, particles = false })    -- a potion effect by its modern name: speed, slowness, haste, jump_boost, regeneration, resistance, fire_resistance, water_breathing, invisibility, blindness, night_vision, glowing (1.9), levitation (1.9), slow_falling (1.13), darkness (1.19), ... ; `level` from 1, `duration` in seconds (30 by default; math.huge is for ever). A client too old for the effect is not sent it; a name no version has is an error naming them all.
player:clear_effect("speed")
player:push(vec3(0, 1, 0))    -- a shove, in blocks per tick, on top of what they are doing
player:damage(4)    -- two hearts, with the flash and the sound; "<name> died" if it was the last
player.health = 20    -- set outright, no flash; 0 is a death; above player.max_health it stops there
player:look_at(pos)    -- turn their head to a point, where they stand
player.camera = cam    -- look out of a camera (see cameras); nil or false is their own eyes
player.time = "midnight"    -- this player's sky alone, held there (ticks or a world.time name); nil or false gives them the room's again, as does moving rooms
player:stop_sound("rave.kick")    -- one sound by name, or every sound with no name (1.13 and later)
player:kick("Server full")    -- disconnect them, with that text on their screen
player:connect("hub")    -- ask Minefort to move them to another server, by its name
```
- `player:connect(server)` asks Minefort’s proxy to move the player: a BungeeCord `Connect` for a Java player, a `Transfer` to that name for a Bedrock player. It returns nothing and does not yield.
  - `server` is a server name: the `id` of an instance (see Network), the name of the network, or `hub`.
  - The name of the network sends the player to its default member. `network.info().network` is that name. `hub` is Minefort’s hub.
  - The name is 1 to 128 characters of letters, digits, `.`, `_` and `-`. Any other name is an error, and nothing is sent.
  - Minefort decides. It does not move a player to a server out of the network, and it does not tell the pack.
  - The call does not tell the pack the result. A player who is still here some seconds later was not moved.
  - It moves a Bedrock player, and a Java player on 1.7 or later. A Java player on an older version stays.
  - On a local run there is no proxy. A Java player stays. A Bedrock client reads the name as an address, and leaves the server.
- On a pack server, only `damage` and `health` hurt a player. Creative and
spectator players take no damage.
- At zero health the player dies. `players.on_death` fires with cause
`"other"`, and the client shows the respawn screen.
- On a pack server a death drops and clears nothing. The hotbar is a menu,
not an inventory.
