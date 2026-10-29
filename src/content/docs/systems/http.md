---
title: 'HTTP'
description: 'http.get fetches public URLs with headers, timeout and an on-disk cache; the answer is an HttpResponse with :json() and :image(). Plus http.socket WebSockets, the queue limits, and fetching chunk terrain live.'
---

:::note[In short]
`http.get` fetches a public URL and waits, like `task.wait` —
events and other callbacks run meanwhile. The answer is an
[`HttpResponse`](/ref/HttpResponse/): read `ok`, `status`, `body`, `headers`,
or parse it with `:json()` and `:image()`. A `cache` option keeps 200
answers on disk, and `http.socket` opens a WebSocket the engine keeps
alive.
:::

## `http.get`

```luau
local res = http.get("https://tile.example.org/15/9649/12315.png", {
    query = { key = "abc" },             -- added to the URL, encoded
    headers = { accept = "image/png" },
    timeout = 15,                        -- seconds, 1 .. 60; 15 is the default
    cache = 86400,                       -- seconds a 200 answer is kept on disk; left out, nothing is kept
})
res.ok        -- true for a 2xx status
res.status    -- 200; 0 when no answer came
res.error     -- why no answer came, or nil
res.body      -- the answer, a string
res.headers   -- { ["content-type"] = "image/png", ... }, names in lower case
res:json()    -- the body as a table; an error when it is not JSON
res:image()   -- a PNG body as { width, height, pixels }; pixels is a buffer, 4 bytes (RGBA) a pixel, row by row
```

| Option    | Meaning                                                                               |
| --------- | ------------------------------------------------------------------------------------- |
| `query`   | Added to the URL, encoded.                                                            |
| `headers` | Request headers, such as `{ accept = "image/png" }`.                                  |
| `timeout` | Seconds, 1 .. 60; 15 is the default. Clamped, and must be finite.                     |
| `cache`   | Seconds a 200 answer is kept on disk; left out, nothing is kept. Negative means zero. |

`res:image()` reads PNG with 8 bits a channel, not interlaced.

## Waiting, and where to call it from

The call waits, like `task.wait`. Events, other callbacks and other chunks run
during the wait. **Call it from a script or a callback, not from the top level
of a module.**

- Transport failures return `res.ok = false` — a failed request is not an
  error; read `res.error`.
- Invalid arguments or exhausted request slots raise errors.

## Limits

- Only `http` and `https`, and only GET. An answer is at most **16 MiB**.
- A pack can have **64 requests without an answer**. Eight are on the wire at
  the same time.
- A server's packs send **600 requests in a minute** at most, all packs
  together. Over that, a request waits for room, and fails when its `timeout`
  ends first. An answer from the cache does not count.
- A host can turn off private and loopback addresses. Such an address is then
  an error in `res.error`, **also after a redirect**.

## The cache

`cache` keeps the body in `<pack>/data/http/`. A cached answer has status 200
and no headers. Use it for data that does not change, such as tiles — the
86400-second tile cache in the example above is one day.

A `range` header gets a part of a file
(`headers = { range = "bytes=0-126" }`). The status is then **206**, and the
cache keeps each range by itself.

:::note
a gzip body arrives undone, with the server's
`content-encoding: gzip` or without it. A tile cut out of an archive is
gzip without the header.
:::

## The host's switches

The host decides whether packs get this, with the environment the server
starts in. **A pack cannot change it, and the server's `citadel.yml` cannot:**

```sh
CITADEL_DISABLE_HTTP=true         # http.get is off for every pack; res.error then says so
CITADEL_DISABLE_HTTP_LOCAL=true   # no private or loopback address: a pack cannot reach the host's own network
```

## A socket

`http.socket` opens a WebSocket and keeps it open. Use it for what a server
says the moment it happens, such as a chat line or a score, where `http.get`
would ask again and again.

```luau
local socket = http.socket("wss://live.example.org/room/7", {
    headers = { authorization = "Bearer abc" },   -- sent with the handshake
    on_message = function(message)
        local event = message:json()               -- or message.text, the message as it came
        if event.kind == "chat" then message(event.author .. ": " .. event.body) end
    end,
})
socket.open          -- true while the connection is up
socket:send("hello") -- queues text; true if queued, false if closed or full
socket.error         -- terminal queue overflow, or nil
socket:cancel()      -- closes it for good
```

- When the connection ends or cannot be made, the engine dials again every 3
  seconds. The log says so once. **The pack gets no event for it: read
  `socket.open`.** Receive-queue overflow is terminal and does not reconnect.
- A socket gives no message twice and none from before it opened. For what
  was said before, ask with `http.get` first.
- `on_message` runs on a tick, with the tick budget of any callback. At most
  32 messages of a socket go to the pack in a tick; the rest wait.
- Each direction queues at most **256 messages or 4 MiB per socket**. If the
  incoming queue fills, the socket closes permanently and `socket.error`
  explains why. Cancel its handle, then create a new socket after handling
  the gap. The outgoing queue returns false when full. **A true send result
  means queued, not delivered.**
- Only `ws` and `wss`. A message is at most 1 MiB; a larger send is an error.
  A binary message arrives as text with invalid UTF-8 replaced.
- A pack can have 8 sockets. A socket ends with the script.
- The host's two switches for `http.get` hold for sockets too.

## A world from fetched data

`world.on_generate` can wait, so a chunk can come from data that is fetched
when the chunk loads:

```luau
local tiles = {}
local function tile(tx, tz)                        -- one fetch for each 256 by 256 blocks
    local key = tx .. "," .. tz
    local t = tiles[key]
    if not t then
        t = { loading = true }
        tiles[key] = t                              -- before the wait, so the next chunk does not fetch it again
        local res = http.get(`https://tile.example.org/heights/{tx}/{tz}.png`, { cache = 86400 })
        if res.ok then t.image = res:image() end
        t.loading = false
    end
    while t.loading do task.wait(0.05) end          -- another chunk started the fetch
    return t.image
end

world.on_generate(function(chunk)
    local image = tile(chunk.min.x // 256, chunk.min.z // 256)
    for x = chunk.min.x, chunk.max.x do
        for z = chunk.min.z, chunk.max.z do
            local h = if image then buffer.readu8(image.pixels, ((z % 256) * 256 + x % 256) * 4) else 64
            chunk:fill(vec3(x, 0, z), vec3(x, h, z), "stone")
        end
    end
end)
```

- The engine waits 60 s for a chunk. A chunk that is not ready then is air.
- Make the chunk without the data when the fetch fails.

## See also

- [Terrain generation](/world/terrain-generation/) — `world.on_generate` and
  the chunk callbacks this pattern runs inside.
- [Hub](/systems/hub/) — reading experience banners with the cache and
  `:image()`.
- [`HttpResponse`](/ref/HttpResponse/), [`Socket`](/ref/Socket/) — the
  reference entries.
- [Limits](/systems/limits/) — every numeric limit in one place.
