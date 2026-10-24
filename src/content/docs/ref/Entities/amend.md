---
title: "entities.amend"
description: "The game's own content only — never another pack's."
---

Part of [`entities`](/ref/Entities/).

```luau
entities.amend(name: string, hooks: EntityAmendSpec, options: EntityAmendOptions ?)
```

The game's own content only — never another pack's.

## Parameters

| Name      | Type                                             | Required |
| --------- | ------------------------------------------------ | -------- |
| `name`    | `string`                                         | yes      |
| `hooks`   | [`EntityAmendSpec`](/ref/EntityAmendSpec/)       | yes      |
| `options` | [`EntityAmendOptions`](/ref/EntityAmendOptions/) | no       |

## Used in

> "`game.entities.amend("cow", { ... })`." — [Game data](/world/game-data/)
> "game.entities.amend("pig", {" — [Custom entities](/entities/custom-entities/)
> "- Profiles run no callbacks. To change gameplay, use `game.entities.amend(name, hooks)` and `game.entities.define(spec)`." — [Custom entities](/entities/custom-entities/)
