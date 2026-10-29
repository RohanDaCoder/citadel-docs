---
title: 'players global · type Players'
description: 'A room''s players and their events: the players global, or room.players.'
---

A room's players and their events: the `players` global, or `room.players`.

Part of the [Player lifecycle](/players/player-lifecycle/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`on_join`](/ref/Players/on_join/) | Calls `fn` when a player arrives: on the globals when a client connects, on a room's table each time a player moves into it. |
| [`on_leave`](/ref/Players/on_leave/) | The same player value on_join had; it can no longer be sent to. |
| [`list`](/ref/Players/list/) | Returns every player in the room. |
| [`get`](/ref/Players/get/) | Returns the player with this name, or nil. |
| [`count`](/ref/Players/count/) | Returns how many players are in the room. |
| [`near`](/ref/Players/near/) | Who is within a radius of a point, and who is inside a box of blocks. |
| [`within`](/ref/Players/within/) | Returns every player inside a box of blocks, corners included. |
| [`on_click`](/ref/Players/on_click/) | Calls `fn` on a left or right click; `hit` holds the button and the entity, player, block and face it met. |
| [`on_sneak`](/ref/Players/on_sneak/) | Calls `fn` once per sneak press and release; `down` is true on the press. |
| [`on_slot`](/ref/Players/on_slot/) | Calls `fn` when a player picks a hotbar slot, 1..9. |
| [`on_chat`](/ref/Players/on_chat/) | Return false and the line is not said. |
| [`on_pickup`](/ref/Players/on_pickup/) | A stack taken off the ground, and one that landed on it. `player` is nil where the world dropped it, or where they have already left. |
| [`on_drop`](/ref/Players/on_drop/) | Calls `fn` when a stack lands on the ground; `player` is nil where the world dropped it or they have left. |
| [`on_death`](/ref/Players/on_death/) | Calls `fn` when a player dies, with the cause (fall, drown, void, lava, ...) and the line broadcast; `player` is nil once they have left. |
| [`on_respawn`](/ref/Players/on_respawn/) | Calls `fn` when a player respawns; `player` is nil once they have left. |
| [`on_break`](/ref/Players/on_break/) | Cancellable. Return `false` to stop it; return nothing to let it through. These are asked *before* the world changes and the engine waits milliseconds for the answer, so they must be quick and must never `task.wait`.  Timeout, error, overflow and disabled handlers deny the action. Across packs any `false` wins. See docs/luau-api.md, "saying no". |
| [`on_place`](/ref/Players/on_place/) | Asks `fn` before a player puts a block down; return false to cancel it. A missed deadline denies the place. |
| [`on_damage`](/ref/Players/on_damage/) | Asks `fn` before damage lands on a player; return false to refuse it. A missed deadline denies it. A pack's own `player:damage` is not asked about. |
