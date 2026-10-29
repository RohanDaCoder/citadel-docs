---
title: The event model
section: concepts
order: 4
description: How every on_* subscription works — connections and cancellation, the notification events across world, players and rooms, and the three cancellable asks with their two-millisecond deadline.
tags: [events, callbacks, asks, cancellation, connections]
---

# The event model

> **In short:** pack code reacts to the game through `on_*` subscriptions that
> return a connection; `connection:cancel()` unsubscribes. Most events are
> notifications that arrive after the fact. Three — `players.on_break`,
> `on_place` and `on_damage` — are **asks**: the engine pauses the action for
> two milliseconds and `false` vetoes it. This page is the model; the full
> per-event catalog is in the [event catalog](/appendix/event-catalog).

## Subscriptions and connections

```luau
local conn = players.on_click(function(player, hit) end)
-- ...later:
conn:cancel()      -- the subscription stops; pending deliveries are removed too
```

- Subscriptions live in the pack that made them. On reload, the old script's
  timers and connections end.
- `world.on_generate` and `world.on_populate` are **not** subscriptions: they
  are single-handler setters. A later call replaces the previous handler, and
  they return nothing.
- The engine's own `/help` lists every command a player may run — commands are
  registered, not events (see [Commands](/wiki/commands)).

## Notification events

Notifications arrive after the fact. The load-bearing ones on the world and
its entities:

```luau
world.on_block_break(function(player, pos, block) end)   -- block: what was there
world.on_block_place(function(player, pos, block) end)   -- block: what was put down
world.on_entity_spawn(function(entity, name) end)        -- a mob appeared; entity is the handle
world.on_entity_death(function(id, name) end)            -- it is gone: id and name is all there is
players.on_pickup(function(player, item, count) end)
players.on_drop(function(player, item, count) end)
```

`block` is the canonical name in both. `player` is `nil` when the world
dropped the stack (a leaf decays, a mob dies, an explosion) or the player has
already left the room — always check before using it:

```luau
world.on_block_break(function(player, pos, block)
    if block == "diamond_ore" and player then
        message(player.name .. " struck diamond", colors.cyan)
    end
end)
```

Player lifecycle — `players.on_join` fires on connect in the main room, and a
room's own `room.players.on_join` fires on each `player:move_to(room)`;
`players.on_leave` matches. Joins, leaves, deaths and respawns are retained in
order and never dropped by budget pressure (see
[Runtime](/wiki/runtime#the-tick-budget)).

## Asks: the cancellable events

Three events are questions the engine asks **before** acting, waiting a few
milliseconds for the answer:

```luau
players.on_break(function(player, pos, block) return false end)
players.on_place(function(player, pos, block) return false end)
players.on_damage(function(player, hit) return false end)
```

`players.on_damage` receives a `hit` table:

| Field        | Meaning                                                                                                                                 |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| `hit.amount` | The damage, in half hearts, before armour.                                                                                              |
| `hit.cause`  | `"fall"`, `"drown"`, `"suffocate"`, `"void"`, `"lava"`, `"fire"`, `"cactus"`, `"starve"`, `"attack"`, `"shot"`, `"blast"` or `"magic"`. |
| `hit.by`     | The player who hit, or who shot the arrow; `nil` for anything else.                                                                     |
| `hit.kind`   | The kind's name (`"Skeleton"`) when a mob did it; else `nil`.                                                                           |

The veto rules:

- **Only `false` is a veto.** A handler that returns nothing allows the
  action; a handler that errors is not a veto — it counts as a missed
  deadline.
- **Across packs, any `false` wins.** One `false` cancels the action.
- A refused arrow bounces off, as off a creative player.
- A pack's own `player:damage` call is not asked about, in this pack or
  another. An entity of a pack's own has the same question as a hook:
  `on_damage` in `game.entities.define`, which answers `"take"` or `"ignore"`.

```luau
-- No friendly fire, and nobody is hurt at the spawn.
players.on_damage(function(player, hit)
    if hit.by and hit.by.data.team == player.data.team then return false end
    if player.at:distance(SPAWN) < 8 then return false end
end)

-- A spawn area nobody digs in.
players.on_break(function(player, pos, block)
    if math.abs(pos.x) < 16 and math.abs(pos.z) < 16 then
        player:message("not here", colors.red)
        return false
    end
end)
```

## The deadline

The engine waits **two milliseconds** for your pack, then stops waiting.
`task.wait` and anything that blocks are errors inside an ask handler.

| Hook                | A missed deadline means                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| `players.on_break`  | **The break is denied.** Protection fails closed on timeout, error, overflow, or a disabled handler. |
| `players.on_place`  | **The place is denied.** The same protection guarantee.                                              |
| `players.on_damage` | **The damage is denied.** The same protection guarantee.                                             |

The rule: **fail open only where the default is safe.** A pack block's own
`on_break` (which comes with pack blocks) fails _closed_ to the drops its
definition declares.

Miss a kind too often and the engine **stops asking you** that kind: it takes
the default, logs this once, and sets `disabled`. Watch the counters:

```luau
time.every(60, function()
    for kind, count in citadel.budget().asks.kinds do
        if count.missed > count.answered then
            citadel.log(`slow at {kind}: {count.missed} of {count.asks} missed`)
        end
    end
end)
```

- Answer at once — never `task.wait` in an ask.
- Answering costs tick budget, under the hook name `"ask"`.
- A spent budget does not stop an ask from being answered.
- With no protection listener registered, the action follows the normal game
  rules; a listener that completes and returns `nil` still allows it.

## Observe-after-veto

The observe-only events come **after** the asks: a vetoed break never reaches
`world.on_block_break` or `world.on_block_place`.

## See also

- [Event catalog](/appendix/event-catalog) — every `on_*` event in one table.
- [Runtime](/wiki/runtime) — the budget, the event queue and its 4096 cap.
- [Cancelling in practice](/wiki/health) — damage rules and room rules.
