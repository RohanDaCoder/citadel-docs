---
title: 'API reference'
description: 'Every Citadel global, type and member — 29 globals in five domains, 141 types, 674 documented members, each with signature, parameters, returns and usage.'
---

Every global, type and call in Citadel, one page each: the signature,
the parameters, the returns, and the guides that use it. Pick a domain,
or browse the types.

## World & game

| Global | What it is |
| --- | --- |
| [`world`](/ref/World/) | A room's blocks, entities, displays, screens and time — the `world` global, or `room.world`. Start here for terrain, block writes, entities in the world, and world rules. |
| [`game`](/ref/Game/) | The game version's own facts — blocks, items, entity kinds, terrain — and the pack's definitions of its own blocks and entities. |
| [`models`](/ref/models/) | The models this pack makes, for `world.display{ kind = "model" }`. |
| [`parts`](/ref/parts/) | Named parts of a stored world and the generators that build them. |
| [`routes`](/ref/routes/) | How players get between the worlds of the group. |
| [`noise`](/ref/noise/) | Smooth random numbers for a generator, made by the engine. |
| [`fields`](/ref/fields/) | Recipes for numbers over the world, for `world.generate`. |
| [`data`](/ref/data/) | Helpers for persistent data views — `data.copy`, `data.insert`, `data.remove`. |

## Players

| Global | What it is |
| --- | --- |
| [`players`](/ref/Players/) | Everyone in the room: joins and leaves, clicks and chat, inventory, visibility and health — the `players` global, or `room.players`. |
| [`camera`](/ref/camera/) | Camera paths and modes per player. |

## Interface & media

| Global | What it is |
| --- | --- |
| [`ui`](/ref/Ui/) | What the players see: titles, chat lines, sidebars, boss bars, screens, menus and dialogs — the `ui` global, or `room.ui`. |
| [`fx`](/ref/Fx/) | Particles: `fx.particle` with count, spread, velocity and dust colour. |
| [`sound`](/ref/Sound/) | Sound by name from the resource pack, or streamed through Simple Voice Chat. |
| [`message`](/ref/message/) | A chat line to everyone in the main room. |
| [`tween`](/ref/tween/) | Any live field eased over time — numbers, vec3 and color values. |
| [`color`](/ref/color/) | Colour helpers: hsv, gradients and nearest-map-colour. |
| [`colors`](/ref/colors/) | The named colour table: Minecraft's sixteen and more. |

## Systems

| Global | What it is |
| --- | --- |
| [`commands`](/ref/Commands/) | `commands.add` with typed arguments, tab-completion, permissions and aliases. |
| [`time`](/ref/time/) | Clocks for a pack: a callback every tick, one every few seconds, and the seconds since the pack started. |
| [`task`](/ref/task/) | The scheduler: `spawn`, `delay`, `defer`, `wait` and `cancel`. |
| [`rooms`](/ref/rooms/) | Making and destroying rooms — isolated worlds with their own tables. |
| [`storage`](/ref/storage/) | A per-pack JSON file that survives a restart. |
| [`stores`](/ref/stores/) | The experience's shared store: versioned facts, blobs and leases across every server. |
| [`http`](/ref/http/) | HTTP requests from the pack, with caching. |
| [`network`](/ref/network/) | WebSockets out and listening sockets, for multiplayer-scale IO. |
| [`shop`](/ref/shop/) | Minefort's Gem shop: prompts, ownership and paid delivery. |
| [`hub`](/ref/hub/) | The Minefort hub: servers, experiences and portals. |

## Engine

| Global | What it is |
| --- | --- |
| [`citadel`](/ref/citadel/) | The engine itself: the log, versions, environment and the tick budget. |
| [`vec3`](/ref/vec3/) | Positions and directions with `x`, `y`, `z` — plus `lerp`, `distance` and friends. |

## Types A–Z

