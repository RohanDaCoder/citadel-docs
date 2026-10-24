---
title: "Event catalog"
description: "Every on_* event in the Citadel API in one table — what fires it, what the handler receives, and where the full treatment lives."
---

:::note[In short]
every `on_*` subscription in the API, one row each.
Subscribe with the call, keep the connection, cancel to stop. The
model itself — deadlines, asks, ordering — is in
[The event model](/concepts/events/).
:::

62 events across 12 types.

## `BlockAmendSpec`

| Event                                                   | Signature                                                                                                         | Fires when                                                                                                                   |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| [`on_added`](/ref/BlockAmendSpec/on_added/)             | `blockAmendSpec.on_added((block: BlockAt, base: (... any) -> any) -> ()) → ?`                                     | It has just been stored, whatever stored it.                                                                                 |
| [`on_break`](/ref/BlockAmendSpec/on_break/)             | `blockAmendSpec.on_break((block: BlockAt, player: Player ?, by: Breaker, base: (... any) -> any) -> Drops ?) → ?` | Something broke it; `by` says what. Answers "none", "table" or a drops list.                                                 |
| [`on_neighbour`](/ref/BlockAmendSpec/on_neighbour/)     | `blockAmendSpec.on_neighbour((block: BlockAt, from: Vec3, announced: string, base: (... any) -> any) -> ()) → ?`  | A neighbour at `from` changed; `announced` is the block the notifier announced itself as.                                    |
| [`on_place`](/ref/BlockAmendSpec/on_place/)             | `blockAmendSpec.on_place((block: BlockAt, player: Player ?, base: (... any) -> any) -> ()) → ?`                   | A player put it down.                                                                                                        |
| [`on_power`](/ref/BlockAmendSpec/on_power/)             | `blockAmendSpec.on_power((block: BlockAt, powered: boolean, base: (... any) -> any) -> ()) → ?`                   | A redstone signal started (`powered` is true) or stopped reaching it. Called once for each, not for every change beside it.  |
| [`on_random_tick`](/ref/BlockAmendSpec/on_random_tick/) | `blockAmendSpec.on_random_tick((block: BlockAt, base: (... any) -> any) -> ()) → ?`                               | The random pass landed on it.                                                                                                |
| [`on_removed`](/ref/BlockAmendSpec/on_removed/)         | `blockAmendSpec.on_removed((block: BlockAt, base: (... any) -> any) -> ()) → ?`                                   | It has just gone.                                                                                                            |
| [`on_step`](/ref/BlockAmendSpec/on_step/)               | `blockAmendSpec.on_step((block: BlockAt, body: Body, base: (... any) -> any) -> ()) → ?`                          | A body (a player, mob, item or other) is standing on it.                                                                     |
| [`on_tick`](/ref/BlockAmendSpec/on_tick/)               | `blockAmendSpec.on_tick((block: BlockAt, base: (... any) -> any) -> ()) → ?`                                      | A scheduled tick this block asked for came due.                                                                              |
| [`on_trigger`](/ref/BlockAmendSpec/on_trigger/)         | `blockAmendSpec.on_trigger((block: BlockAt, cause: Trigger, base: (... any) -> any) -> ()) → ?`                   | It was lit, blasted or burnt; `cause` is "ignite", "explosion" or "fire".                                                    |
| [`on_use`](/ref/BlockAmendSpec/on_use/)                 | `blockAmendSpec.on_use((block: BlockAt, player: Player ?, held: string ?, base: (... any) -> any) -> Used ?) → ?` | Somebody right-clicked it; `held` is the item in hand. Answers "used" or "pass"; a missed deadline passes the click through. |

## `BlockSpec`

