---
title: "ModelDisplay type"
description: "A model visual in a room"
---

A model visual in a room. Shares at, rotation, scale, alive and move with other visuals; adds named animations and model materials.

## Functions

| Call                                    | Purpose                                                                          |
| --------------------------------------- | -------------------------------------------------------------------------------- |
| [`move`](/ref/ModelDisplay/move/)       | Place and turn it in one step, every part and seat together.                     |
| [`play`](/ref/ModelDisplay/play/)       | Starts an animation; replaying the current one changes speed without restarting. |
| [`stop`](/ref/ModelDisplay/stop/)       | Where it is; the parts stay as they are.                                         |
| [`destroy`](/ref/ModelDisplay/destroy/) | Removes the model from the room.                                                 |

## Fields

| Field                                                               | Purpose                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`modelDisplay.id: number`](/ref/ModelDisplay/id/)                  | What `player:ride(model)` is handed; the seat is picked from `seats`.                                                                                                                                                                                                            |
| [`modelDisplay.paint: { [string]: Ink }`](/ref/ModelDisplay/paint/) | Whether it is still present. Read-only. Where it stands; live, and each write is a move of its own. Partial writes preserve other angles; nil after removal. Reads vec3; write a number or equal-axis vec3 for uniform size. Nil when gone. Material name to colour; write-only. |
