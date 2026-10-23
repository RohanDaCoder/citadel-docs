---
title: "chunk:get"
url: /docs/citadel/reference/Chunk/get
---

# chunk:get

Chunk X coordinate (16 blocks each). Chunk Z coordinate (16 blocks each). The chunk's lowest corner, inclusive; y runs 0..255 or the game version's height. The chunk's highest corner, inclusive. Returns the block there now, by name; air outside the chunk.

```
chunk:get(pos: Vec3) → string
```


## Parameters


## Returns


## Used in
- [`-- chunk:get(pos) what is there now, by name; air outside the chunk`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`(not loaded), not `"air"`. Inside `on_generate`, `chunk:get` always works.`Blocks and terrain](/docs/citadel/blocks-and-terrain)
