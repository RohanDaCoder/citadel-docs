---
title: Entity handles
section: entities
order: 2
description: The EntityHandle API — the live handle world.spawn returns, world.entities lists and every hook receives: position and rotation, velocity and push, nearby queries, e.data, and life checks.
tags: [entities, entity-handle, world-spawn, queries, data-views]
---
# Entity handles

> **In short:** A handle is a live view of **a body the world moves** — a
> pack's own entity, a mob, a stack on the ground. `world.spawn` returns one,
> `world.entities()` lists them, and each hook gets one. A mob has the same
> handle as every entity the world moves: `cow.velocity`, `cow:push(v)` and
> `cow:nearby(8)` all work. Every read is a fresh look at the world, so check
> `alive` before you trust what you read.

## What a handle is

The [`EntityHandle`](/ref/EntityHandle) is the one type behind every body the
world moves — a pack's own entity, a mob, a stack on the ground. Wherever you
get one from, it behaves the same:

- `world.spawn` returns a handle; `world.entities()` lists handles; each hook (`on_steer`, `on_tick`, `on_spawn`, ...) gets one.
- Every read is a fresh look at the world. A handle to something that has died reads `nil` on its fields — so **check `alive`** before you use what you read.
- Inside a hook, the same handle reads the entity as it was at the top of the tick, and its writes land at that hook's own slot.
- `tostring(cow)` is `entity(cow, 7)`: the kind's name and the id.

## Position and rotation

`at` is where its feet are; `rotation` is which way it faces. Both are live —
set them and the entity is there:

| Read / call | What it is |
| --- | --- |
| `entity.at` | where it is, live; writing it is a teleport. `nil` once it is gone. |
| `entity.rotation` | a table of degree angles. Bodies have no roll: yaw and pitch. Partial writes preserve omitted angles; `nil` after removal. |
| `entity:move(at, rotation?)` | sets position and optional rotation together. |

- 0 yaw faces south (+z), 90 faces west; positive pitch tips down. For a living body, `e.rotation.yaw` is one of the intent fields: it keeps the heading until you change it.
- `move` changes position and rotation in one operation, and validates both before applying either. Entities keep simulating after a move: changing their position does not clear velocity.
- Writing the current position with `at` or `move` is the normal way to place an entity; the engine smooths visual movement.

## Velocity, push and intent

There are two ways to move a body by hand — a shove now, or an intent it keeps
— and the intent fields are the ones steering uses:

| Field / call | What it is |
| --- | --- |
| `entity.velocity` | how it is moving, live; writing it is steering by hand — a push. `nil` once it is gone. |
| `entity:push(v)` | a shove, in blocks a tick, added to what it is already doing. |
| `entity.forward`, `entity.strafe` | intent, -1 to 1. `strafe` is 1 left, -1 right. |
| `entity.jumping` | intent: whether it wants to jump. |
| `entity.flying` | intent, a living body with `can_fly` only: `true` flies, `false` falls and walks. |

- A body keeps its intent until you change it. Outside a hook, writing `e.forward`, `e.strafe`, `e.jumping` and `e.flying` on a world handle changes the body at once.
- `e.flying = true` on a body without `can_fly` is an error; `e.flying` reads `false` there.
- A vehicle's seat 1 writes `forward`, `strafe` and `jumping` from the keys every tick. See [Displays and 3D models](/wiki/displays).
- `entity.in_water` is `true` while it is in water.

## Finding entities

`world.entities()` with no argument returns all entities. For a local query,
give a position and a radius. You can also filter by kind:

```luau
local cows = world.entities {
    near = vec3(8, 65, 8),
    radius = 16,
    kind = "cow",
}
for _, cow in cows do
    cow:push(vec3(0, 0.1, 0))
end

local allCows = world.entities { kind = "cow" }
```

| Option of `world.entities(query)` | Meaning |
| --- | --- |
| — (no argument) | all entities |
| `near`, `radius` | a sphere, boundary included. They go together. |
| `kind` | the handle's canonical name, with the pack namespace for a custom kind |
| `mob` | `true`: the mobs only; `false`: the rest |

- Results are handles in ascending id order. Queued spawns are included; removed entities are not.
- Invalid options, a negative radius and non-finite numbers raise an error. An unknown kind returns an empty list.
- `entity:nearby(radius)` measures horizontal distance and excludes the entity itself.

