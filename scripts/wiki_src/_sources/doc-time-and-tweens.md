# SOURCE: Time and tweens

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
`easing` is `"linear"` (the default), `"in"`, `"out"`, `"in_out"` or
`"bounce"`. A `duration` that is not a number, or an `easing` that is not
one of these names, is an error. A display’s own `animate` tweens on the client: smoother, but
1.19.4 and later only. Use `tween` for everything else and every client.
