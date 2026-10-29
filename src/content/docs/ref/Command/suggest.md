---
title: 'command:suggest'
description: 'What arg offers from now on: a list, a function, or nil or false for nothing.'
---

Part of [`Command`](/ref/Command/).

```luau
command:suggest(arg: string, words: ({ Suggestion } | Suggester | false)?)
```

What `arg` offers from now on: a list, a function, or nil or false for nothing.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `arg` | `string` | yes |
| `words` | `({ Suggestion } \| Suggester \| false )` | no |

## Used in

> "command:suggest(arg, words)   -- a list, a function, or nil or false for nothing: what `arg` offers from now on" — [Commands](/systems/commands/)
> "- **The command** handle: `command:suggest` sends the new list to every" — [Commands](/systems/commands/)
