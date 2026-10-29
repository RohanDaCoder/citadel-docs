---
title: 'entitySpec.sounds'
description: 'physics = "living" only: sound names for its hurt, its death and its idle sound, vanilla or "<pack>.<file>"'
---

Part of [`entitySpec`](/ref/EntitySpec/).

```luau
entitySpec.sounds: ({ hurt: string ?, death: string ?, ambient: string ? } | false)?
```

physics = "living" only: sound names for its hurt, its death and its idle sound, vanilla or "<pack>.<file>". false or nil: silent.
