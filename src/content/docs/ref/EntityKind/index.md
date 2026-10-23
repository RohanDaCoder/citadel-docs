---
title: 'EntityKind type'
description: 'One kind the game version has, in its own numbers, from game.entities.<kind>: name, size, max_health, speed and drop'
---

One kind the game version has, in its own numbers, from `game.entities.<kind>`: name, size, max_health, speed and drop. A kind that is not a mob (an arrow, a boat, primed TNT; `mob == false`) has `name`, `mob`, `width`, `height` and `physics` only: every other fact is nil for it, and a write to `spawn`, `attacks` or `interact` and a call of `amend` are errors.

## Functions

| Call | Purpose |
| --- | --- |
| [`amend`](/ref/EntityKind/amend/) | The same as `game.entities.amend(name, hooks)`. |

## Fields

| Field | Purpose |
| --- | --- |
| [`entityKind.name: string`](/ref/EntityKind/name/) | Its modern registry name: "cow". |
| [`entityKind.mob: boolean`](/ref/EntityKind/mob/) | Whether the kind is a mob: true for a cow, false for an arrow. |
| [`entityKind.physics: string ?`](/ref/EntityKind/physics/) | For a kind that is not a mob, which order of operations moves it: "item", "falling", "vehicle" or "none". Nil for a mob kind. |
| [`entityKind.behaviour: string`](/ref/EntityKind/behaviour/) | The name of the behaviour the engine runs for this kind, such as "sheep" or "living". |
| [`entityKind.profile: { [string]: string \| number \| boolean }?`](/ref/EntityKind/profile/) | Read-only copy; nil for a specialized behavior without a shared profile. |
| [`entityKind.registry_name: string`](/ref/EntityKind/registry_name/) | This version's own registry spelling: "Cow". A dungeon spawner stores this one. |
| [`entityKind.width: number`](/ref/EntityKind/width/) | Its width in blocks, in this version's numbers. |
| [`entityKind.height: number`](/ref/EntityKind/height/) | Its height in blocks, in this version's numbers. |
| [`entityKind.max_health: number`](/ref/EntityKind/max_health/) | The most health one of this kind has, in this version's numbers. `health` on a kind is an error: health is what one entity has now. |
| [`entityKind.speed: number`](/ref/EntityKind/speed/) | Blocks a tick at a full walk. |
| [`entityKind.hostile: boolean`](/ref/EntityKind/hostile/) | Whether it is hostile. |
| [`entityKind.drop: string ?`](/ref/EntityKind/drop/) | The item its death leaves behind, such as "leather"; nil for none. |
| [`entityKind.spawn: boolean ?`](/ref/EntityKind/spawn/) | The one writable field. `true`: the kind is in this world as the game defines it: it spawns by the game's own rule, also on a `mode: lite` world, and `attacks` and `interact` are on for it unless a pack sets them; an error on a 1.8.9 world with no biomes, where nothing would spawn it. `false`: the kind never spawns by itself in this world; spawner blocks, `world.spawn`, `/summon` and breeding still make it. `nil`: the pack says nothing and the world's default applies: no natural spawning on a `mode: lite` world and in a room from `rooms.create`, the game's own rule on a `mode: full` world and after `world.rules{ survival = true }`. A table is an error today. Reads what this pack set (`true`, `false` or nil), not the game's own rule. The value is this room's (`room.game.entities.cow.spawn`) and this pack's: a `false` of any pack wins. Every write is an error on a game with no natural spawning (a0.1.0 to a0.1.3). |
| [`entityKind.attacks: boolean ?`](/ref/EntityKind/attacks/) | Whether its hits hurt players. `nil`: on for a kind with `spawn = true`, else the room's `damage` rule. The kind's own setting is stronger than the room's rule. It covers the kind's own hit, its arrow (also after the shooter died) and a creeper's blast. `false` stops the damage to players only: a blast still breaks blocks. |
| [`entityKind.interact: boolean ?`](/ref/EntityKind/interact/) | Whether a player's right click on it has the game's effect (milk, a saddle). `nil`: on for a kind with `spawn = true`, else the room's `survival`. `true` is an error on 1.8.9, which has no right click on a mob. |
