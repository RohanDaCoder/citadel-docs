---
title: "player:supports"
description: "True if this player's client can show the feature."
---

Part of [`Player`](/ref/Player/).

```luau
player:supports(feature: Feature) → boolean
```

True if this player's client can show the feature.

## Parameters

| Name      | Type                       | Required |
| --------- | -------------------------- | -------- |
| `feature` | [`Feature`](/ref/Feature/) | yes      |

## Returns

- `boolean`

## Used in

> "client version. To check a feature, ask `player:supports` (see "Client" — [Packs](/concepts/pack-anatomy/)
> "(`player:supports("resource_pack")` is false). A pack that needs the textures" — [Packs](/concepts/pack-anatomy/)
> "player:supports("light") -- can this player's client show it? see "Client versions"" — [Players](/players/player-lifecycle/)
> "once. Nothing here needs `player:supports`: a client too old for a feature is" — [Body and movement](/players/movement/)
> "Both need 1.19.4 (`player:supports("display")`). `free` means mouse look" — [Cameras](/players/movement/)
> "if player:supports("display") then" — [Client versions](/appendix/client-versions/)
