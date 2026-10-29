---
title: 'blockSpec.on_neighbour'
description: 'A neighbour changed; from is its position and announced the block name the notifier announced itself as.'
---

Part of [`blockSpec`](/ref/BlockSpec/).

```luau
blockSpec.on_neighbour((block: BlockAt, from: Vec3, announced: string, base: (... any) -> any) -> ()) → ?
```

A neighbour changed; `from` is its position and `announced` the block name the notifier announced itself as.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `(block` | `BlockAt , from: Vec3 , announced: string , base: (... any ) -> any ) -> ()` | yes |

## Returns

- `?`
