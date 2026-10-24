---
title: 'Client versions'
description: 'The player:supports feature matrix — which client version each UI and world feature needs, how resource-pack refusals read, and what min_client does.'
---

:::note[In short]
the script never sees a client version. It asks
`player:supports(feature)` and gets a boolean — the same pack then serves
1.8 and 26.x clients at once. Unguarded calls are safe: a client that
cannot show a feature is not sent it; guard only to show something else.
:::

## The feature matrix

| Feature | What needs it | From |
| --- | --- | --- |
| `bossbar` | `ui.bossbar`, `player.ui.bossbar` | 1.9 |
| `potion_color` | an item's `color` | 1.11 |
| `floor_frame` | a screen or frame with `facing = "up"` | 1.13 |
| `light` | `world.light` | 1.14 |
| `hex_color` | a colour outside Minecraft's sixteen names | 1.16 |
| `glow_frame` | `glow = true` on a screen | 1.17 |
| `display` | `world.display`, any kind | 1.19.4 |
| `hitbox` | `world.hitbox` | 1.19.4 |
| `model` | `world.display{ kind = "model" }` | 1.21.4 |
| `layout` | `player.ui.show` | 1.21.4 |
| `dialog` | `player.ui.dialog` | 1.21.6 |
| `overlay` | `player.ui.overlay` | 26.3 only |
| `resource_pack` | the pack's textures, models and sounds | a client that did not turn the pack down |

- A name not in this table is an error.
- A Bedrock client answers `false` to every feature in the table (except where noted in the topic pages).

## The fallback pattern

```luau
if player:supports("display") then
    world.display{ kind = "text", text = "Bet 50", at = pad }
else
    board:text(8, 8, "Bet 50", colors.white, 24)   -- a screen works from 1.8
end
```

## Resource-pack refusals

A client that turns the resource pack down answers `false` to
`resource_pack`, `model`, `layout`, `dialog` and `overlay`, from the moment
it answers. It is sent no layout and no dialog: they are drawn in the pack's
fonts. An open dialog closes.

A pack that needs the textures says so with `min_client` in `citadel.yml`,
which refuses old clients outright instead of degrading feature by feature.

## Version-related behaviours elsewhere

- Particles: a client whose version lacks a particle does not get it. Before
  1.13, dust is one particle a point, in its colour, with no count, spread or
  size. 1.7 shows dust only. See [FX](/ui/fx/).
- Sound: a client older than 1.13 hears nothing of streams; Simple Voice
  Chat is required. See [Sound](/ui/sound/).
- Player heads: clients from 1.7 see the face; Bedrock clients see no face.
- Input: `player.input` reads keys on foot from 1.21.2; before that a client
  reports keys only while it rides. See [Movement](/players/movement/).
- Cameras: from 1.20.2 the client glides between moves. See
  [Movement](/players/movement/).
- Textures of your own: on Java 1.21.4 and later. See
  [Pack anatomy](/concepts/pack-anatomy/).

## See also

- [Conventions](/concepts/conventions/) — what a version lacks is absent, not zero.
- [Pack anatomy](/concepts/pack-anatomy/) — `min_client` in the manifest.
- [Server settings](/systems/server-settings/) — the server's own file.
