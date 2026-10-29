---
title: 'BlockAmendSpec type'
description: 'What game.blocks.amend takes: hooks only'
---

What `game.blocks.amend` takes: **hooks only**.  Every tnt in every world already looks like tnt and is as hard as tnt, so a data column here is refused by name. For a block of your own with different numbers, `game.blocks.define { extends = "tnt" }`.

## Functions

| Call | Purpose |
| --- | --- |
| [`on_use`](/ref/BlockAmendSpec/on_use/) | Somebody right-clicked it; `held` is the item in hand. Answers "used" or "pass"; a missed deadline passes the click through. |
| [`on_break`](/ref/BlockAmendSpec/on_break/) | Something broke it; `by` says what. Answers "none", "table" or a drops list. |
| [`on_step`](/ref/BlockAmendSpec/on_step/) | A body (a player, mob, item or other) is standing on it. |
| [`on_tick`](/ref/BlockAmendSpec/on_tick/) | A scheduled tick this block asked for came due. |
| [`on_random_tick`](/ref/BlockAmendSpec/on_random_tick/) | The random pass landed on it. |
| [`on_place`](/ref/BlockAmendSpec/on_place/) | A player put it down. |
| [`on_neighbour`](/ref/BlockAmendSpec/on_neighbour/) | A neighbour at `from` changed; `announced` is the block the notifier announced itself as. |
| [`on_trigger`](/ref/BlockAmendSpec/on_trigger/) | It was lit, blasted or burnt; `cause` is "ignite", "explosion" or "fire". |
| [`on_power`](/ref/BlockAmendSpec/on_power/) | A redstone signal started (`powered` is true) or stopped reaching it. Called once for each, not for every change beside it. |
| [`on_added`](/ref/BlockAmendSpec/on_added/) | It has just been stored, whatever stored it. |
| [`on_removed`](/ref/BlockAmendSpec/on_removed/) | It has just gone. |
