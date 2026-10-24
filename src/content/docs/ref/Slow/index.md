---
title: "Slow type"
description: "One overrun, as citadel.on_slow is handed it."
---

One overrun, as `citadel.on_slow` is handed it.

## Fields

| Field                                        | Purpose                                                                          |
| -------------------------------------------- | -------------------------------------------------------------------------------- |
| [`slow.hook: string`](/ref/Slow/hook/)       | The short name of the hook that ran out: "on_tick", "every", or the event's own. |
| [`slow.of: number`](/ref/Slow/of/)           | The pack's budget per tick, in milliseconds: `budget_ms` in citadel.yml.         |
| [`slow.used: number`](/ref/Slow/used/)       | Milliseconds the pack spent in the tick that ran out.                            |
| [`slow.skipped: number`](/ref/Slow/skipped/) | Callbacks not run for want of budget, since the script started.                  |
