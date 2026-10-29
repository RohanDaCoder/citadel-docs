---
title: "Lighting"
url: /docs/citadel/lighting
---

# Lighting

```luau
world.light{
    { at = vec3(4, 65, -2), level = 12 },   -- 1 to 15 (15 by default), in the air where it shines
    { at = vec3(0, 70, 0) },
}

```
- Light drops one level per block, like block light. Solid blocks stop it.
- The light has no colour. For colour, put coloured blocks or a glowing screen under it.
- The server never sees this light. The world’s real light does not change.
- It needs clients 1.14 and later. Older clients ignore it. A pack that depends on it sets `min_client: "1.14"`.
- A block change can erase the light near it. While the light moves, call `world.light` every tick or two.
