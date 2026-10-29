---
title: 'Container type'
description: 'A chest''s stacks: world.container(pos)'
---

A chest's stacks: `world.container(pos)`. A chest a player has open is theirs until it closes — `take` takes nothing, `put` puts nothing.

## Functions

| Call | Purpose |
| --- | --- |
| [`items`](/ref/Container/items/) | The filled slots, in order. |
| [`take`](/ref/Container/take/) | Up to `count` (1 unless you say) of what matches; how many it took. |
| [`put`](/ref/Container/put/) | How many did not fit; 0 when all of it went in. |

## Fields

| Field | Purpose |
| --- | --- |
| [`container.size: number`](/ref/Container/size/) | How many slots the chest has, e.g. 27; 0 once it has gone. |
| [`container.at: Vec3`](/ref/Container/at/) | The chest's block position. |
