---
title: 'Builder type'
description: 'What world.build hands the function it is given'
---

What `world.build` hands the function it is given. Coordinates are whole blocks of the build's own and may be negative; later writes win.

## Functions

| Call | Purpose |
| --- | --- |
| [`block`](/ref/Builder/block/) | Sets one block of the build; later writes win. |
| [`box`](/ref/Builder/box/) | Inclusive corners, in any order, like `chunk:fill`. |
| [`line`](/ref/Builder/line/) | Every block the straight line between the ends passes through. |
| [`part`](/ref/Builder/part/) | What `fn` writes is a named part, found by `citadel render --part` and `citadel check` once pasted. Nested calls name "tower/roof". |
