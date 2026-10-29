---
title: "chunk:paste"
url: /docs/citadel/reference/Chunk/paste
---

# chunk:paste

Clipped to this chunk; air is skipped unless `air` is true. `part` names the paste for `citadel render --part` and `citadel check`; the build's own `b:part`s are then inside it ("house/roof").

```
chunk:paste(schem: Schematic, origin: Vec3, opts: { air: boolean?, part: string? }?)
```


## Parameters


## Used in
- [`chunk:paste(cottage, vec3(0, 64, 0) + cottage.min) -- only the part in this chunk`Guide: Build a cottage](/docs/citadel/guides/build-a-cottage)
- [``chunk:paste` puts the part of the cottage that falls in each chunk as`Guide: Build a cottage](/docs/citadel/guides/build-a-cottage)
- [`-- chunk:paste(schem, origin) a schematic, clipped to the chunk`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`- `chunk:paste` and `world.paste` take a build like any schematic. Make it`Blocks and terrain](/docs/citadel/blocks-and-terrain)
