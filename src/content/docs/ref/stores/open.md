---
title: 'stores.open'
description: 'Returns the experience''s one store'
---

Part of [`stores`](/ref/stores/).

```luau
stores.open() → DurableStore
```

Returns the experience's one store. It takes no id; passing one is an error.

## Returns

- [`DurableStore`](/ref/DurableStore/)

## Used in

> "local s = stores.open()" — [Time and tweens](/world/world-state/)
> "bytes raise an error instead of being replaced. Use `stores.open():blob_put` for" — [Storage](/systems/storage/)
> "local scores = stores.open()" — [Shared stores](/systems/shared-stores/)
> "- `stores.open()` returns the experience's store. Passing an id is an error." — [Shared stores](/systems/shared-stores/)
