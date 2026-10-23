---
title: "npc:look_at"
url: /docs/citadel/reference/Npc/look_at
---

# npc:look_at

Where it stands; live, so setting it moves the NPC. A riding NPC reads the seat's position. Partial writes preserve other angles; nil after removal. Bodies have no roll. Turns head and body toward a point.

```
npc:look_at(pos: Vec3)
```


## Parameters
