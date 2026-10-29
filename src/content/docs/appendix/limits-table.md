---
title: 'Limits'
description: 'Every numeric limit in Citadel in one table — tick budgets, load times, event queues, stores, blobs, leases, builds and generation.'
---

:::note[In short]
every number the engine enforces, in one place. Each row
links to the page that explains what happens at the edge.
:::

| Limit | Value | What it bounds | Details |
| --- | --- | --- | --- |
| Tick budget | 2 ms default (`budget_ms`) | A pack's tick and event callbacks per tick | [Limits](/systems/limits/) |
| Runaway limit | 100 ms | Joins, input events, commands, task threads | [Limits](/systems/limits/) |
| Chunk callback | 2 s | `on_generate` / `on_populate` per chunk | [Terrain generation](/world/terrain-generation/) |
| Chunk wait | 60 s | The engine's wait for a chunk to be made; then it is air | [Terrain generation](/world/terrain-generation/) |
| Entry script | 5 s between waits, 30 s total | Pack load; past it the load fails | [Runtime](/concepts/runtime/) |
| Event queue | 4096 ordinary events per pack | Overflow drops the oldest and logs | [Limits](/systems/limits/) |
| Ask deadline | 2 ms | `on_break` / `on_place` / `on_damage` answers; miss and the action is denied | [The event model](/concepts/events/) |
| `on_slow` | at most once a second | Budget warnings to the script | [Limits](/systems/limits/) |
| Slow-pack log | at most once every 5 s | Server log lines about budget | [Limits](/systems/limits/) |
| Zone re-trigger | 0.5 s | A route trigger block, after a trip | [Rooms and dimensions](/concepts/rooms-and-dimensions/) |
| Store facts | 1 MiB each, keys 256 B | `stores` values | [Shared stores](/systems/shared-stores/) |
| Store blobs | 32 MiB each, 1,000 per player | `stores` blobs | [Shared stores](/systems/shared-stores/) |
| Hosted storage | 512 MiB + 1 MiB per Java player ever joined | Per experience | [Shared stores](/systems/shared-stores/) |
| Pending store requests | 32 per pack | Concurrent yielding store calls | [Shared stores](/systems/shared-stores/) |
| Lease tokens | 100,000 issued; leases last up to 1 hour | `stores.lease` | [Shared stores](/systems/shared-stores/) |
| Build size | 4,096 16-block cubes (32 MB) in a 256-million-block box | One `world.build` | [Building](/world/building/) |
| `max_health` | 1 to 1024 | `player.max_health` writes | [Health](/players/health/) |
| Player name to `player:connect` | 1 to 128 chars | Server addresses | [Player lifecycle](/players/player-lifecycle/) |
| Camera moves | 20 per second | Camera positioning | [Movement](/players/movement/) |
| Client versions | 1.8 to 26.x join every server | Java clients | [Client versions](/appendix/client-versions/) |

## See also

- [Limits](/systems/limits/) — the budget system in depth.
- [FAQ](/appendix/faq/) — when a limit is why.
