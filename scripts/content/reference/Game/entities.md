---
title: "game.entities"
url: /docs/citadel/reference/Game/entities
---

# game.entities

The kinds of entity: `define` a pack's own, `amend` the game's own, and read a kind of the game: a mob kind by either spelling (`game.entities.cow`, `game.entities.Cow`), a kind that is not a mob by its name (`game.entities.arrow`); nil where the game has none. It iterates every kind, including pack definitions: `for name, kind in game.entities do`.

```
game.entities: Entities & { [string]: (EntityKind | EntityDef)? }
```


## Used in
- [`game.entities.names { mob = true } -- {"pig", "sheep", "cow", ...}`Game data](/docs/citadel/game-data)
- [`entity here: players are in `players`, never in `world.entities`. `game.entities.<kind>``Game data](/docs/citadel/game-data)
- [`| Physics, gameplay hooks or persistence | `game.entities.define` and `world.spawn` | Gives a body behavior independent of its appearance. |`Displays](/docs/citadel/displays)
- [`local car = game.entities.define {`Displays](/docs/citadel/displays)
- [``game.entities.<kind>`.`Custom entities](/docs/citadel/custom-entities)
- [`game.entities.amend("pig", {`Custom entities](/docs/citadel/custom-entities)
- [`in `game.entities.define`, which answers `"take"` or `"ignore"`.`Cancelling events](/docs/citadel/cancelling-events)
