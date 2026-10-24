---
title: "player:damage"
description: "A hit in half-hearts: the flash, the sound, the resistance window"
---

Part of [`Player`](/ref/Player/).

```luau
player:damage(amount: number) → boolean
```

A hit in half-hearts: the flash, the sound, the resistance window. `false` on a version with no damage rules.

## Parameters

| Name     | Type     | Required |
| -------- | -------- | -------- |
| `amount` | `number` | yes      |

## Returns

- `boolean`

## Used in

> "player:damage(4) -- a hit: two hearts, the flash, the sound, the resistance window" — [Players](/players/player-lifecycle/)
> "`player:damage`). `message` is the broadcast English death line. `by` is the" — [Players](/players/player-lifecycle/)
> "player:damage(4) -- two hearts, with the flash and the sound; "<name> died" if it was the last" — [Body and movement](/players/movement/)
> "Anything that is not a rule is the pack's job: `player:damage` for a hit," — [Room rules](/world/world-state/)
> "hit.player:damage(2)" — [Room rules](/world/world-state/)
> "- A pack's own `player:damage` is not asked about, in this pack or another." — [Cancelling events](/concepts/events/)
