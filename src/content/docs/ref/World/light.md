---
title: "world.light"
description: "Sends players light no block makes, 1 to 15 a source; each call replaces the last, {} ends it"
---

Part of [`world`](/ref/World/).

```luau
world.light(sources: { LightSource })
```

Sends players light no block makes, 1 to 15 a source; each call replaces the last, `{}` ends it. 1.14 and later.

## Parameters

| Name      | Type              | Required |
| --------- | ----------------- | -------- |
| `sources` | `{ LightSource }` | yes      |

## Used in

> "\| `light` \| `world.light` \| 1.14 \|" — [Client versions](/appendix/client-versions/)
> "`world.light` sends players light that no block makes. Each call replaces the" — [Lighting](/ui/displays/)
> "last call's sources. `world.light{}` removes them all." — [Lighting](/ui/displays/)
