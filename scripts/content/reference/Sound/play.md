---
title: "sound.play"
url: /docs/citadel/reference/Sound/play
---

# sound.play

Plays a sound by name to everyone in the room; volume above 1 carries further, pitch 0.5..2.0.

```
sound.play(name: string, opts: { at: Vec3?, volume: number?, pitch: number?, category: string?, }?)
```


## Parameters


## Used in
- [`sound.play("entity.experience_orb.pickup", { at = at, pitch = 1.2 })`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`sound.play("entity.experience_orb.pickup", { at = at, pitch = 1.2 })`Guide: Coin rush](/docs/citadel/guides/coin-rush)
- [`room.sound.play("block.note_block.bell", { at = pad.at })`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`room.sound.play("block.note_block.bell", { at = pad.at })`Guide: Parkour, a room each](/docs/citadel/guides/parkour-a-room-each)
- [`sound.play("block.note_block.hat", { at = player.at, pitch = 1.5 })`Scoreboard with a button](/docs/citadel/scoreboard-with-a-button)
- [`if powered then sound.play("block.note_block.pling", { at = block.at }) end`Custom blocks](/docs/citadel/custom-blocks)
- [`sound.play(name, { at = spawn, volume = 1, pitch = 1, category = "record" })`Sound](/docs/citadel/sound)
- [`| | `sound.play` | `sound.stream` |`Sound](/docs/citadel/sound)
