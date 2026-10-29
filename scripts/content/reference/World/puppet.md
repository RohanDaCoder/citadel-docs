---
title: "world.puppet"
url: /docs/citadel/reference/World/puppet
---

# world.puppet

Places a mob's body with no mind of its own that the script moves; its name tag always shows. An error when this game has no such mob kind.

```
world.puppet(opts: { kind: string, at: Vec3?, rotation: BodyRotation?, name: Text? }) → Puppet
```


## Parameters


## Returns


## Used in
- [`| A mob appearance moved entirely by the pack | `world.puppet` | Uses a mob body without its AI or gameplay simulation. |`Displays](/docs/citadel/displays)
- [`local p = world.puppet{ kind = "horse", at = vec3(0.5, 65, -100.5), rotation = { yaw = 90 }, name = { "Lightning", color = "gold" } } -- name is text`NPCs](/docs/citadel/npcs)
