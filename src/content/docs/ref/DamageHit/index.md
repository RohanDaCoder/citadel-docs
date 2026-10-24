---
title: 'DamageHit type'
description: 'A hit on a player, before it lands: what players.on_damage hands a pack.'
---

A hit on a player, before it lands: what `players.on_damage` hands a pack.

## Fields

| Field | Purpose |
| --- | --- |
| [`damageHit.amount: number`](/ref/DamageHit/amount/) | Half hearts, before armour. |
| [`damageHit.cause: string`](/ref/DamageHit/cause/) | "fall", "drown", "suffocate", "void", "lava", "fire", "cactus", "starve", "attack", "shot", "blast" or "magic". |
| [`damageHit.by: Player ?`](/ref/DamageHit/by/) | The player who hit, or who shot the arrow. |
| [`damageHit.kind: string ?`](/ref/DamageHit/kind/) | The kind's name ("Skeleton") when a mob did it. |
