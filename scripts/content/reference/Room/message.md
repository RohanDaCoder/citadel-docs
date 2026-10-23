---
title: "room:message"
url: /docs/citadel/reference/Room/message
---

# room:message

This room's `world` table: its blocks, entities and displays. This room's `players` table; its `on_join` fires each time a player moves in. This room's `sound` table. This room's `fx` table. This room's `ui` table. This room's `game` table: the game version it runs, its entity kinds and blocks. This room's `commands` table. Sends a chat line to everyone in this room.

```
room:message(text: Text, color: Ink?)
```


## Parameters


## Used in
- [`room:message("A new round starts") -- a chat line to everyone in this room`Rooms](/docs/citadel/rooms)
