---
title: 'rooms global'
description: 'Making and destroying rooms — isolated worlds with their own tables.'
---

Making and destroying rooms — isolated worlds with their own tables.

Part of the [Rooms and dimensions](/concepts/rooms-and-dimensions/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`create`](/ref/rooms/create/) | Creates an isolated room with its own chunks, players and effects; `spawn_point` defaults to (0.5, 65, 0.5), `generate` fills each chunk. |

## Fields

| Field | Purpose |
| --- | --- |
| [`rooms.main: Room`](/ref/rooms/main/) | The main room, whose tables are the globals `world`, `players`, `ui` and the rest. |
