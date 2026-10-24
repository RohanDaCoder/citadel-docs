---
title: "BlockAt type"
description: "The block a hook was called about"
---

The block a hook was called about. Reads are fields and acts are methods. The reads are **live** — the world as it is right now — and everything that changes the world is carried out by the engine the moment the hook returns, in the order it was asked for.

## Functions

| Call                                 | Purpose                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------ |
| [`get`](/ref/BlockAt/get/)           | The block one face away, by name; nil where that chunk is not in memory. |
| [`set`](/ref/BlockAt/set/)           | Puts another block at this position.                                     |
| [`destroy`](/ref/BlockAt/destroy/)   | Takes it out, leaving nothing.                                           |
| [`become`](/ref/BlockAt/become/)     | **The door**: this block stops being a block, and that entity appears.   |
| [`drop`](/ref/BlockAt/drop/)         | A name, or an item table: a pack item keeps its id.                      |
| [`schedule`](/ref/BlockAt/schedule/) | Asks for this block's `on_tick`, `tick_every` seconds from now.          |
| [`notify`](/ref/BlockAt/notify/)     | Tells the six neighbours this block changed.                             |

## Fields

| Field                                                 | Purpose                                                                                                                                                                                                                          |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`blockAt.data: DataView`](/ref/BlockAt/data/)        | What this block remembers beyond its state; kept with the position, saved with the chunk, and gone when the block goes. Nested writes are tracked; whole-record assignment is supported. Copy before keeping it beyond the hook. |
| [`blockAt.at: Vec3`](/ref/BlockAt/at/)                | The block's position; a live read.                                                                                                                                                                                               |
| [`blockAt.name: string`](/ref/BlockAt/name/)          | The block's name with its namespace, such as "rave:crate"; a live read.                                                                                                                                                          |
| [`blockAt.room: number`](/ref/BlockAt/room/)          | Which room the block is in.                                                                                                                                                                                                      |
| [`blockAt.state: number`](/ref/BlockAt/state/)        | Which of this definition's states it is in, counting from 1. Writable, and bounds-checked against the definition's own `looks` list: it _is_ the block state, so a crop's stages cost nothing.                                   |
| [`blockAt.facing: Facing ?`](/ref/BlockAt/facing/)    | A facing block's front: "north", "south", "west", "east"; nil otherwise. Writable.                                                                                                                                               |
| [`blockAt.powered: boolean ?`](/ref/BlockAt/powered/) | Whether a redstone signal reaches it: what a lamp asks. A live read; nil where the chunk is not loaded.                                                                                                                          |
