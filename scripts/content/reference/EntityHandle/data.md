---
title: "entityHandle.data"
url: /docs/citadel/reference/EntityHandle/data
---

# entityHandle.data

A pack-defined entity's attached record. Nested edits write through. Saved with persist = "save". Built-in entities raise an error on access. on_steer/on_tick views expire after the callback batch; copy to keep a snapshot.

```
entityHandle.data: DataView
```
