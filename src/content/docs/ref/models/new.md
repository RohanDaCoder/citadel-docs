---
title: "models.new"
description: "Makes a model named name from the parts fn builds and returns it"
---

Part of [`models`](/ref/models/).

```luau
models.new(name: string, fn: (m: ModelBuild) -> ()) → Model
```

Makes a model named `name` from the parts `fn` builds and returns it. Call it at the top of the script; from a callback it is an error.

## Parameters

| Name   | Type                     | Required |
| ------ | ------------------------ | -------- |
| `name` | `string`                 | yes      |
| `fn`   | `(m: ModelBuild ) -> ()` | yes      |

## Returns

- [`Model`](/ref/Model/)

## Used in

> "local belt = models.new("belt", function(m)" — [Custom blocks](/world/custom-blocks/)
> "\| Reusable appearance and named animations \| `models.new` \| Defines an asset for visuals or simulated entities. \|" — [Displays](/ui/displays/)
> "looks = models.car, -- a model from models.new" — [Displays](/ui/displays/)
> "local car = models.new("car", function(m)" — [3D models](/ui/displays/)
> "- Make models while the pack loads. `models.new` in a callback is an error." — [3D models](/ui/displays/)
> "local rex = models.new("rex", function(m)" — [Custom entities](/entities/custom-entities/)
