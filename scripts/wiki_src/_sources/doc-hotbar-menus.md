# SOURCE: Hotbar menus

- Selecting a slot fires `players.on_slot`.
- A click while holding a slot fires `players.on_click` with `hit.slot`
  set. Any target and either button counts.
- Right clicks never merge into a hold. The halves of one click (block
  use, item use, both hands) are one event.
- In pack mode the rest of the inventory is locked.

```luau
player:hotbar{                       -- replaces the nine hotbar slots; a missing index is empty
    [1] = { item = "lapis_block", name = "HIT", count = 1 },
    [7] = { item = "gold_nugget", name = "Bet: 50" },
    [8] = { canvas = minimap, name = "Map" },   -- a filled map of a canvas: a live picture in the hand
}
player.slot                          -- the slot in hand, 1..9, live
hit.slot                             -- on every players.on_click, 1..9
```

A slot is an item (see “items”), with the same meta. An item name that the
game version lacks is an error.
With `canvas = c`, the map shows the picture on every client
from 1.8, and it updates as the script draws.
