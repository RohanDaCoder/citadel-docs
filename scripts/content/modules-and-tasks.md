---
title: "Modules and tasks"
url: /docs/citadel/modules-and-tasks
---

# Modules and tasks

`spawn`, `delay` and `defer` accept either a function or a suspended coroutine,
forward all arguments (including nils), and return that coroutine. `spawn`
runs immediately until the task yields or returns. `task.cancel` also works
after the task has called `task.wait`; canceling a running thread is an error.
Canceling a task stops its script, but cannot undo I/O already submitted.
`wait` and `delay` use elapsed real time in both full and lite mode. Unlike
Roblox’s heartbeat-based scheduling, they resume once the requested time has
passed and the script scheduler can run them, without rounding to Minecraft’s
50 ms ticks. Zero or negative seconds yield until the next scheduler turn.
Use `time.on_tick` for work tied to world ticks. The actual wait may be longer
under load. Durations must be finite and within the supported clock
range; invalid values raise catchable errors. `time.every` remains a repeating
timer returning a connection, and can cancel itself inside its callback.
**Initialization exception:** tasks spawned, deferred or delayed while
`main.luau` loads start only after initialization commits. This preserves the
pack’s atomic startup. The top level may `task.wait`, but cannot wait for one
of those child tasks to finish before startup.
Ordinary event callbacks and `main.luau` may call `task.wait`. Synchronous ask
handlers and a module’s top level may not. `require` resolves from the pack
root, caches by canonical file path, rejects cycles, and rejects symlinks that
lead outside the pack. A module returning nil is cached as true.