| Event                                              | Signature                                                                                                    | Fires when                                                                                                                  |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| [`on_added`](/ref/BlockSpec/on_added/)             | `blockSpec.on_added((block: BlockAt, base: (... any) -> any) -> ()) → ?`                                     | It has just been stored, whatever stored it.                                                                                |
| [`on_break`](/ref/BlockSpec/on_break/)             | `blockSpec.on_break((block: BlockAt, player: Player ?, by: Breaker, base: (... any) -> any) -> Drops ?) → ?` | Something broke it. Answers "none", "table" or a drops list; fails closed to the definition's `drops`.                      |
| [`on_neighbour`](/ref/BlockSpec/on_neighbour/)     | `blockSpec.on_neighbour((block: BlockAt, from: Vec3, announced: string, base: (... any) -> any) -> ()) → ?`  | A neighbour changed; `from` is its position and `announced` the block name the notifier announced itself as.                |
| [`on_place`](/ref/BlockSpec/on_place/)             | `blockSpec.on_place((block: BlockAt, player: Player ?, base: (... any) -> any) -> ()) → ?`                   | A player put it down; `block.data` is empty then, ready to be filled.                                                       |
| [`on_power`](/ref/BlockSpec/on_power/)             | `blockSpec.on_power((block: BlockAt, powered: boolean, base: (... any) -> any) -> ()) → ?`                   | A redstone signal started (`powered` is true) or stopped reaching it. Called once for each, not for every change beside it. |
| [`on_random_tick`](/ref/BlockSpec/on_random_tick/) | `blockSpec.on_random_tick((block: BlockAt, base: (... any) -> any) -> ()) → ?`                               | The random pass landed on it. Not the same thing as `on_tick`, which is why it has the longer name.                         |
| [`on_removed`](/ref/BlockSpec/on_removed/)         | `blockSpec.on_removed((block: BlockAt, base: (... any) -> any) -> ()) → ?`                                   | It has just gone from the world.                                                                                            |
| [`on_step`](/ref/BlockSpec/on_step/)               | `blockSpec.on_step((block: BlockAt, body: Body, base: (... any) -> any) -> ()) → ?`                          | A body is standing on it; `body` is `{ id, kind }`.                                                                         |
| [`on_tick`](/ref/BlockSpec/on_tick/)               | `blockSpec.on_tick((block: BlockAt, base: (... any) -> any) -> ()) → ?`                                      | A scheduled tick this block asked for came due.                                                                             |
| [`on_trigger`](/ref/BlockSpec/on_trigger/)         | `blockSpec.on_trigger((block: BlockAt, cause: Trigger, base: (... any) -> any) -> ()) → ?`                   | It was lit, blasted or burnt; `cause` is "ignite", "explosion" or "fire".                                                   |
| [`on_use`](/ref/BlockSpec/on_use/)                 | `blockSpec.on_use((block: BlockAt, player: Player ?, held: string ?, base: (... any) -> any) -> Used ?) → ?` | The hooks. Writing one is what asks for it — there is no flag beside `on_random_tick` saying the random pass may land here. |

## `citadel`

| Event                              | Signature                                              | Fires when                                                     |
| ---------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------- |
| [`on_slow`](/ref/citadel/on_slow/) | `citadel.on_slow(fn: (slow: Slow) -> ()) → Connection` | Called when a batch runs out of budget; at most once a second. |

## `EntityAmendSpec`

| Event                                          | Signature                                                                                   | Fires when                                                                                                                  |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [`on_damage`](/ref/EntityAmendSpec/on_damage/) | `entityAmendSpec.on_damage((e: EntityHandle, amount: number) -> ("take" \| "ignore")?) → ?` | Asked when it takes damage; return "ignore" to cancel it. Silence or a missed deadline is "take".                           |
| [`on_load`](/ref/EntityAmendSpec/on_load/)     | `entityAmendSpec.on_load((e: EntityHandle) -> ()) → ?`                                      | Called for an entity that already existed: a saved chunk loaded it, or a reload rebound it.                                 |
| [`on_remove`](/ref/EntityAmendSpec/on_remove/) | `entityAmendSpec.on_remove((e: EntityHandle, why: string ?) -> ()) → ?`                     | Called when it leaves the world; `why` is "removed", "settled", "killed" or "unloaded". Not called when the pack goes away. |
| [`on_spawn`](/ref/EntityAmendSpec/on_spawn/)   | `entityAmendSpec.on_spawn((e: EntityHandle) -> ()) → ?`                                     | Called when a new entity of this kind spawns; told, never waited on.                                                        |
| [`on_steer`](/ref/EntityAmendSpec/on_steer/)   | `entityAmendSpec.on_steer((e: EntityHandle, base: () -> ()) -> ()) → ?`                     | Wrapped behavior runs first unless options.replace = true.                                                                  |
| [`on_tick`](/ref/EntityAmendSpec/on_tick/)     | `entityAmendSpec.on_tick((e: EntityHandle, base: () -> ()) -> ()) → ?`                      | Wrapped behavior runs first unless options.replace = true.                                                                  |

## `EntityHandle`

| Event                                       | Signature                           | Fires when                                           |
| ------------------------------------------- | ----------------------------------- | ---------------------------------------------------- |
| [`on_ground`](/ref/EntityHandle/on_ground/) | `entityHandle.on_ground: boolean ?` | Whether it stands on something. Nil once it is gone. |

