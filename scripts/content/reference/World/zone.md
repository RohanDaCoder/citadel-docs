---
title: "world.zone"
url: /docs/citadel/reference/World/zone
---

# world.zone

Makes a box of blocks, both corners included, that knows who is in it; checked once a tick by feet position. Ends with the script.

```
world.zone(opts: { from: Vec3, to: Vec3, on_enter: ((player: Player) -> ())?, on_leave: ((player: Player) -> ())? }) → Zone
```


## Parameters


## Returns


## Used in
- [`coin.zone = world.zone{`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`- `world.zone` is a box of blocks. Here it is one block, and `on_enter``Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`room.world.zone{ from = from, to = to, on_enter = function(p)`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`room.world.zone{ from = vec3(-40, 30, -10), to = vec3(40, 58, c.finish.z + 10), on_enter = function(p)`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`local goal = world.zone{ from = vec3(10, 64, 10), to = vec3(14, 66, 14),`Zones and raycasts](/docs/citadel/zones-and-raycasts)
