---
title: "Citadel Developer Wiki"
description: "The unofficial developer wiki for Minefort Citadel — the Luau scripting engine for Minecraft servers. Concepts, every API call, and working guides, restructured from the official docs into scannable reference form."
---

:::note[In short]
Citadel is Minefort's Luau scripting engine for Minecraft
servers. This wiki is a restructured, developer-facing reference of the
whole platform — the concepts, every API call, and working guides —
rebuilt from the official documentation into scannable, linkable,
table-first pages.
:::

Citadel runs a Luau script on a vanilla Minecraft server and gives it the
whole game: blocks, terrain, entities, players, inventories, UI, storage,
networking and the shop. The same script runs on Java clients from 1.8 to
26.x. This wiki covers the full surface, from your first pack to the
limits the engine enforces.

## Start here

- [What is Citadel](/getting-started/what-is-citadel/) — the platform, the lite, full
  and plugin modes, and what a pack is.
- [Quick start](/getting-started/quick-start/) — your first pack, from empty folder to
  a running server.
- [Luau primer](/getting-started/luau-primer/) — strict mode, types and the task
  library, for developers new to Luau.
- [The event model](/concepts/events/) — the one programming pattern every
  Citadel pack is built on.

## How the wiki is organized

| Section                                              | What you find there                                                                                  |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| [Getting started](/getting-started/what-is-citadel/) | The platform, your first pack, tooling, the Luau primer.                                             |
| [Core concepts](/concepts/architecture/)             | Architecture, pack anatomy, runtime, events, conventions, rooms and dimensions.                      |
| [World & building](/world/terrain-generation/)       | Terrain generation, block reference, building, custom blocks, game data, world state.                |
| [Entities](/entities/custom-entities/)               | Custom entities, entity handles, mobs and drops, NPCs.                                               |
| [Players](/players/player-lifecycle/)                | Lifecycle, movement and cameras, inventory, visibility, health, permissions.                         |
| [Interface & media](/ui/ui-basics/)                  | Messages, titles and bars, screens, canvases, menus, dialogs, displays, fx, sound.                   |
| [Server systems](/systems/commands/)                 | Commands, storage, shared stores, network, HTTP, shop, hub, server settings, limits.                 |
| [Guides](/guides/guide-build-a-cottage/)             | Five complete, step-by-step builds — cottage, coin rush, parkour, a dungeon dimension, a scoreboard. |
| [Cookbook](/cookbook/cookbook-cooldowns/)            | Drop-in patterns: cooldowns, leaderboards, teleport pads, kits, teams, a minigame loop, save/load.   |
| [Appendix](/appendix/event-catalog/)                 | The event catalog, client version matrix, the limits table, and the FAQ.                             |

## API reference

Every global, type and call — 29 globals in five domains, 141 types, 674
documented members, each with its signature, parameters, returns and the
guides that use it — lives in the [API reference](/ref/).

## See also

- [Conventions](/concepts/conventions/) — the API's naming, vec3, colours and
  options-table rules, before you read anything else.
- [Limits](/systems/limits/) — the budget system and every number the engine
  enforces.
- [FAQ](/appendix/faq/) — reload rules, load failures, mode conflicts and
  other troubleshooting.