## The fields

What a handle reads, beyond position and movement above. Most go `nil` once
the entity is gone:

| Field | What it is |
| --- | --- |
| `id` | its entity id, the one `players.on_click` reports in `hit.entity_id` |
| `name` | the kind's name: `"cow"`, `"rave:rocket"`. `nil` once it is gone. |
| `alive` | whether it is still in the world. A hook only runs for one that is. |
| `age` | ticks lived. |
| `at`, `rotation` | where it is and where it looks; see [position and rotation](#position-and-rotation) |
| `velocity` | how it is moving; see [velocity, push and intent](#velocity-push-and-intent) |
| `forward`, `strafe`, `jumping`, `flying` | the intent fields |
| `on_ground` | whether it stands on something. `nil` once it is gone. |
| `in_water` | `true` while it is in water |
| `health` | its health now. `nil` once it is gone. |
| `max_health` | the most health its kind gives it. Read-only; `nil` for an entity that is not a mob and once it is gone. |
| `hostile` | whether its kind is hostile. `nil` once it is gone. |
| `physics` | which order of operations moves it: `"vehicle"`, `"living"`, `"falling"`, `"item"` or `"none"` |
| `origin` | the block it used to be, for anything that arrived through a transition; `nil` for anything that was never a block |
| `data` | a pack-defined entity's attached record; see below |
| `driver` | the player supplying driving input from seat 1; `nil` for an NPC or empty seat |
| `paint` | material name to colour; write-only |

A model entity (a kind with `looks = models.x`) also has `scale` — `nil`
without a model — and the animation calls `entity:play(animation, { speed = n })`
and `entity:stop(animation)`: `play` starts a model animation from the start,
and on the one already playing only changes its speed; `stop` leaves the parts
where they are.

## e.data

`e.data` is a data view for a **pack-defined entity**, including one with
`physics = "living"`:

- Nested writes persist through both callback and world handles. It saves with the chunk only when the kind has `persist = "save"`.
- Reading or assigning `.data` on a **built-in entity**, including an amended one, raises an error: its engine-owned state is not a pack data record.
- Keep temporary state for built-in entities in a pack table keyed by entity id; ids do not provide a persistent identity across server restarts.
- `on_steer`/`on_tick` data views expire after the callback batch; copy out what you need to keep a snapshot.

## Amending reaches live entities

An amend is not a respawn: `game.entities.amend("pig", { ... })` changes
**pigs already in the world** the moment it runs, and every pig after, with no
respawn. The hooks change; the entities stay. What an amend cannot change —
`size`, `looks`, `physics`, `max_health`, `speed`, `persist` — and the
wrapping of `base` are in [Custom entities](/wiki/custom-entities).

## Life, death and removal

The end of an entity is a read like any other — `alive` goes `false`, the
other fields `nil` — with two calls and two events around it:

- `entity:destroy()` removes it.
- `entity:settle()` stops it being an entity: it is a block again where it stands. No argument: the entity remembers what it was (its `origin`).
- A living body at 0 health dies as a mob: it falls over, leaves its `drops`, and is gone a second later. `on_remove` gets `"killed"`, and `world.on_entity_death` fires with its id and name.
- `world.on_entity_spawn` tells after a mob appeared, with its handle and name; a natural spawn fires it on every game version that has one, and a pack's own `world.spawn("cow", pos)` fires it too. Mob kinds only.
- `on_remove` is told `"removed"`, `"settled"`, `"killed"` or `"unloaded"`. It does **not** fire when your pack is removed.

## See also

- [Custom entities](/wiki/custom-entities) — `define` and `amend`, the hooks, the `on_think` brain.
- [Mobs and spawning](/wiki/mobs) — `world.spawn` on the game's own kinds, natural spawning, drops.
- [Displays and 3D models](/wiki/displays) — vehicles, seats, and the shared `id`/`alive`/`at`/`rotation`/`:move` contract.
- [Game data](/wiki/game-data) — a kind's facts from `game.entities.<kind>`.
- [The event model](/wiki/events) — `world.on_entity_spawn`, `world.on_entity_death` and the other `on_*` subscriptions.
