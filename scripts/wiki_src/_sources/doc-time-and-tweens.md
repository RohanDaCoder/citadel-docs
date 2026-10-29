# SOURCE: Time and tweens

```luau
time.on_tick(function(tick) end) -> connection    -- 20 times a second; keep it short
time.every(seconds, fn) -> connection    -- precise (1 ms), never drifts; use it for music
task.delay(seconds, fn, ...) -> thread    -- once, later; cancel with task.cancel(thread)
connection:cancel()    -- stops it; every connection has this and only this
time.now()    -- seconds since the pack started
os.time()    -- whole seconds since 1970 (UTC), the wall clock
os.date("!*t")    -- that time as { year, month, day, hour, min, sec, wday }; "!" is UTC
```
`time.now()` starts again at zero when the pack does. Use it for what
happens while the pack runs: a race, a cooldown. For something that ends
after a restart, such as a rental of a week, keep an `os.time()` in
`stores` and compare with it. It is UTC, so every server of an
experience reads the same clock, whatever its region:
```luau
local s = stores.open()
local ends, version = s:get("rent:" .. player.uuid)
if not ends or os.time() >= ends then          -- over, even if no server ran meanwhile
    s:set("rent:" .. player.uuid, os.time() + 7 * 24 * 3600, version)
end
```
## Tween
`tween` eases a live number, `vec3`, `color` or `rotation` field, once a tick, such as
a display’s `at` or a player’s `speed`.
```luau
tween(door, { at = door.at + vec3(0, 3, 0) }, { duration = 0.5, easing = "out" })
tween(bar, { progress = 0 }, { duration = 30, on_done = function() ui.title{ title = "Time" } end })
local t = tween(sign, { scale = 2, color = "gold", rotation = { yaw = 90 } }, { duration = 1 })    -- a number is every axis of a vec3; a name is its colour
t:cancel()    -- leaves it where it got to
t.done    -- true once it landed
```
`easing` is `"linear"` (the default), `"in"`, `"out"`, `"in_out"` or
`"bounce"`. A `duration` that is not a number, or an `easing` that is not
one of these names, is an error. A display’s own `animate` tweens on the client: smoother, but
1.19.4 and later only. Use `tween` for everything else and every client.
