---
title: "world.npc"
url: /docs/citadel/reference/World/npc
---

# world.npc

Places a player-shaped entity every client from 1.8 sees; removed when the script ends or reloads.

```
world.npc(opts: { name: string?, at: Vec3?, rotation: BodyRotation?, skin: (string | { value: string, signature: string } | false)?, }) → Npc
```


## Parameters


## Returns


## Used in
- [``world.npc{ skin = }`. The signature is optional.`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`| A player-shaped character with a skin and equipment | `world.npc` | Adds avatar-specific behavior. |`Displays](/docs/citadel/displays)
- [`local n = world.npc{ name = "Dealer", at = vec3(0.5, 65, 4.5), rotation = { yaw = 180, pitch = 0 },`NPCs](/docs/citadel/npcs)
