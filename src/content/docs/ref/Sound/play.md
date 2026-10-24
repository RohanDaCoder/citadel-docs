---
title: 'sound.play'
description: 'Plays a sound by name to everyone in the room; volume above 1 carries further, pitch 0.5..2.0.'
---

Part of [`sound`](/ref/Sound/).

```luau
sound.play(name: string, opts: { at: Vec3 ?, volume: number ?, pitch: number ?, category: string ?, }?)
```

Plays a sound by name to everyone in the room; volume above 1 carries further, pitch 0.5..2.0.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| `name` | `string` | yes |
| `opts` | `{ at: Vec3 ?, volume: number ?, pitch: number ?, category: string ?, }` | no |

## Used in

> "sound.play("entity.experience_orb.pickup", { at = at, pitch = 1.2 })" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "sound.play("entity.experience_orb.pickup", { at = at, pitch = 1.2 })" — [Guide: Coin rush](/guides/guide-coin-rush/)
> "room.sound.play("block.note_block.bell", { at = pad.at })" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "room.sound.play("block.note_block.bell", { at = pad.at })" — [Guide: Parkour, a room each](/guides/guide-parkour-a-room-each/)
> "sound.play("block.note_block.hat", { at = player.at, pitch = 1.5 })" — [Scoreboard with a button](/guides/guide-scoreboard-with-a-button/)
> "if powered then sound.play("block.note_block.pling", { at = block.at }) end" — [Custom blocks](/world/custom-blocks/)
