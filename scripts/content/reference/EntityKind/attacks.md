---
title: "entityKind.attacks"
url: /docs/citadel/reference/EntityKind/attacks
---

# entityKind.attacks

Whether its hits hurt players. `nil`: on for a kind with `spawn = true`, else the room's `damage` rule. The kind's own setting is stronger than the room's rule. It covers the kind's own hit, its arrow (also after the shooter died) and a creeper's blast. `false` stops the damage to players only: a blast still breaks blocks.

```
entityKind.attacks: boolean?
```
