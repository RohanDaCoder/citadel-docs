---
title: "Client versions"
url: /docs/citadel/client-versions
---

# Client versions

```luau
if player:supports("display") then
    world.display{ kind = "text", text = "Bet 50", at = pad }
else
    board:text(8, 8, "Bet 50", colors.white, 24)   -- a screen works from 1.8
end

```
| feature | what needs it | from |
| --- | --- | --- |
| `bossbar` | `ui.bossbar`, `player.ui.bossbar` | 1.9 |
| `potion_color` | an item’s `color` | 1.11 |
| `floor_frame` | a screen or frame with `facing = "up"` | 1.13 |
| `light` | `world.light` | 1.14 |
| `hex_color` | a colour outside Minecraft’s sixteen names | 1.16 |
| `glow_frame` | `glow = true` on a screen | 1.17 |
| `display` | `world.display`, any kind | 1.19.4 |
| `hitbox` | `world.hitbox` | 1.19.4 |
| `model` | `world.display{ kind = "model" }` | 1.21.4 |
| `layout` | `player.ui.show` | 1.21.4 |
| `dialog` | `player.ui.dialog` | 1.21.6 |
| `overlay` | `player.ui.overlay` | 26.3 only |
| `resource_pack` | the pack’s textures, models and sounds | a client that did not turn the pack down |
- A name not in this table is an error.
- A client that turns the resource pack down answers false to
`resource_pack`, `model`, `layout`, `dialog` and `overlay`, from the
moment it answers. It is sent no layout and no dialog: they are drawn in
the pack’s fonts. An open dialog closes.
- A Bedrock client answers false to every feature in this table.
- Unguarded calls are safe: a client that cannot show a feature is not
sent it. Guard only to show something else.
- Or set `min_client` in `citadel.yml` to refuse old clients.
