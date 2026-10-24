---
title: "EntityAmendSpec type"
description: "Called when a new entity of this kind spawns; told, never waited on."
---

Called when a new entity of this kind spawns; told, never waited on.

## Functions

| Call                                           | Purpose                                                                                                                     |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [`on_spawn`](/ref/EntityAmendSpec/on_spawn/)   | Called when a new entity of this kind spawns; told, never waited on.                                                        |
| [`on_load`](/ref/EntityAmendSpec/on_load/)     | Called for an entity that already existed: a saved chunk loaded it, or a reload rebound it.                                 |
| [`on_steer`](/ref/EntityAmendSpec/on_steer/)   | Wrapped behavior runs first unless options.replace = true.                                                                  |
| [`on_tick`](/ref/EntityAmendSpec/on_tick/)     | Wrapped behavior runs first unless options.replace = true.                                                                  |
| [`on_damage`](/ref/EntityAmendSpec/on_damage/) | Asked when it takes damage; return "ignore" to cancel it. Silence or a missed deadline is "take".                           |
| [`on_remove`](/ref/EntityAmendSpec/on_remove/) | Called when it leaves the world; `why` is "removed", "settled", "killed" or "unloaded". Not called when the pack goes away. |
