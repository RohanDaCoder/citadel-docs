---
title: 'time global'
description: 'Clocks for a pack: a callback every tick, one every few seconds, and the seconds since the pack started.'
---

Clocks for a pack: a callback every tick, one every few seconds, and the seconds since the pack started.

Part of the [Terrain generation](/world/terrain-generation/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`on_tick`](/ref/time/on_tick/) | Calls `fn` every tick, 20 times a second, with the tick number; keep it short. |
| [`every`](/ref/time/every/) | Calls `fn` every `seconds`, precise to 1 ms and never drifting; use it for music. |
| [`now`](/ref/time/now/) | Seconds since the pack started. |
