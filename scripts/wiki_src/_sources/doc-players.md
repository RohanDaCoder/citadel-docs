# SOURCE: Players

```luau
players.on_join(function(player) end) -> connection
players.on_leave(function(player) end) -> connection    -- the same player value; it can no longer be sent to
players.list()    -- array of player
players.get(name)    -- player or nil
players.count()
player.name    -- string
player.uuid    -- the account's own id, as a string
player.at    -- vec3, where they stand now
player.data    -- a table of your own, kept until 10 seconds after they leave
player.gamemode    -- 0 survival, 1 creative, 2 adventure, 3 spectator; set it to change it
player.ui.title{ title = "RAVE", subtitle = "", color = "white", fade_in = 0.25, stay = 2, fade_out = 0.5 }    -- text; seconds
player:message(text, color)    -- text; color is for the words that did not pick one
player:sound(name, { at = player.at, volume = 1, pitch = 1, category = "record" })
player:teleport(pos, { yaw = 0, pitch = 0 })    -- a rotation; an angle left out keeps the way they face
player:move_to(room)    -- see rooms; `player.room` is the Room the player is in
player:give("stone_pickaxe")    -- one; canonical item name; errors on a name this game version lacks
player:give{ item = "arrow", count = 16 }
player:held()    -- { item = "cobblestone", count = 3 } in hand, or nil; a pack item adds `id`, a worn tool `damage`
player:inventory()    -- { { item = "cobblestone", count = 3 }, ... }, one entry per filled slot, the same rows
player:count("iron_ingot")    -- how many of one item, across every slot; see "items of your own" for what matches
player:take("coal", 8)    -- takes up to 8, the hand first; answers how many it took
player:set_held(item)    -- the stack in hand, replaced; nil or false empties the hand
player:supports("light")    -- can this player's client show it? see "Client versions"
player.visible = false    -- nobody else sees this player; true or nil shows them again; see "who sees whom"
player:hide(other)    -- this player stops seeing `other`; player:show(other) undoes it
player:can_see(other)    -- true unless `other` is not visible or is hidden from this player
player.health    -- their health now, 0 to player.max_health; nil where the version has no damage rules
player.max_health    -- the most health they can have: 20 unless a pack set it; nil for the same reason
player.food    -- 0..20, or nil where the version has no food bar
player.saturation    -- number, or nil for the same reason
player.dead    -- true while they are on the death screen
player:kill()    -- true if it happened; false on a version with no damage rules
player.health = 12    -- set outright, no flash; 0 is a death. See "Body and movement"
player.max_health = 40    -- 20 hearts; nil gives the game's own (20) back. See "health, food and `nil`"
player:damage(4)    -- a hit: two hearts, the flash, the sound, the resistance window
players.on_death(function(player, cause, message, by) end) -> connection    -- by: the player who did it, or nil
players.on_respawn(function(player) end) -> connection
```
`player:give`, `player:take`, `player:inventory` and `player:count` work on
inventory stacks.
- A given stack merges into existing stacks, hotbar first.
- What does not fit is dropped from the give, not duplicated.
- Clicks in the player’s own window work as in the game, all seven click
modes included.
- A pack’s own menu over the inventory is `player.ui.menu{}` (see “Menus”).
- A chest’s stacks are `world.container` (see “containers”).
## Who sees whom
A player sees others in their room who are in view. Two settings remove a
player’s body from a client:
```luau
player.visible = false        -- from everyone; true or nil brings it back
viewer:hide(player)           -- from this viewer only; viewer:show(player) undoes it
viewer:can_see(player)        -- what the two add up to

-- a lobby where nobody sees anyone
room.players.on_join(function(p) p.visible = false end)
room.players.on_leave(function(p) p.visible = true end)

-- teams: each side sees only its own
for _, a in players.list() do
    for _, b in players.list() do
        if a.data.team ~= b.data.team then a:hide(b) else a:show(b) end
    end
end
```
- A hidden player is gone from that client: no body, name, armour or hitbox.
The `invisibility` effect differs: it shows armour and the held item.
- The tab list still shows hidden players.
- Both settings last across rooms.
- `hide` is by account, so it lasts when the other player rejoins.
- A new session resets both: nothing hidden, and `visible` is true.
## Health, food and nil
`player.health`, `player.max_health`, `player.food` and `player.saturation`
are `nil`, not `0`, on a game version with no rule for them. Every Alpha node
is one (a0.1.0 has no food and no damage). Across the engine, what a version
lacks is absent, not zero.
`health` is always the health of one individual now. `max_health` is always
the most it can be. This is the same for a player, for an entity in the world
and for a kind (a kind has `max_health` only).
- `player.max_health = n` takes 1 to 1024. `nil` gives the game’s own (20)
back. Another type or a number out of range is an error. It is an error on
a version with no damage rules.
- A lower maximum takes `player.health` down to it. A higher maximum does not
heal.
- `player.health = n` with `n` above the maximum gives the maximum. Food,
regeneration and peaceful healing stop at the maximum. A respawn fills to
it.
- Every Java client (1.7 to 26.3) draws the hearts of the maximum. A Bedrock
client draws no health today.
- The maximum lasts for the session, also across rooms and deaths. Set it in
`players.on_join`.
`cause` in `players.on_death` is one of `fall`, `drown`, `suffocate`, `void`,
`lava`, `fire`, `cactus`, `starve`, `attack` (a mob’s or a player’s hit),
`shot` (an arrow), `blast`, `magic` and `other` (a pack’s own
`player:damage`). `message` is the broadcast English death line. `by` is the
player who hit or shot them, or `nil`.
**A player is one value while connected.** Every event passes the same
`player`:
- `a == b` compares players, and a player can be a table key.
- `player.data` holds your own state. You need no table keyed by name.
- In `players.on_leave`, `player.name` and `player.data` still read. `data`
is kept for 10 seconds after they leave; after that a value you still hold
reads an empty table.
- `data` may name the player (`p.data.state = { player = p }`, a function
that uses `p`); it is let go with them all the same.
- A player who rejoins is a new value with empty `data`.
```luau
players.on_join(function(p) p.data.coins = 0 end)
players.on_leave(function(p) storage.set("coins." .. p.uuid, p.data.coins) end)
```
