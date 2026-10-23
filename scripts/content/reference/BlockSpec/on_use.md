---
title: "blockSpec.on_use"
url: /docs/citadel/reference/BlockSpec/on_use
---

# blockSpec.on_use

The hooks. Writing one is what asks for it — there is no flag beside `on_random_tick` saying the random pass may land here.

```
blockSpec.on_use((block: BlockAt, player: Player?, held: string?, base: (...any) -> any) -> Used?) → ?
```


## Parameters


## Returns
