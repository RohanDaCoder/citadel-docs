---
title: "entityHandle:play"
url: /docs/citadel/reference/EntityHandle/play
---

# entityHandle:play

Model size: reads vec3; write a positive number or equal-axis vec3. Nil without a model. Plays a model entity's animation from the start; on the one already playing, `speed` only changes its speed.

```
entityHandle:play(animation: string, opts: { speed: number? }?)
```


## Parameters
