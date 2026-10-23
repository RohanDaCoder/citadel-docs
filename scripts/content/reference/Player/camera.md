---
title: "player.camera"
url: /docs/citadel/reference/Player/camera
---

# player.camera

What they look out of: a camera from camera.fixed/free/orbit/chase, or nil or false for their own eyes. No delay is needed after creating its target. Ends when the target is destroyed or the player leaves the room.

```
player.camera: (Camera | false)?
```


## Used in
- [`player.camera = cam -- look out of a camera (see cameras); nil or false is their own eyes`Body and movement](/docs/citadel/body-and-movement)
- [`player.camera = orbit`Cameras](/docs/citadel/cameras)
- [`player.camera = nil -- their own eyes again`Cameras](/docs/citadel/cameras)
- [`| A different viewpoint | `player.camera` | Controls the view; `chase` composes with riding. |`Displays](/docs/citadel/displays)
