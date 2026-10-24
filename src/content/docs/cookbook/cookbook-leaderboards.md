---
title: "Leaderboards"
description: "Three leaderboard patterns — the live sidebar for a running game, the world.screen board that persists with storage, and the experience-wide best score with stores:increment."
---

:::note[In short]
a leaderboard needs a score, a sort, and a place to draw.
Scores live in `player.data` for the session, `storage` for the pack, or
`stores` for the whole experience; the drawing side is `ui.sidebar` for a
running game or a `world.screen` board in the world. This page shows the
three patterns from the working guides.
:::

## Pattern 1: the live sidebar

The sidebar lists every player, most coins first — this is the Coin rush
pattern verbatim:

```luau
local function show_scores()
    local list = players.list()
    table.sort(list, function(a, b)
        return a.data.coins > b.data.coins
    end)
    local lines = {}
    for _, p in list do
        table.insert(lines, `{p.name}  {p.data.coins}`)
    end
    ui.sidebar{ title = "COIN RUSH", lines = lines }
end
```

- Scores are `player.data.coins` — session state, right for a round.
- `players.list()` returns everyone in the main room; `table.sort` with a
  comparator does the ranking.
- Call `show_scores()` after every score change; the sidebar is a replace,
  not an append.

## Pattern 2: the screen board that persists

A `world.screen` board in the world, backed by `storage` so scores survive a
restart — the "Scoreboard with a button" pattern:

```luau
local board = world.screen{ at = vec3(-2, 68, -10), facing = "south", width = 4, height = 2 }

local function redraw()
    board:clear(colors.black)
    board:text(16, 12, "TAPS", colors.yellow, 40)
    local y = 64
    for _, p in players.list() do
        local score = storage.get("taps." .. p.name) or 0
        board:text(16, y, p.name, colors.white, 28)
        board:text(board.width - 16 - board:measure(tostring(score), 28), y,
                   tostring(score), colors.cyan, 28)
        y += 34
    end
end

players.on_leave(function() redraw() end)
```

- `storage.get(key) or 0` — absent is `nil`, never zero.
- `board:measure(text, size)` right-aligns the score column.
- Redraw on the events that change the board (score, join, leave), not on a
  tick; a screen keeps its pixels until you redraw.
- The full working example, including the click that increments, is
  [Scoreboard with a button](/guides/guide-scoreboard-with-a-button/).

## Pattern 3: the experience-wide best

For a best score that spans every server of an experience, use
`stores:increment` — it is atomic, so two servers can raise the same key at
once:

```luau
local scores = stores.open()

local function finish(player: Player, coins: number)
    local best = scores:increment(`best.{player.uuid}`, 0)   -- read-start at 0
    if coins > best then
        scores:set(`best.{player.uuid}`, coins)
        player:message(`New best: {coins}!`, "gold")
    end
end
```

- Every store call yields while the I/O runs — call from a callback or
  `task.spawn`, never from a synchronous ask handler or module top level.
- Keys are strings; facts are at most 1 MiB. A number is a long way from that.
- The conflict rules (`if_version`, fencing tokens) are in
  [Shared stores](/systems/shared-stores/).

## Sorting helper

Every pattern above sorts the same way; one helper serves all of them:

```luau
local function ranked(get: (p: Player) -> number): { Player }
    local list = players.list()
    table.sort(list, function(a, b) return get(a) > get(b) end)
    return list
end
```

## See also

- [Guide: Coin rush](/guides/guide-coin-rush/) — the full game these patterns
  come from.
- [UI basics](/ui/ui-basics/) — `ui.sidebar` and text runs.
- [Screens and layouts](/ui/screens/) — the screen drawing API.
- [Storage](/systems/storage/) and [Shared stores](/systems/shared-stores/).
