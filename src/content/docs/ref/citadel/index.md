---
title: 'citadel global'
description: 'The engine itself: the log, versions, environment and the tick budget.'
---

The engine itself: the log, versions, environment and the tick budget.

Part of the [Pack anatomy](/concepts/pack-anatomy/) article.

## Functions

| Call | Purpose |
| --- | --- |
| [`log`](/ref/citadel/log/) | Writes its arguments to the server log, under this pack's name. |
| [`budget`](/ref/citadel/budget/) | This pack's slice of a tick, and what it did with it. |
| [`on_slow`](/ref/citadel/on_slow/) | Called when a batch runs out of budget; at most once a second. |

## Fields

| Field | Purpose |
| --- | --- |
| [`citadel.version: string`](/ref/citadel/version/) | The engine version, e.g. "0.1.0". |
| [`citadel.game: string`](/ref/citadel/game/) | The game version from citadel.yml, e.g. "1.8.9". |
| [`citadel.env: string`](/ref/citadel/env/) | "development", "unlisted" or "published": which copy of the game this is. |
