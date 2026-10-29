# SOURCE: Input

```luau
players.on_click(function(player, hit) end) -> connection
--   hit.button = "left" | "right"   left is attack / swing, right is interact / use
--   hit.entity = display | hitbox | npc | puppet | nil   the thing itself, so `hit.entity == dealer` works
--   hit.entity_id = number?   its raw id; all there is for a screen's own frames, and for anything the script no longer keeps a handle to
--   hit.player = player?   another player, when that is what was clicked: a hit in a game
--   hit.block   = vec3?                 the block, when the click hit one
--   hit.face   = "up" | "down" | "north" | "south" | "west" | "east" | nil
players.on_sneak(function(player, down) end) -> connection    -- once per press and release
players.on_slot(function(player, slot) end) -> connection    -- hotbar 1..9
players.on_chat(function(player, text) end) -> connection    -- return false and the line is not said
player.rotation    -- { yaw, pitch } in degrees, live; read only
player.sneaking    -- boolean, live
player.input    -- { forward, sideways, jump, sneak, sprint, attack }: the keys held right now attack is the left button held on a block in reach: a client reports a held left button only while it digs, so it is false on air, and an adventure client never digs. A held left button on anything is: survival, `player.reach` long enough for the crosshair to land, and `player:effect("mining_fatigue", { level = 5 })` so no block cracks forward is 1, 0 or -1 (W and S); sideways is 1 for left, -1 for right (A and D); the rest are booleans
player:ride(thing) -> boolean    -- sit on a display, a model, a hitbox or an npc, and go where it goes; false when somebody sits in that seat of a model
player:dismount()    -- get off; sneaking does the same, as off a horse
player.riding    -- boolean, live
player:look() -> vec3    -- unit vector the player faces
player:set_slot(n)    -- selects hotbar slot 1..9
```
- One click is one event.
- A held button repeats every 200 ms. That is not a click.
- A left click on the world carries the block under the crosshair, up to
five blocks from the eyes.
- On a pack server, a click never changes the world.
The first `players.on_chat` takes over chat in its room. Each line is then
said once as `<name> text`, unless a listener returns `false`. With several
packs, each gets every line; it is still said once or not at all.
