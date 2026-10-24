---
title: "entityKind.spawn"
description: "The one writable field"
---

Part of [`entityKind`](/ref/EntityKind/).

```luau
entityKind.spawn: boolean ?
```

The one writable field. `true`: the kind is in this world as the game defines it: it spawns by the game's own rule, also on a `mode: lite` world, and `attacks` and `interact` are on for it unless a pack sets them; an error on a 1.8.9 world with no biomes, where nothing would spawn it. `false`: the kind never spawns by itself in this world; spawner blocks, `world.spawn`, `/summon` and breeding still make it. `nil`: the pack says nothing and the world's default applies: no natural spawning on a `mode: lite` world and in a room from `rooms.create`, the game's own rule on a `mode: full` world and after `world.rules{ survival = true }`. A table is an error today. Reads what this pack set (`true`, `false` or nil), not the game's own rule. The value is this room's (`room.game.entities.cow.spawn`) and this pack's: a `false` of any pack wins. Every write is an error on a game with no natural spawning (a0.1.0 to a0.1.3).
