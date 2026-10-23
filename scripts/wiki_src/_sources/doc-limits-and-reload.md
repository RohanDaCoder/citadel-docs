# SOURCE: Limits and reload

**The tick budget.** A pack’s tick and event callbacks share part of each
tick. Set it with `budget_ms` in the pack’s `citadel.yml`. The default is
**2 ms**.
- It covers `time.on_tick`, `time.every` and the survival events
(`world.on_block_break` and the rest).
- It does not cover `players.on_join`, input events (`on_click`, `on_chat`,
commands), or task threads. Those keep the 100 ms runaway limit. Chunk
callbacks keep their separate 2 s limit.
- It counts work, not time spent waiting.
citadel.yml
When the budget runs out mid-batch:
- Ordinary events retain their original arguments and remaining listeners
until the next budget window. Canceling a subscription also removes its
pending delivery. The bounded event queue still applies.
- `time.on_tick` coalesces missed ticks: remaining listeners resume with the
latest tick number. It does not replay every elapsed tick.
- Socket messages stay queued until their callback can run.
- A `time.every` timer that does not fit retains its place among due timers.
- Nothing is killed. A started callback always finishes.
Read the numbers with `citadel.budget()`:
```luau
local b = citadel.budget()
print(b.of)        -- 2, the ms this pack gets per tick
print(b.used)      -- what the last tick spent
print(b.peak)      -- the most any tick has spent
print(b.skipped)   -- callbacks not run for want of budget, since the script started
print(b.dropped)   -- events this pack never saw; see below
print(b.slowest)   -- { hook = "on_tick", ms = 4.1 }, or nil
print(b.asks)      -- what the engine's questions cost this pack; see below

citadel.on_slow(function(slow)
    print(slow.hook, slow.used, slow.of, slow.skipped)   -- "on_tick" 2.4 2 3
end)
```
Hook names are short: `"on_tick"`, `"every"`, or the event’s name
(`"block_break"`, `"pickup"`). `on_slow` runs at most once a second. The
server log shows the pack, hook and time, at most once every five seconds.
Going over is not an error. Do less per tick, or raise `budget_ms`.
**`b.dropped` counts lost ordinary events.** Each pack retains at most 4096
ordinary events; overflow drops the oldest ordinary event and logs the pack.
Joins, leaves, deaths and respawns are retained in order and never evicted by
ordinary traffic or skipped because the tick budget was spent. They carry the
original player session, so a delayed leave still has its `player.data` after
a reconnect. This is in-process delivery, not a durable journal across a
server crash. Keep lifecycle callbacks short so their retained backlog drains.
**`b.asks` counts the engine’s questions.** An **ask** is a
cancellable event, such as “may this player break this block”. The engine
waits a few milliseconds for the answer. Three exist: `players.on_break`
(kind `"break"`), `players.on_place` (kind `"place"`) and
`players.on_damage` (kind `"damage"`). With no answer in time, the engine
denies the protected action. With no protection listener registered, the
action follows the normal game rules. A listener that completes and returns
nil still allows the action; an error or missing answer does not.
Counters are totals; watch them per kind:
```luau
time.every(60, function()
    for kind, count in citadel.budget().asks.kinds do
        if count.missed > count.answered then
            citadel.log(`slow at {kind}: {count.missed} of {count.asks} missed`)
        end
    end
end)
```
The log names a kind you keep missing. Miss it too often and the engine
**stops asking you** that kind. It then takes the default, logs this once,
and sets `disabled`.
Ask handler rules:
- Answer at once. Never call `task.wait` in one.
- Answering costs tick budget, under the hook name `"ask"`.
- A spent budget does not stop an ask from being answered.
Saving any `.luau` file in the pack, at any depth, restarts the pack’s
script. The server keeps running.
- Players stay connected.
- Initialization stages recipes, assets, layouts, block/entity registrations,
commands, model registrations, asks, spawn settings and queued world actions.
A failed entry script discards these drafts and resumes the old script.
- The entry must finish within 30 seconds, including any `task.wait` or read
requests. `task.spawn` work starts after successful initialization.
- Local storage is flushed before loading the replacement, and the old VM
finishes cleanup before the replacement starts callbacks.
- Writes to shared stores, purchase prompts/acks and `storage.flush` belong
in `task.spawn` or callbacks, because external writes cannot be rolled back.
Existing-world/player side effects should also be performed in callbacks.
- On success, the old script’s timers and connections end.
- `players.on_join` runs again for every online player. Make it safe to run
twice.
**A reload keeps the world.** Every existing chunk stays, in script and
terrain worlds.
A changed `world.on_generate`, `seed` or `terrain` applies only to chunks
generated **from here on**. To regenerate the whole map, stop the server,
delete the world folder, and start it again. The log names that folder the first
time a script world reloads.
