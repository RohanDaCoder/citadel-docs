---
title: "npc:look_at"
description: "Where it stands; live, so setting it moves the NPC"
---

Part of [`Npc`](/ref/Npc/).

```luau
npc:look_at(pos: Vec3)
```

Where it stands; live, so setting it moves the NPC. A riding NPC reads the seat's position. Partial writes preserve other angles; nil after removal. Bodies have no roll. Turns head and body toward a point.

## Parameters

| Name  | Type                 | Required |
| ----- | -------------------- | -------- |
| `pos` | [`Vec3`](/ref/Vec3/) | yes      |
