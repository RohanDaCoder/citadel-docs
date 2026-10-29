---
title: "models.new"
url: /docs/citadel/reference/models/new
---

# models.new

Makes a model named `name` from the parts `fn` builds and returns it. Call it at the top of the script; from a callback it is an error.

```
models.new(name: string, fn: (m: ModelBuild) -> ()) → Model
```


## Parameters


## Returns


## Used in
- [`local belt = models.new("belt", function(m)`Custom blocks](/docs/citadel/custom-blocks)
- [`| Reusable appearance and named animations | `models.new` | Defines an asset for visuals or simulated entities. |`Displays](/docs/citadel/displays)
- [`looks = models.car, -- a model from models.new`Displays](/docs/citadel/displays)
- [`local car = models.new("car", function(m)`3D models](/docs/citadel/3d-models)
- [`- Make models while the pack loads. `models.new` in a callback is an error.`3D models](/docs/citadel/3d-models)
- [`local rex = models.new("rex", function(m)`Custom entities](/docs/citadel/custom-entities)
