---
title: "http.get"
description: "GET a URL"
---

Part of [`http`](/ref/http/).

```luau
http.get(url: string, options: {query: {[string]: string }?, headers: {[string]: string }?, timeout: number ?, cache: number ?}?) → HttpResponse
```

GET a URL. `cache` is the seconds a 200 answer is kept on disk; `timeout` is 1 to 60 seconds, 15 by default.

## Parameters

| Name      | Type                                                                                                   | Required |
| --------- | ------------------------------------------------------------------------------------------------------ | -------- |
| `url`     | `string`                                                                                               | yes      |
| `options` | `{query: {[ string ]: string }?, headers: {[ string ]: string }?, timeout: number ?, cache: number ?}` | no       |

## Returns

- [`HttpResponse`](/ref/HttpResponse/)

## Used in

> "-- it may wait (task.wait, http.get, stores); the chunk is done when it returns" — [Blocks and terrain](/world/terrain-generation/)
> "- A `banner` is a 1024×512 PNG its creator uploaded and Minefort checked: 8 by 4 maps. Read it with `http.get(banner, { cache = 86400 }):image()`; a new banner has a new URL, so the cache never shows an old one." — [Hub](/systems/hub/)
> "`http.get` fetches a URL: map tiles, a leaderboard, any public API." — [HTTP](/systems/http/)
> "local res = http.get("https://tile.example.org/15/9649/12315.png", {" — [HTTP](/systems/http/)
