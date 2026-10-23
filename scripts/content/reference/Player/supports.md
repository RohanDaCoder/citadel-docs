---
title: "player:supports"
url: /docs/citadel/reference/Player/supports
---

# player:supports

True if this player's client can show the feature.

```
player:supports(feature: Feature) → boolean
```


## Parameters


## Returns


## Used in
- [`client version. To check a feature, ask `player:supports` (see "Client`Packs](/docs/citadel/packs)
- [`(`player:supports("resource_pack")` is false). A pack that needs the textures`Packs](/docs/citadel/packs)
- [`player:supports("light") -- can this player's client show it? see "Client versions"`Players](/docs/citadel/players)
- [`once. Nothing here needs `player:supports`: a client too old for a feature is`Body and movement](/docs/citadel/body-and-movement)
- [`Both need 1.19.4 (`player:supports("display")`). `free` means mouse look`Cameras](/docs/citadel/cameras)
- [`if player:supports("display") then`Client versions](/docs/citadel/client-versions)
- [`local map = player.ui.overlay{ corner = "top_right", size = 96, margin = 4 } -- nil where player:supports("overlay") is false`HUD](/docs/citadel/hud)
- [`(`player:supports("layout")`). On any other client, `player.ui.show``Layouts](/docs/citadel/layouts)
