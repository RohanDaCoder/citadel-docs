---
title: 'network.browse'
description: 'The platform''s hub finding every network, in the order to show them'
---

Part of [`network`](/ref/network/).

```luau
network.browse(view: "search" | "for-you" | "recent" | "featured", options: {player: (Player | string)?, query: string ?, page: number ?, category: string ?, online: boolean ?, ids: {string}?, sort: ("players" | "name")?, also: {recent: boolean ?, favorites: {string}?}?}?) → ({BrowseEntry}?, (number | string)?, {recent: {rows: {BrowseEntry}, total: number} | false | nil, favorites: {rows: {BrowseEntry}, total: number} | false | nil}?)
```

The platform's hub finding every network, in the order to show them. nil and why on a refusal, and anywhere but that hub. One page of 6 rows (page from 1), and how many there are in all; nil and why on a refusal.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `view` | `"search" \| "for-you" \| "recent" \| "featured"` | yes |
| `options` | `{player: (Player \| string)?, query: string ?, page: number ?, category: string ?, online: boolean ?, ids: {string}?, sort: ("players" \| "name")?, also: {recent: boolean ?, favorites: {string}?}?}` | no |

## Returns

- `({BrowseEntry}?, (number | string)?, {recent: {rows: {BrowseEntry}, total: number} | false | nil, favorites: {rows: {BrowseEntry}, total: number} | false | nil}?)`

## Used in

> "- `network.browse(view, options?)` finds other networks, and only the platform's hub may ask:" — [Network](/systems/network/)
> "- `view` is `"search"` (what matches `query`: names as they are typed, and domains), `"for-you"` (more of what `player` plays, busiest first, none of their recent ones), `"recent"` (where `player` played last, newest first) or `"featured"` (the busiest). Each row is a network: `{id, name, category, motd, icon, players, maxPlayers, state}`, and `id` is what `player:connect` takes. A network is one row, however many servers it has. It returns one page of 6 rows and how many there are in all: `local rows, total = network.browse('featured', { page = 2 })`." — [Network](/systems/network/)
> "with `network.browse`, and its hubs with `network.instances`, and asks the" — [Hub](/systems/hub/)
> "for _, s in network.browse('featured') or {} do print(s.name, s.players) end" — [Hub](/systems/hub/)
