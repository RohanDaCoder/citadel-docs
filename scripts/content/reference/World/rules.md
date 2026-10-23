---
title: "world.rules"
url: /docs/citadel/reference/World/rules
---

# world.rules

`world.rules{ fall = true }` switches one on, false off; a rule left out or nil keeps its value, and a number or a string is an error. `world.rules()` reads them.

```
world.rules(opts: { survival: boolean?, fall: boolean?, damage: boolean?, hunger: boolean?, anticheat: boolean?, day_cycle: boolean?, redstone: boolean? }?) → Rules
```


## Parameters


## Returns


## Used in
- [``world.rules{ fall = 0 }` does not turn the rule off.`API basics](/docs/citadel/api-basics)
- [`- Whether the sun moves is a rule: `world.rules{ day_cycle = true }` runs`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`- On a `mode: full` world, and after `world.rules{ survival = true }`, the`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [``world.rules{ redstone = false }` stops every signal in a room. See "Room`Custom blocks](/docs/citadel/custom-blocks)
- [``world.rules{ survival = true }`.`Game data](/docs/citadel/game-data)
- [`world and after `world.rules{ survival = true }`: each kind spawns by the`Game data](/docs/citadel/game-data)
- [`world.rules{ fall = true } -- landings past three blocks cost health`Room rules](/docs/citadel/room-rules)
- [`world.rules{ damage = true } -- the world hurts: void, fire, lava, drowning, suffocation, cactus`Room rules](/docs/citadel/room-rules)
