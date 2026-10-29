---
title: 'Cooldowns'
description: 'Rate-limit commands and actions with player.data and time.now — per-player cooldowns that survive reloads safely and degrade correctly.'
---

:::note[In short]
a cooldown is a per-player timestamp plus a check. Store the
last use in `player.data` and compare against `time.now()` — seconds since
the pack started. `player.data` lives as long as the player is connected,
which is exactly the lifetime a cooldown wants.
:::

## The pattern

```luau
--!strict
local COOLDOWN = 5  -- seconds

commands.add("kit", function(player)
    local last = player.data.kit_at
    if last and time.now() - last < COOLDOWN then
        local wait_for = math.ceil(COOLDOWN - (time.now() - last))
        player:message(`Wait {wait_for}s for your kit.`, "red")
        return
    end
    player.data.kit_at = time.now()
    player:give({ item = "iron_sword", count = 1 })
    player:message("Kit delivered.", "green")
end)
```

Why each piece is what it is:

- **`player.data`** is a table that lives as long as the player is connected.
  It resets when they reconnect, which is the right scope for gameplay
  cooldowns — no cleanup needed on leave, no persistence needed.
- **`time.now()`** returns seconds since the pack started, as a number —
  arithmetic on it is plain subtraction.
- **A returned string** from a command shows to the player in red; here we
  send the message ourselves instead because it is informational, not an
  error.

:::caution[Gotcha]
a script reload restarts the clock — `time.now()` counts from
the pack's start — but `player.data` is also reset per session, so the two
stay consistent. For cooldowns that must survive restarts, store the
timestamp in [storage](/systems/storage/) with `storage.set("cooldown." ..
player.uuid, time.now())` instead.
:::

## Cooldown on an action, not a command

The same guard works inside any event. This one rate-limits a button drawn on
a screen, using the click event's player:

```luau
players.on_click(function(player, hit)
    if hit.button ~= "right" then return end
    local last = player.data.press_at
    if last and time.now() - last < 0.2 then return end   -- 200 ms like the client's own
    player.data.press_at = time.now()
    sound.play("block.note_block.hat", { at = player.at, pitch = 1.5 })
end)
```

The client itself fires one click per 200 ms — a script-side guard tighter
than that only breaks legitimate use.

## A repeating timer with a shared budget

For "every player may use this once per round", keep the round's start time
once instead of per-player timestamps:

```luau
local round_start = time.now()

commands.add("daily", function(player)
    if player.data.daily_round == round_start then
        player:message("Already claimed this round.", "red")
        return
    end
    player.data.daily_round = round_start
    player:give("diamond")
end)
```

Marking the round by identity (a copied timestamp) rather than comparing
times means no drift, no off-by-one, and no arithmetic.

## See also

- [Commands](/systems/commands/) — the command options (`permission`,
  `suggest`) that pair with cooldowns.
- [Player lifecycle](/players/player-lifecycle/) — what `player.data` survives.
- [Runtime](/concepts/runtime/) — `time.now`, `time.every` and tick timing.
