---
title: "Suggester type"
description: "Called as the player types; must answer at once (no task.wait)"
---

Called as the player types; must answer at once (no task.wait). `args` holds the arguments typed before this one, by name.

`(player: Player, typed: string, args: { [string]: any }) -> { Suggestion }`
