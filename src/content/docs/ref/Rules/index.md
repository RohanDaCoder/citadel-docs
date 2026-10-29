---
title: 'Rules type'
description: 'Which parts of the player simulation this room runs'
---

Which parts of the player simulation this room runs. All on for a `mode: full` server, all off on a pack server until the pack says. `survival` is the whole game: digging and its drops, placing, the inventory and crafting, respawning — and it turns fall, damage, hunger and day_cycle on. `anticheat` is on everywhere until a pack turns it off, and so is `redstone`: off, no signal moves in the room.

`{ survival: boolean, fall: boolean, damage: boolean, hunger: boolean, anticheat: boolean, day_cycle: boolean, redstone: boolean }`
