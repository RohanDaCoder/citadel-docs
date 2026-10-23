---
title: "http.get"
url: /docs/citadel/reference/http/get
---

# http.get

GET a URL. `cache` is the seconds a 200 answer is kept on disk; `timeout` is 1 to 60 seconds, 15 by default.

```
http.get(url: string, options: {query: {[string]: string}?, headers: {[string]: string}?, timeout: number?, cache: number?}?) → HttpResponse
```


## Parameters


## Returns


## Used in
- [`-- it may wait (task.wait, http.get, stores); the chunk is done when it returns`Blocks and terrain](/docs/citadel/blocks-and-terrain)
- [`- A `banner` is a 1024×512 PNG its creator uploaded and Minefort checked: 8 by 4 maps. Read it with `http.get(banner, { cache = 86400 }):image()`; a new banner has a new URL, so the cache never shows an old one.`Hub](/docs/citadel/hub)
- [``http.get` fetches a URL: map tiles, a leaderboard, any public API.`HTTP](/docs/citadel/http)
- [`local res = http.get("https://tile.example.org/15/9649/12315.png", {`HTTP](/docs/citadel/http)
