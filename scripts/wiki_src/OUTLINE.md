# Citadel Developer Wiki — Information Architecture

Sections and pages. `src:` = source page(s) in `_sources/`. `new:` = synthesized from corpus-wide analysis.

## /getting-started

1. what-is-citadel — new (platform, lite/full/plugin modes, hosting, versions 1.8–26.x)
2. quick-start — src: doc-your-first-pack + guide-your-first-pack (merged, expanded)
3. tooling — src: doc-packs (lsp/CLI parts), doc-version-info (new: CLI + luau-lsp + strict types)
4. luau-primer — new (Luau for devs: strict mode, types, task library differences, --!strict)

## /concepts

1. architecture — new (server/rooms/ticks/pack lifecycle/reload semantics/budgets)
2. pack-anatomy — src: doc-packs (citadel.yml manifest reference, file layout, assets, modes, load limits)
3. runtime — src: doc-modules-and-tasks, doc-limits-and-reload (tasks, require, reload semantics, budgets)
4. events — src: doc-game-events, doc-cancelling-events + all on_* facts corpus-wide (event model)
5. conventions — src: doc-api-basics (vec3/color/text/options tables/nil-false-true/naming)
6. rooms-and-dimensions — src: doc-rooms, doc-dimensions, doc-a-world-per-player, guide-a-dungeon-dimension (reference parts)

## /world

1. terrain-generation — src: doc-blocks-and-terrain (on_generate/on_populate, Chunk API, heightmaps, terrain steps)
2. block-reference — src: doc-blocks-and-terrain + api-basics block naming (names, [props], version fallbacks)
3. building — src: doc-building-well (world.build, Builder, Schematic, pasting)
4. custom-blocks — src: doc-custom-blocks (BlockSpec, hooks, state/data, power)
5. game-data — src: doc-game-data (game.block/item/entities, spawn/attacks/interact rules)
6. world-state — src: doc-blocks-and-terrain rules parts + time/weather facts (world.rules, time, spawn_point)

## /entities

1. custom-entities — src: doc-custom-entities (EntitySpec, define, think, physics)
2. entity-handles — src: doc-custom-entities handle parts (EntityHandle: velocity/amend/nearby)
3. mobs — src: doc-mobs-and-drops + game-data spawn rules (world.spawn, drops)
4. npcs — src: doc-npcs (Npc API, poses, riding)

## /players

1. player-lifecycle — src: doc-players lifecycle parts (join/leave/death/respawn, sessions, data)
2. movement — src: doc-body-and-movement, doc-input, doc-cameras (teleport, ride, speed, input)
3. inventory — src: doc-items, doc-armour (ItemSpec, give/take, containers)
4. visibility — src: doc-players visibility parts (visible/hide/teams)
5. health — src: doc-players health parts + room-rules damage parts
6. permissions — src: doc-permissions

## /ui

1. ui-basics — src: doc-hud, doc-titles-and-bars, doc-text-formatting (message/title/bars/text runs)
2. screens — src: doc-screens, doc-layouts (Screen, Layout, LayoutNode)
3. canvases — src: doc-canvases, doc-map-pictures (Canvas drawing, Picture)
4. menus — src: doc-menus, doc-hotbar-menus, doc-shop UI parts
5. dialogs — src: doc-dialogs (Dialog, DialogNode)
6. displays — src: doc-displays, doc-3d-models (Display kinds, models, animations)
7. fx — src: doc-particles-and-lasers (fx.particle)
8. sound — src: doc-sound (sound.play, streams, speakers)

## /systems

1. commands — src: doc-commands
2. storage — src: doc-storage (per-pack JSON)
3. shared-stores — src: doc-shared-stores (stores, leases, blobs)
4. network — src: doc-network (websockets)
5. http — src: doc-http
6. shop — src: doc-shop (Gems, products, on_paid)
7. hub — src: doc-hub (servers, experiences, portals)
8. server-settings — src: doc-server-settings, doc-client-versions (server file, min_client)
9. limits — src: doc-limits-and-reload budgets parts

## /guides (tutorials, keep step-by-step nature)

1. build-a-cottage — src: guide-build-a-cottage
2. coin-rush — src: guide-coin-rush
3. parkour-a-room-each — src: guide-parkour-a-room-each
4. a-dungeon-dimension — src: guide-a-dungeon-dimension
5. scoreboard-with-a-button — src: doc-scoreboard-with-a-button
6. a-world-per-player moved here? no — concepts. keep 5.

## /cookbook (new, patterns from corpus)

1. cooldowns — new (time-based command cooldowns)
2. leaderboards — new (stores + ui.sidebar)
3. teleport-pads — new (zones + routes)
4. kits — new (player:give inventory patterns)
5. teams — new (player.data + visibility)
6. minigame-loop — new (rooms.create round loop from coin-rush/parkour)
7. save-load — new (storage/stores patterns)

## /appendix

1. event-catalog — GENERATED (all on_* events, table)
2. limits-table — GENERATED+curated (all numeric limits)
3. client-versions — src: doc-client-versions (feature matrix)
4. faq — new (troubleshooting from corpus facts: reload, load failure, mode conflicts)

## /ref (API reference — pipeline generated from dataset.json, enriched)

- Modules: 29 globals grouped by domain
- Types: 148 types A-Z
- Every member: signature, params, returns, description, examples (from used_in quotes)
