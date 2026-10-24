---
title: "Room type"
description: "An isolated world with its own players and tables, from rooms.create or rooms.main."
---

An isolated world with its own players and tables, from `rooms.create` or `rooms.main`.

## Functions

| Call                            | Purpose                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`message`](/ref/Room/message/) | This room's `world` table: its blocks, entities and displays. This room's `players` table; its `on_join` fires each time a player moves in. This room's `sound` table. This room's `fx` table. This room's `ui` table. This room's `game` table: the game version it runs, its entity kinds and blocks. This room's `commands` table. Sends a chat line to everyone in this room. |
| [`destroy`](/ref/Room/destroy/) | Takes the room away; players still in it keep the world. Does nothing to `rooms.main`.                                                                                                                                                                                                                                                                                            |

## Fields

| Field                                              | Purpose                                                                                                                                                                        |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`room.spawn_point: Vec3`](/ref/Room/spawn_point/) | The room's number. Rooms also compare by identity with `==`. Where players arrive in this room; writable. A write is not stored and does not move the chunks that stay loaded. |
