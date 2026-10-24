---
title: 'entityHandle:play'
description: 'Model size: reads vec3; write a positive number or equal-axis vec3'
---

Part of [`EntityHandle`](/ref/EntityHandle/).

```luau
entityHandle:play(animation: string, opts: { speed: number ? }?)
```

Model size: reads vec3; write a positive number or equal-axis vec3. Nil without a model. Plays a model entity's animation from the start; on the one already playing, `speed` only changes its speed.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `animation` | `string` | yes |
| `opts` | `{ speed: number ? }` | no |
