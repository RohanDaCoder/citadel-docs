---
title: 'EntityHandle type'
description: 'A body the world moves: a pack''s own entity, a mob, a stack on the ground'
---

A body the world moves: a pack's own entity, a mob, a stack on the ground. Every read is a fresh look at the world, so a handle to something that has died reads `nil`. Inside a hook the same handle reads the entity as it was at the top of the tick, and its writes land at that hook's own slot.

## Functions

| Call | Purpose |
| --- | --- |
| [`play`](/ref/EntityHandle/play/) | Model size: reads vec3; write a positive number or equal-axis vec3. Nil without a model. Plays a model entity's animation from the start; on the one already playing, `speed` only changes its speed. |
| [`stop`](/ref/EntityHandle/stop/) | Stops a model entity's animation; the parts stay where they are. |
| [`move`](/ref/EntityHandle/move/) | Gone on the next tick. Sets position and optional rotation together. |
| [`destroy`](/ref/EntityHandle/destroy/) |  |
| [`push`](/ref/EntityHandle/push/) | A shove, in blocks a tick, added to what it is already doing. |
| [`settle`](/ref/EntityHandle/settle/) | It stops being an entity and is a block again where it stands. No argument: the entity remembers what it was. |
| [`nearby`](/ref/EntityHandle/nearby/) | What else is around it, by horizontal distance. |

## Fields

| Field | Purpose |
| --- | --- |
| [`entityHandle.id: number`](/ref/EntityHandle/id/) | Its entity id, the one players.on_click reports in `hit.entity_id`. |
| [`entityHandle.name: string ?`](/ref/EntityHandle/name/) | The kind's name: "cow", "rave:rocket". Nil once it is gone. |
| [`entityHandle.alive: boolean`](/ref/EntityHandle/alive/) | Whether it is still in the world. A hook only runs for one that is. |
| [`entityHandle.age: number ?`](/ref/EntityHandle/age/) | Ticks lived. |
| [`entityHandle.velocity: Vec3 ?`](/ref/EntityHandle/velocity/) | Where it is, live; writing it is a teleport. Nil once it is gone. Partial writes preserve other angles; nil after removal. Bodies have no roll. How it is moving, live; writing it is steering by hand. Nil once it is gone. writing it is steering by hand |
| [`entityHandle.on_ground: boolean ?`](/ref/EntityHandle/on_ground/) | Whether it stands on something. Nil once it is gone. |
| [`entityHandle.health: number ?`](/ref/EntityHandle/health/) | Its health now. Nil once it is gone. |
| [`entityHandle.max_health: number ?`](/ref/EntityHandle/max_health/) | The most health its kind gives it. Nil for an entity that is not a mob and once it is gone. Read-only. |
| [`entityHandle.hostile: boolean ?`](/ref/EntityHandle/hostile/) | Whether its kind is hostile. Nil once it is gone. |
| [`entityHandle.physics: Physics ?`](/ref/EntityHandle/physics/) | Which order of operations moves it: "vehicle", "living", "falling", "item" or "none". |
| [`entityHandle.origin: string ?`](/ref/EntityHandle/origin/) | The block it used to be, for anything that arrived through a transition; nil for anything that was never a block. |
| [`entityHandle.data: DataView`](/ref/EntityHandle/data/) | A pack-defined entity's attached record. Nested edits write through. Saved with persist = "save". Built-in entities raise an error on access. on_steer/on_tick views expire after the callback batch; copy to keep a snapshot. |
| [`entityHandle.forward: number`](/ref/EntityHandle/forward/) | The intent fields: what a body *wants* to do, which is what steering is. Writing one outside `on_steer` lasts until the next decision. |
| [`entityHandle.strafe: number`](/ref/EntityHandle/strafe/) | Intent: 1 left, -1 right. A vehicle's seat 1 writes it from the keys every tick. |
| [`entityHandle.jumping: boolean`](/ref/EntityHandle/jumping/) | Intent: whether it wants to jump. A vehicle's seat 1 writes it from the keys every tick. |
| [`entityHandle.flying: boolean`](/ref/EntityHandle/flying/) | Intent, a living body with can_fly only: true flies (no gravity; forward moves it along its look, pitch included), false falls and walks. Setting it true on another body is an error. |
| [`entityHandle.driver: Player ?`](/ref/EntityHandle/driver/) | Whether it is in water now. False for an entity that is not alive. The player supplying driving input from seat 1; nil for an NPC or empty seat. |
| [`entityHandle.paint: { [string]: Ink }`](/ref/EntityHandle/paint/) | Every occupant by seat number, including NPCs; nil means empty. Material name to colour; write-only. |
