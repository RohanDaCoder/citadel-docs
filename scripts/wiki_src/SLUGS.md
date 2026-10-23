# Wiki slug map (definitive — use these exact paths in cross-links)

## getting-started
- /wiki/what-is-citadel
- /wiki/quick-start
- /wiki/tooling
- /wiki/luau-primer

## concepts
- /wiki/architecture
- /wiki/pack-anatomy
- /wiki/runtime
- /wiki/events
- /wiki/conventions
- /wiki/rooms-and-dimensions

## world
- /wiki/terrain-generation        (from blocks-and-terrain)
- /wiki/block-reference           (block naming, states, fallbacks, heads, detail)
- /wiki/building                  (world.build, Builder, schematics, named parts)
- /wiki/custom-blocks
- /wiki/game-data
- /wiki/world-state               (world.rules, time, weather, spawn protection)

## entities
- /wiki/custom-entities
- /wiki/entity-handles
- /wiki/mobs
- /wiki/npcs

## players
- /wiki/player-lifecycle
- /wiki/movement                  (body, cameras, input)
- /wiki/inventory
- /wiki/visibility
- /wiki/health
- /wiki/permissions

## ui
- /wiki/ui-basics                 (message/title/bars + text formatting)
- /wiki/screens                   (screens + layouts)
- /wiki/canvases                  (canvases + map pictures)
- /wiki/menus                     (menus + hotbar menus)
- /wiki/dialogs
- /wiki/displays                  (displays + 3d models)
- /wiki/fx
- /wiki/sound

## systems
- /wiki/commands
- /wiki/storage
- /wiki/shared-stores
- /wiki/network
- /wiki/http
- /wiki/shop
- /wiki/hub
- /wiki/server-settings           (server citadel.yml + client versions)
- /wiki/limits

## guides
- /wiki/guide-build-a-cottage
- /wiki/guide-coin-rush
- /wiki/guide-parkour-a-room-each
- /wiki/guide-a-dungeon-dimension
- /wiki/guide-scoreboard-with-a-button

## cookbook
- /wiki/cookbook-cooldowns
- /wiki/cookbook-leaderboards
- /wiki/cookbook-teleport-pads
- /wiki/cookbook-kits
- /wiki/cookbook-teams
- /wiki/cookbook-minigame-loop
- /wiki/cookbook-save-load

## appendix
- /appendix/event-catalog
- /appendix/client-versions
- /appendix/limits-table
- /appendix/faq

## reference
- /ref  (index)
- /ref/<Type>       e.g. /ref/World, /ref/Player, /ref/Chunk
- /ref/<Type>/<member>  e.g. /ref/World/block, /ref/Player/give
- lowercase globals alias their type: /ref/world == /ref/World

## Linking rules
- Wiki links: [Display](/wiki/<slug>)
- Guides: [Build a cottage](/wiki/guide-build-a-cottage)
- Ref member links: [`world.block`](/ref/World/block) — type name capitalized
- Ref type links: [`Vec3`](/ref/Vec3)