[`AskCount`](/ref/AskCount/) · [`Asks`](/ref/Asks/) · [`Bar`](/ref/Bar/) · [`BarColor`](/ref/BarColor/) · [`Billboard`](/ref/Billboard/) · [`BiomeDefinition`](/ref/BiomeDefinition/) · [`Biomes`](/ref/Biomes/) · [`Block`](/ref/Block/) · [`BlockAmendSpec`](/ref/BlockAmendSpec/) · [`BlockAt`](/ref/BlockAt/) · [`BlockDef`](/ref/BlockDef/) · [`BlockPick`](/ref/BlockPick/) · [`BlockRef`](/ref/BlockRef/) · [`Blocks`](/ref/Blocks/) · [`BlockSpec`](/ref/BlockSpec/) · [`Body`](/ref/Body/) · [`BodyRotation`](/ref/BodyRotation/) · [`Breaker`](/ref/Breaker/) · [`BrowseEntry`](/ref/BrowseEntry/) · [`Budget`](/ref/Budget/) · [`Builder`](/ref/Builder/) · [`Camera`](/ref/Camera/) · [`Canvas`](/ref/Canvas/) · [`ChaseCamera`](/ref/ChaseCamera/) · [`Chunk`](/ref/Chunk/) · [`Color`](/ref/Color/) · [`ColorName`](/ref/ColorName/) · [`Command`](/ref/Command/) · [`CommandOpts`](/ref/CommandOpts/) · [`Connection`](/ref/Connection/) · [`Container`](/ref/Container/) · [`Context`](/ref/Context/) · [`DamageHit`](/ref/DamageHit/) · [`DataView`](/ref/DataView/) · [`Dialog`](/ref/Dialog/) · [`DialogNode`](/ref/DialogNode/) · [`Display`](/ref/Display/) · [`Drops`](/ref/Drops/) · [`DurableStore`](/ref/DurableStore/) · [`Easing`](/ref/Easing/) · [`Effect`](/ref/Effect/) · [`Entities`](/ref/Entities/) · [`EntityAmendOptions`](/ref/EntityAmendOptions/) · [`EntityAmendSpec`](/ref/EntityAmendSpec/) · [`EntityCamera`](/ref/EntityCamera/) · [`EntityDef`](/ref/EntityDef/) · [`EntityHandle`](/ref/EntityHandle/) · [`EntityKind`](/ref/EntityKind/) · [`EntitySpec`](/ref/EntitySpec/) · [`Face`](/ref/Face/) · [`Faces`](/ref/Faces/) · [`Facing`](/ref/Facing/) · [`Feature`](/ref/Feature/) · [`Field`](/ref/Field/) · [`FixedCamera`](/ref/FixedCamera/) · [`FluidRule`](/ref/FluidRule/) · [`FreeCamera`](/ref/FreeCamera/) · [`Generated`](/ref/Generated/) · [`GeneratorRules`](/ref/GeneratorRules/) · [`GroundItem`](/ref/GroundItem/) · [`GroundRule`](/ref/GroundRule/) · [`HeadSkin`](/ref/HeadSkin/) · [`Hit`](/ref/Hit/) · [`Hitbox`](/ref/Hitbox/) · [`HttpResponse`](/ref/HttpResponse/) · [`Hud`](/ref/Hud/) · [`HudPart`](/ref/HudPart/) · [`Ink`](/ref/Ink/) · [`InventorySlot`](/ref/InventorySlot/) · [`Item`](/ref/Item/) · [`ItemMatch`](/ref/ItemMatch/) · [`ItemMeta`](/ref/ItemMeta/) · [`Items`](/ref/Items/) · [`ItemSpec`](/ref/ItemSpec/) · [`ItemTable`](/ref/ItemTable/) · [`Layout`](/ref/Layout/) · [`LayoutAlign`](/ref/LayoutAlign/) · [`LayoutNode`](/ref/LayoutNode/) · [`LetterStyle`](/ref/LetterStyle/) · [`LightSource`](/ref/LightSource/) · [`Looks`](/ref/Looks/) · [`Material`](/ref/Material/) · [`Menu`](/ref/Menu/) · [`Model`](/ref/Model/) · [`ModelBuild`](/ref/ModelBuild/) · [`ModelDisplay`](/ref/ModelDisplay/) · [`ModelMaterial`](/ref/ModelMaterial/) · [`ModelPart`](/ref/ModelPart/) · [`ModelSkin`](/ref/ModelSkin/) · [`ModelTexture`](/ref/ModelTexture/) · [`MountTarget`](/ref/MountTarget/) · [`NetworkInstance`](/ref/NetworkInstance/) · [`NetworkStarted`](/ref/NetworkStarted/) · [`Noise`](/ref/Noise/) · [`Npc`](/ref/Npc/) · [`NpcPose`](/ref/NpcPose/) · [`Occupant`](/ref/Occupant/) · [`OrbitCamera`](/ref/OrbitCamera/) · [`Orientation`](/ref/Orientation/) · [`Overlay`](/ref/Overlay/) · [`PartDefinition`](/ref/PartDefinition/) · [`Persist`](/ref/Persist/) · [`Physics`](/ref/Physics/) · [`Picture`](/ref/Picture/) · [`PlantRule`](/ref/PlantRule/) · [`Player`](/ref/Player/) · [`PlayerUi`](/ref/PlayerUi/) · [`Puppet`](/ref/Puppet/) · [`RayHit`](/ref/RayHit/) · [`Recipes`](/ref/Recipes/) · [`Room`](/ref/Room/) · [`Rotation`](/ref/Rotation/) · [`Rules`](/ref/Rules/) · [`Schematic`](/ref/Schematic/) · [`Screen`](/ref/Screen/) · [`ScreenFacing`](/ref/ScreenFacing/) · [`ShopPurchase`](/ref/ShopPurchase/) · [`Slow`](/ref/Slow/) · [`Socket`](/ref/Socket/) · [`SocketMessage`](/ref/SocketMessage/) · [`SoundSpeaker`](/ref/SoundSpeaker/) · [`SoundStream`](/ref/SoundStream/) · [`Suggester`](/ref/Suggester/) · [`Suggestion`](/ref/Suggestion/) · [`TerrainStep`](/ref/TerrainStep/) · [`Text`](/ref/Text/) · [`TextRuns`](/ref/TextRuns/) · [`Texture`](/ref/Texture/) · [`TextureRef`](/ref/TextureRef/) · [`ThingGrid`](/ref/ThingGrid/) · [`ThingRule`](/ref/ThingRule/) · [`Think`](/ref/Think/) · [`TimeName`](/ref/TimeName/) · [`Trigger`](/ref/Trigger/) · [`Tween`](/ref/Tween/) · [`Used`](/ref/Used/) · [`Vec3`](/ref/Vec3/) · [`Video`](/ref/Video/) · [`View`](/ref/View/) · [`WorldTarget`](/ref/WorldTarget/) · [`Worn`](/ref/Worn/) · [`Zone`](/ref/Zone/)
