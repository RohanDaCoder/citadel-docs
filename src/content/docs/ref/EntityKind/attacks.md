---
title: 'entityKind.attacks'
description: 'Whether its hits hurt players'
---

Part of [`entityKind`](/ref/EntityKind/).

```luau
entityKind.attacks: boolean ?
```

Whether its hits hurt players. `nil`: on for a kind with `spawn = true`, else the room's `damage` rule. The kind's own setting is stronger than the room's rule. It covers the kind's own hit, its arrow (also after the shooter died) and a creeper's blast. `false` stops the damage to players only: a blast still breaks blocks.
