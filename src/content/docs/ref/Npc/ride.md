---
title: "npc:ride"
description: "Sits in a seat as player:ride does, and never drives; false when somebody sits there."
---

Part of [`Npc`](/ref/Npc/).

```luau
npc:ride(thing: MountTarget, opts: { seat: number ? }?) → boolean
```

Sits in a seat as `player:ride` does, and never drives; `false` when somebody sits there.

## Parameters

| Name    | Type                               | Required |
| ------- | ---------------------------------- | -------- |
| `thing` | [`MountTarget`](/ref/MountTarget/) | yes      |
| `opts`  | `{ seat: number ? }`               | no       |

## Returns

- `boolean`

## Used in

> "npc:ride(c) -- an npc at the wheel; it does not drive (see npcs)" — [Displays](/ui/displays/)
> "- A seat holds one rider. `player:ride` and `npc:ride` return `false` for a" — [Displays](/ui/displays/)
