---
title: "player:ride"
url: /docs/citadel/reference/Player/ride
---

# player:ride

The player's name. The account's own id: the one name for a player a rename does not change. Where they stand now. Your own table, kept on the player for as long as they are connected. A player is one value while connected: `a == b` and `t[player]` work. The Room the player is in; nil while they move between rooms. Degrees: `yaw` sideways, `pitch` up or down; live, read only. True while the player sneaks; live. `attack` is the left button held on a block in reach (see player.reach); a client says nothing about a button held on air. True while the player sits on something; live. Seat 1 drives a vehicle; `locked` keeps a sneak from getting them off. `false` when somebody sits in that seat; keeps the current ride on failure. Works immediately after creating the target. Repeating the same ride keeps the seat; no delay or extra movement is needed.

```
player:ride(thing: MountTarget, opts: { seat: number?, locked: boolean? }?) → boolean
```


## Parameters


## Returns


## Used in
- [`Likewise, `player:ride` while a free/orbit camera is active is an error;`Cameras](/docs/citadel/cameras)
- [`- For the driver's own eyes, seat them: `player:ride(car, { locked = true })``Cameras](/docs/citadel/cameras)
- [`player:ride(thing) -> boolean -- sit on a display, a model, a hitbox or an npc, and go where it goes;`Input](/docs/citadel/input)
- [`player:ride(c) -- seat 1: W and S throttle, A and D steer`Displays](/docs/citadel/displays)
- [`- A seat holds one rider. `player:ride` and `npc:ride` return `false` for a`Displays](/docs/citadel/displays)
- [`n:ride(car, { seat = 2 }) -> boolean -- sits as player:ride does; false when that seat is taken`NPCs](/docs/citadel/npcs)
- [`**Riding.** `n:ride(thing, { seat = n })` takes what `player:ride` takes: a`NPCs](/docs/citadel/npcs)