## `EntitySpec`

| Event                                     | Signature                                                                                            | Fires when                                                                                                                                                       |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`on_damage`](/ref/EntitySpec/on_damage/) | `entitySpec.on_damage((e: EntityHandle, amount: number, by: Player ?) -> ("take" \| "ignore")?) → ?` | Asked when a player hits it: answer "take" or "ignore". Nil or a missed deadline is "take". `by` is the player who hit.                                          |
| [`on_load`](/ref/EntitySpec/on_load/)     | `entitySpec.on_load((e: EntityHandle) -> ()) → ?`                                                    | Told when one that already existed comes back: a saved chunk loaded it or a reload rebound it.                                                                   |
| [`on_remove`](/ref/EntitySpec/on_remove/) | `entitySpec.on_remove((e: EntityHandle, why: string ?) -> ()) → ?`                                   | Told when it goes; `why` is "removed", "settled", "killed" or "unloaded". Not called when the pack goes away.                                                    |
| [`on_spawn`](/ref/EntitySpec/on_spawn/)   | `entitySpec.on_spawn((e: EntityHandle) -> ()) → ?`                                                   | Told when one of this kind is spawned; nothing waits on it and its answer is not read.                                                                           |
| [`on_steer`](/ref/EntitySpec/on_steer/)   | `entitySpec.on_steer((e: EntityHandle, base: () -> ()) -> ()) → ?`                                   | Runs before the physics each tick to decide where it goes; call `base(e)` to extend, leave it out to replace.                                                    |
| [`on_think`](/ref/EntitySpec/on_think/)   | `entitySpec.on_think((b: Think) -> ()) → ?`                                                          | define only. The brain: one call for all due bodies of the kind, with their numbers in columns. The engine never waits for it; the answer lands on the next t... |
| [`on_tick`](/ref/EntitySpec/on_tick/)     | `entitySpec.on_tick((e: EntityHandle, base: () -> ()) -> ()) → ?`                                    | Runs after the physics each tick to react to where it ended up; call `base(e)` to extend.                                                                        |

## `network`

| Event                                      | Signature                                                                      | Fires when                                      |
| ------------------------------------------ | ------------------------------------------------------------------------------ | ----------------------------------------------- |
| [`on_gone`](/ref/network/on_gone/)         | `network.on_gone(handler: (id: string) -> ()) → Connection`                    | Called with the id of an instance that is gone. |
| [`on_instance`](/ref/network/on_instance/) | `network.on_instance(handler: (instance: NetworkInstance) -> ()) → Connection` | Called when an instance starts or changes.      |

## `Players`

| Event                                    | Signature                                                                                                   | Fires when                                                                                                                                                       |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`on_break`](/ref/Players/on_break/)     | `players.on_break(fn: (player: Player ?, pos: Vec3, block: string) -> boolean ?) → Connection`              | Cancellable. Return `false` to stop it; return nothing to let it through. These are asked _before_ the world changes and the engine waits milliseconds for th... |
| [`on_chat`](/ref/Players/on_chat/)       | `players.on_chat(fn: (player: Player, text: string) -> boolean ?) → Connection`                             | Return false and the line is not said.                                                                                                                           |
| [`on_click`](/ref/Players/on_click/)     | `players.on_click(fn: (player: Player, hit: Hit) -> ()) → Connection`                                       | Calls `fn` on a left or right click; `hit` holds the button and the entity, player, block and face it met.                                                       |
| [`on_damage`](/ref/Players/on_damage/)   | `players.on_damage(fn: (player: Player ?, hit: DamageHit) -> boolean ?) → Connection`                       | Asks `fn` before damage lands on a player; return false to refuse it. A missed deadline denies it. A pack's own `player:damage` is not asked about.              |
| [`on_death`](/ref/Players/on_death/)     | `players.on_death(fn: (player: Player ?, cause: string, message: string, by: Player ?) -> ()) → Connection` | Calls `fn` when a player dies, with the cause (fall, drown, void, lava, ...) and the line broadcast; `player` is nil once they have left.                        |
| [`on_drop`](/ref/Players/on_drop/)       | `players.on_drop(fn: (player: Player ?, item: string, count: number) -> ()) → Connection`                   | Calls `fn` when a stack lands on the ground; `player` is nil where the world dropped it or they have left.                                                       |
| [`on_join`](/ref/Players/on_join/)       | `players.on_join(fn: (player: Player) -> ()) → Connection`                                                  | Calls `fn` when a player arrives: on the globals when a client connects, on a room's table each time a player moves into it.                                     |
| [`on_leave`](/ref/Players/on_leave/)     | `players.on_leave(fn: (player: Player) -> ()) → Connection`                                                 | The same player value on_join had; it can no longer be sent to.                                                                                                  |
| [`on_pickup`](/ref/Players/on_pickup/)   | `players.on_pickup(fn: (player: Player ?, item: string, count: number) -> ()) → Connection`                 | A stack taken off the ground, and one that landed on it. `player` is nil where the world dropped it, or where they have already left.                            |
| [`on_place`](/ref/Players/on_place/)     | `players.on_place(fn: (player: Player ?, pos: Vec3, block: string) -> boolean ?) → Connection`              | Asks `fn` before a player puts a block down; return false to cancel it. A missed deadline denies the place.                                                      |
| [`on_respawn`](/ref/Players/on_respawn/) | `players.on_respawn(fn: (player: Player ?) -> ()) → Connection`                                             | Calls `fn` when a player respawns; `player` is nil once they have left.                                                                                          |
| [`on_slot`](/ref/Players/on_slot/)       | `players.on_slot(fn: (player: Player, slot: number) -> ()) → Connection`                                    | Calls `fn` when a player picks a hotbar slot, 1..9.                                                                                                              |
| [`on_sneak`](/ref/Players/on_sneak/)     | `players.on_sneak(fn: (player: Player, down: boolean) -> ()) → Connection`                                  | Calls `fn` once per sneak press and release; `down` is true on the press.                                                                                        |

