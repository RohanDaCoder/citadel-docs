---
title: 'Budget type'
description: 'What a pack''s tick and event callbacks are allowed per tick, together, and what it did with it'
---

What a pack's tick and event callbacks are allowed per tick, together, and what it did with it. Milliseconds throughout.

## Fields

| Field | Purpose |
| --- | --- |
| [`budget.of: number`](/ref/Budget/of/) | `budget_ms` in citadel.yml; 2 by default. |
| [`budget.used: number`](/ref/Budget/used/) | What the last tick spent. |
| [`budget.peak: number`](/ref/Budget/peak/) | The most any tick has spent. |
| [`budget.skipped: number`](/ref/Budget/skipped/) | Callbacks not run for want of budget, since the script started. |
| [`budget.dropped: number`](/ref/Budget/dropped/) | Ordinary events lost to queue overflow. Joins, leaves, deaths and respawns are retained with their original player sessions. |
| [`budget.slowest: { hook: string, ms: number }?`](/ref/Budget/slowest/) | The slowest single callback so far, by short hook name. |
| [`budget.asks: Asks`](/ref/Budget/asks/) | The engine's questions to this pack, and what it did with those. |
