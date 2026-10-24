---
title: "game.entities"
description: "The kinds of entity: define a pack's own, amend the game's own, and read a kind of the game: a mob kind by either spelling (game.entities.cow, game.entities.Cow), a kind that is not a mob by its name"
---

Part of [`game`](/ref/Game/).

```luau
game.entities: Entities & { [string]: (EntityKind | EntityDef)? }
```

The kinds of entity: `define` a pack's own, `amend` the game's own, and read a kind of the game: a mob kind by either spelling (`game.entities.cow`, `game.entities.Cow`), a kind that is not a mob by its name (`game.entities.arrow`); nil where the game has none. It iterates every kind, including pack definitions: `for name, kind in game.entities do`.

## Used in

> "game.entities.names { mob = true } -- {"pig", "sheep", "cow", ...}" — [Game data](/world/game-data/)
> "entity here: players are in `players`, never in `world.entities`. `game.entities.<kind>`" — [Game data](/world/game-data/)
> "\| Physics, gameplay hooks or persistence \| `game.entities.define` and `world.spawn` \| Gives a body behavior independent of its appearance. \|" — [Displays](/ui/displays/)
> "local car = game.entities.define {" — [Displays](/ui/displays/)
> "`game.entities.<kind>`." — [Custom entities](/entities/custom-entities/)
> "game.entities.amend("pig", {" — [Custom entities](/entities/custom-entities/)
