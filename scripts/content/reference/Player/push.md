---
title: "player:push"
url: /docs/citadel/reference/Player/push
---

# player:push

A shove in blocks per tick, on top of what they are doing.

```
player:push(velocity: Vec3)
```


## Parameters


## Used in
- [`player:push(vec3(0, 1, 0)) -- a shove, in blocks per tick, on top of what they are doing`Body and movement](/docs/citadel/body-and-movement)
- [`- `player:push` and a movement effect (`speed`, `jump_boost`, `levitation`, `slow_falling`, `dolphins_grace`) exempt the player while they last. `player:teleport` is always allowed.`Room rules](/docs/citadel/room-rules)
- [`hit.player:push(player:look() * 0.5 + vec3(0, 0.3, 0))`Room rules](/docs/citadel/room-rules)
