---
title: 'Hitbox type'
description: 'An invisible box a player can click, and a wall when solid, from world.hitbox (1.19.4 and later).'
---

An invisible box a player can click, and a wall when solid, from `world.hitbox` (1.19.4 and later).

## Functions

| Call | Purpose |
| --- | --- |
| [`destroy`](/ref/Hitbox/destroy/) | Removes the hitbox, and its wall when solid. |

## Fields

| Field | Purpose |
| --- | --- |
| [`hitbox.id: number`](/ref/Hitbox/id/) | Its entity id, what `players.on_click` reports in `hit.entity_id`. |
| [`hitbox.at: Vec3`](/ref/Hitbox/at/) | Its bottom centre; write it to move the hitbox, and its wall when solid. |
