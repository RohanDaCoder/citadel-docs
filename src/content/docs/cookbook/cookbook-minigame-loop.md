---
title: "A minigame loop"
description: "The round-based minigame skeleton — a room per round with rooms.create, a countdown on time.every with a boss bar, scores in player.data, and cleanup when the last player leaves."
---

:::note[In short]
a round-based game is a room, a timer, a scoreboard and a
cleanup. Make a room with `rooms.create`, count the round down with
`time.every` and `ui.bossbar`, keep scores in `player.data`, and destroy
the room when the last player leaves. This skeleton is distilled from the
Coin rush and Parkour guides.
:::

## The skeleton

Two functions and a command. `finish` comes first, because `start_round`'s
countdown calls it:

```luau
--!strict
local ROUND_SECONDS = 60

local function finish(room)
    local winner: Player? = nil
    for _, p in room.players.list() do
        if not winner or p.data.coins > winner.data.coins then winner = p end
    end
    if winner then
        room.ui.title{ title = winner.name .. " wins", color = "gold" }
    end
    for _, p in room.players.list() do
        p:move_to(rooms.main())     -- back to the lobby
    end
    room:destroy()
end

local function start_round(who: { Player })
    local room = rooms.create{
        spawn_point = vec3(0.5, 65, 0.5),
        generate = function(chunk)
            chunk:fill(vec3(chunk.min.x, 64, chunk.min.z),
                       vec3(chunk.max.x, 64, chunk.max.z), "grass_block")
        end,
    }

    for _, p in who do
        p:move_to(room)          -- the client swaps worlds in place
    end

    local left = ROUND_SECONDS
    room.ui.bossbar{ title = "Round", progress = 1 }
    local timer = time.every(1, function()
        left -= 1
        room.ui.bossbar{ title = "Round", progress = left / ROUND_SECONDS }
        if left <= 0 then
            timer:cancel()
            finish(room)
        end
    end)

    room.players.on_leave(function()
        if room.players.count() == 0 then room:destroy() end   -- the last one out closes it
    end)
end

commands.add("play", function(player)
    start_round({ player })
end)
```

## Why each piece is what it is

- **`rooms.create` per round.** A room made this way runs no survival rules
  and no natural spawning by default, and its `generate` function is its own
  little `on_generate` — a fresh arena per round, and the old room's world is
  discarded with it.
- **`player:move_to(room)`** swaps the client's world in place. A room's own
  `room.players.on_join` fires on each move in, so put the round's welcome
  there.
- **`time.every(1, fn)`** is precise to 1 ms and never drifting; a
  `time.every` timer can cancel itself inside its own callback, which is how
  the countdown ends. For tick-exact work there is `time.on_tick`.
- **`room.ui.*`** addresses everyone in the room — the boss bar counts the
  round down, the title announces the winner. `ui.bossbar` needs clients
  1.9+; on older clients it is simply not sent.
- **`player.data.coins`** scores the round. It resets on reconnect, which is
  the right lifetime for a round score — cross-round bests go to
  [storage](/systems/storage/) or [stores](/systems/shared-stores/).
- **The `on_leave` guard** destroys the room when the last player leaves, so
  an abandoned round cannot leak rooms. Players still in it keep the world
  until they go.

## The lobby, and going back

The main room is `rooms.main()` — the lobby players start in. Moving a player
back there ends their round. The global `players.on_join` fires on connect in
the main room; a room's own fires on each move in; `players.on_leave`
matches. Keep the lobby's welcome in the global, the round's welcome in the
room's own:

```luau
players.on_join(function(player)
    player.ui.title{ title = "Lobby", subtitle = "type /play", color = colors.cyan }
end)
```

## Rounds on a schedule

To run rounds back-to-back without a command, chain them with `task.delay` —
and remember tasks spawned at load start only after initialization commits
(see [Runtime](/concepts/runtime/)):

```luau
task.spawn(function()
    while true do
        start_round(players.list())           -- everyone in the lobby; it ends itself
        task.wait(ROUND_SECONDS + 10)         -- play + winner screen
        task.wait(5)                          -- breather between rounds
    end
end)
```

Each `start_round` owns its own countdown timer and destroys its own room when
it ends (or when the last player leaves), so the loop only paces the rounds.
`task.wait` uses elapsed real time, not ticks — a 60-second round is 60 real
seconds, however loaded the server is. `rooms.main()` is the lobby itself;
`room:destroy()` does nothing to it.

## Spawning things to collect

Coins on the floor are a loop of ground items or a custom block with an
`on_step` hook — the Coin rush guide does it with an item pickup that counts
itself and places a new one, keeping five on the floor at all times. Read
[Guide: Coin rush](/guides/guide-coin-rush/) for that half of the game, and
[Custom entities](/entities/custom-entities/) for mobs that think.

## See also

- [Guide: Coin rush](/guides/guide-coin-rush/) — the complete game this
  skeleton comes from.
- [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/) — one room
  per player instead of per round.
- [Rooms and dimensions](/concepts/rooms-and-dimensions/) — the room API.
- [Runtime](/concepts/runtime/) — `time.every`, `task.wait`, and reload rules.
