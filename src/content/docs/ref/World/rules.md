---
title: "world.rules"
description: "world.rules{ fall = true } switches one on, false off; a rule left out or nil keeps its value, and a number or a string is an error"
---

Part of [`world`](/ref/World/).

```luau
world.rules(opts: { survival: boolean ?, fall: boolean ?, damage: boolean ?, hunger: boolean ?, anticheat: boolean ?, day_cycle: boolean ?, redstone: boolean ? }?) → Rules
```

`world.rules{ fall = true }` switches one on, false off; a rule left out or nil keeps its value, and a number or a string is an error. `world.rules()` reads them.

## Parameters

| Name   | Type                                                                                                                                              | Required |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `opts` | `{ survival: boolean ?, fall: boolean ?, damage: boolean ?, hunger: boolean ?, anticheat: boolean ?, day_cycle: boolean ?, redstone: boolean ? }` | no       |

## Returns

- [`Rules`](/ref/Rules/)

## Used in

> "`world.rules{ fall = 0 }` does not turn the rule off." — [API basics](/concepts/conventions/)
> "- Whether the sun moves is a rule: `world.rules{ day_cycle = true }` runs" — [Blocks and terrain](/world/terrain-generation/)
> "- On a `mode: full` world, and after `world.rules{ survival = true }`, the" — [Blocks and terrain](/world/terrain-generation/)
> "`world.rules{ redstone = false }` stops every signal in a room. See "Room" — [Custom blocks](/world/custom-blocks/)
> "`world.rules{ survival = true }`." — [Game data](/world/game-data/)
> "world and after `world.rules{ survival = true }`: each kind spawns by the" — [Game data](/world/game-data/)
