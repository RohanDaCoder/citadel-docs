---
title: 'chunk:paste'
description: 'Clipped to this chunk; air is skipped unless air is true'
---

Part of [`Chunk`](/ref/Chunk/).

```luau
chunk:paste(schem: Schematic, origin: Vec3, opts: { air: boolean ?, part: string ? }?)
```

Clipped to this chunk; air is skipped unless `air` is true. `part` names the paste for `citadel render --part` and `citadel check`; the build's own `b:part`s are then inside it ("house/roof").

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `schem` | [`Schematic`](/ref/Schematic/) | yes |
| `origin` | [`Vec3`](/ref/Vec3/) | yes |
| `opts` | `{ air: boolean ?, part: string ? }` | no |

## Used in

> "chunk:paste(cottage, vec3(0, 64, 0) + cottage.min) -- only the part in this chunk" — [Guide: Build a cottage](/guides/guide-build-a-cottage/)
> "`chunk:paste` puts the part of the cottage that falls in each chunk as" — [Guide: Build a cottage](/guides/guide-build-a-cottage/)
> "--   chunk:paste(schem, origin)    a schematic, clipped to the chunk" — [Blocks and terrain](/world/terrain-generation/)
> "- `chunk:paste` and `world.paste` take a build like any schematic. Make it" — [Blocks and terrain](/world/terrain-generation/)
