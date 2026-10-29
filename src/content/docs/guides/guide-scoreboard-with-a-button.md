---
title: 'Scoreboard with a button'
description: 'A compact tutorial — a screen in the air, a Tap me item on the hotbar: right-click it, a hat sound plays, and every player''s tap count redraws on the board, kept in storage.'
---

:::note[In short]
a one-file pack that counts clicks. A screen hangs in the
air over a stone floor, every player gets a "Tap me" block in hotbar
slot 1, and each right-click plays a sound and adds one to that player's
count on the board. The counts live in `storage`, so they survive a
restart.
:::

## What you build

- A stone floor, and a 4 by 2 screen in the air, facing south.
- Every player who joins gets a lapis block, "Tap me", in hotbar slot 1.
- Right-clicking the block in hand counts a tap: a hat sound plays, and
  the count is kept in `storage` under `"taps.<name>"`.
- The board lists every player's name and taps, redrawn on every join,
  leave and click.

## Before you start

Built on [Quick start](/getting-started/quick-start/): `world.on_generate`,
`players.on_join` and one `main.luau`.

## 1. The ground

Flat stone, one fill per chunk:

```luau
-- main.luau
world.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "stone")
end)
```

## 2. The board

The board itself — a screen at `(-2, 68, -10)`, four blocks wide, two
tall, facing south:

```luau
local board = world.screen{ at = vec3(-2, 68, -10), facing = "south", width = 4, height = 2 }
```

`world.screen` is the call for a picture in the air; the full set of
drawing calls and options is in [Screens](/ui/screens/).

## 3. Redraw the scores

One function draws the whole board, so every change goes through it:

```luau
local function redraw()
    board:clear(colors.black)
    board:text(16, 12, "TAPS", colors.yellow, 40)
    local y = 64
    for _, p in players.list() do
        local score = storage.get("taps." .. p.name) or 0
        board:text(16, y, p.name, colors.white, 28)
        board:text(board.width - 16 - board:measure(tostring(score), 28), y, tostring(score), colors.cyan, 28)
        y += 34
    end
end
```

The board clears to black, writes the `TAPS` header in yellow at size 40,
then a row per connected player: the name in white from x = 16, the count
in cyan right-aligned — its x is `board.width - 16 - board:measure(..)`,
the board's width less a 16-pixel margin less the text's measured width.
`storage.get("taps." .. p.name) or 0` reads a player with no taps yet as 0.

## 4. Players in and out

Joining hands out the button; leaving redraws the list:

```luau
players.on_join(function(player)
    player:hotbar{ [1] = { item = "lapis_block", name = "Tap me" } }
    player:message("Right click the block in your hand.", colors.cyan)
    redraw()
end)

players.on_leave(function()
    redraw()
end)
```

`player:hotbar` puts a lapis block named "Tap me" in slot 1 (see
[Menus](/ui/menus/) for the hotbar and its click events), and both events
call `redraw` so the board stays current.

## 5. The click

The click is the game — count it, sound it, redraw:

```luau
players.on_click(function(player, hit)
    if hit.slot ~= 1 or hit.button ~= "right" then
        return
    end
    local key = "taps." .. player.name
    storage.set(key, (storage.get(key) or 0) + 1)
    sound.play("block.note_block.hat", { at = player.at, pitch = 1.5 })
    redraw()
end)
```

Only a right-click while holding slot 1 counts: any other slot or button
returns early. The count is `storage.get(key) or 0`, plus one, written
back under the same key; a hat note plays at the player, pitched at 1.5;
and the board redraws.

## Try it

Run the pack and join: a lapis block named "Tap me" in slot 1, and a cyan
message telling you to right-click it. Right-click — a hat sound plays
where you stand and your count on the board goes up by one. Join with a
second player and the board lists both; leave, and the list redraws
without you.

## Where to go next

- [Screens](/ui/screens/) — `world.screen`, every drawing call,
  per-player views.
- [Menus](/ui/menus/) — hotbar menus, `on_click`, `on_slot`.
- [Storage](/systems/storage/) — keys, values, what storage can hold.
- [Sound](/ui/sound/) — playback options and positions.

## See also

- [Coin rush](/guides/guide-coin-rush/) — the same scores on a sidebar, in a
  full game.
- [Cookbook: leaderboards](/cookbook/cookbook-leaderboards/) — the list-and-
  storage pattern on its own.
