---
title: 'Npc type'
description: 'A player-shaped entity every client from 1.8 sees, from world.npc; it can walk, talk, hold items, wear armour and ride.'
---

A player-shaped entity every client from 1.8 sees, from `world.npc`; it can walk, talk, hold items, wear armour and ride.

## Functions

| Call | Purpose |
| --- | --- |
| [`look_at`](/ref/Npc/look_at/) | Where it stands; live, so setting it moves the NPC. A riding NPC reads the seat's position. Partial writes preserve other angles; nil after removal. Bodies have no roll. Turns head and body toward a point. |
| [`swing`](/ref/Npc/swing/) | Plays the arm swing animation. |
| [`hold`](/ref/Npc/hold/) | Puts an item in the main hand; nil or false empties it. An error on an unknown item. |
| [`say`](/ref/Npc/say/) | Sends a chat line "<name> ..." to the room, or just the words for an NPC with no name. |
| [`walk`](/ref/Npc/walk/) | Walks the points by itself, facing where it goes; nil stops it. |
| [`wear`](/ref/Npc/wear/) | Puts armour on it, head first; each piece is an item. |
| [`ride`](/ref/Npc/ride/) | Sits in a seat as `player:ride` does, and never drives; `false` when somebody sits there. |
| [`dismount`](/ref/Npc/dismount/) | Gets off where it sits; set `at` after it to put it somewhere else. |
| [`move`](/ref/Npc/move/) | Removes the NPC. Sets position and optional rotation together. |
| [`destroy`](/ref/Npc/destroy/) |  |

## Fields

| Field | Purpose |
| --- | --- |
| [`npc.id: number`](/ref/Npc/id/) | The entity id, what `players.on_click` reports in `hit.entity_id`. |
| [`npc.name: string`](/ref/Npc/name/) | Whether it is still present. Read-only. "" for one made with no name, which has no name tag. |
| [`npc.walking: boolean`](/ref/Npc/walking/) | True while it walks a path, until the last point; never false with `loop`. |
| [`npc.pose: NpcPose`](/ref/Npc/pose/) | How the body is held; live. |
| [`npc.riding: boolean`](/ref/Npc/riding/) | Whether it sits in a seat; live. |
