---
title: 'player.camera'
description: 'What they look out of: a camera from camera.fixed/free/orbit/chase, or nil or false for their own eyes'
---

Part of [`player`](/ref/Player/).

```luau
player.camera: (Camera | false)?
```

What they look out of: a camera from camera.fixed/free/orbit/chase, or nil or false for their own eyes. No delay is needed after creating its target. Ends when the target is destroyed or the player leaves the room.

## Used in

> "player.camera = cam            -- look out of a camera (see cameras); nil or false is their own eyes" — [Body and movement](/players/movement/)
> "player.camera = orbit" — [Cameras](/players/movement/)
> "player.camera = nil                                       -- their own eyes again" — [Cameras](/players/movement/)
> "\| A different viewpoint \| `player.camera` \| Controls the view; `chase` composes with riding. \|" — [Displays](/ui/displays/)
