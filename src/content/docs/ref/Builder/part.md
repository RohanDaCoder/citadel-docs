---
title: 'builder:part'
description: 'What fn writes is a named part, found by citadel render --part and citadel check once pasted'
---

Part of [`Builder`](/ref/Builder/).

```luau
builder:part(name: string, fn: () -> ())
```

What `fn` writes is a named part, found by `citadel render --part` and `citadel check` once pasted. Nested calls name "tower/roof".

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `name` | `string` | yes |
| `fn` | `() -> ()` | yes |