## `Screen`

| Event                               | Signature                                                                                                 | Fires when                                                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| [`on_click`](/ref/Screen/on_click/) | `screen.on_click(((player: Player, x: number, y: number, button: "left" \| "right") -> ()) \| false) → ?` | Called with the pixel the player points at and the button, when a player clicks the screen. nil or false takes the hook off. |

## `shop`

| Event                                   | Signature                                                                | Fires when                                                                                                                     |
| --------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| [`on_declined`](/ref/shop/on_declined/) | `shop.on_declined(handler: (purchase: ShopPurchase) -> ()) → Connection` | Called when the player said no or did not answer.                                                                              |
| [`on_paid`](/ref/shop/on_paid/)         | `shop.on_paid(handler: (purchase: ShopPurchase) -> ()) → Connection`     | Called once per paid purchase; returning without an error hands it over. An error leaves it waiting, to be called again later. |

## `time`

| Event                           | Signature                                             | Fires when                                                                     |
| ------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------ |
| [`on_tick`](/ref/time/on_tick/) | `time.on_tick(fn: (tick: number) -> ()) → Connection` | Calls `fn` every tick, 20 times a second, with the tick number; keep it short. |

## `World`

| Event                                            | Signature                                                                                   | Fires when                                                                                                                                                       |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`on_block_break`](/ref/World/on_block_break/)   | `world.on_block_break(fn: (player: Player ?, pos: Vec3, block: string) -> ()) → Connection` | What the survival tick did. Observe-only: the world has already changed, and what the callback returns is not read.                                              |
| [`on_block_place`](/ref/World/on_block_place/)   | `world.on_block_place(fn: (player: Player ?, pos: Vec3, block: string) -> ()) → Connection` | Tells after a block was placed, with its canonical name. Observe-only; `player` is nil when nobody placed it or they left.                                       |
| [`on_entity_death`](/ref/World/on_entity_death/) | `world.on_entity_death(fn: (id: number, name: string) -> ()) → Connection`                  | Tells after a mob died; it is gone, so its id and name is all there is. Mob kinds only.                                                                          |
| [`on_entity_spawn`](/ref/World/on_entity_spawn/) | `world.on_entity_spawn(fn: (entity: EntityHandle, name: string) -> ()) → Connection`        | Tells after a mob appeared, with its handle and name; a natural spawn fires it on every game version that has one, and a pack's own `world.spawn("cow", pos)`... |
| [`on_generate`](/ref/World/on_generate/)         | `world.on_generate(fn: (chunk: Chunk) -> ())`                                               | Called for a chunk each time it comes into memory, in a script world; it must make the same blocks every time.                                                   |
| [`on_populate`](/ref/World/on_populate/)         | `world.on_populate(fn: (chunk: Chunk) -> ())`                                               | Each chunk the overworld terrain made, once, after it made it.                                                                                                   |

## See also

- [The event model](/concepts/events/) — subscriptions, asks, deadlines.
- [Runtime](/concepts/runtime/) — the event queue and its 4096 cap.
