---
title: "room:message"
description: "This room's world table: its blocks, entities and displays"
---

Part of [`Room`](/ref/Room/).

```luau
room:message(text: Text, color: Ink ?)
```

This room's `world` table: its blocks, entities and displays. This room's `players` table; its `on_join` fires each time a player moves in. This room's `sound` table. This room's `fx` table. This room's `ui` table. This room's `game` table: the game version it runs, its entity kinds and blocks. This room's `commands` table. Sends a chat line to everyone in this room.

## Parameters

| Name    | Type                 | Required |
| ------- | -------------------- | -------- |
| `text`  | [`Text`](/ref/Text/) | yes      |
| `color` | [`Ink`](/ref/Ink/)   | no       |

## Used in

> "room:message("A new round starts") -- a chat line to everyone in this room" — [Rooms](/concepts/rooms-and-dimensions/)
