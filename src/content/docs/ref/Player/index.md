---
title: 'Player type'
description: 'A player in the room: what players.on_join and every player event hand you.'
---

A player in the room: what `players.on_join` and every player event hand you.

## Functions

| Call | Purpose |
| --- | --- |
| [`ride`](/ref/Player/ride/) | The player's name. The account's own id: the one name for a player a rename does not change. Where they stand now. Your own table, kept on the player for as long as they are connected. A player is one value while connected: `a == b` and `t[player]` work. The Room the player is in; nil while they move between rooms. Degrees: `yaw` sideways, `pitch` up or down; live, read only. True while the player sneaks; live. `attack` is the left button held on a block in reach (see player.reach); a client says nothing about a button held on air. True while the player sits on something; live. Seat 1 drives a vehicle; `locked` keeps a sneak from getting them off. `false` when somebody sits in that seat; keeps the current ride on failure. Works immediately after creating the target. Repeating the same ride keeps the seat; no delay or extra movement is needed. |
| [`dismount`](/ref/Player/dismount/) | Gets the player off what they ride; sneaking does the same, as off a horse. |
| [`message`](/ref/Player/message/) | What shows on this player's screen: the calls `ui` has, for them alone, plus their own menu and overlay. Sends a chat line to this player alone; `color` is for the words that did not pick one. Chat is not part of the screen, so it is not in `ui`. |
| [`sound`](/ref/Player/sound/) | Plays a sound by name to this player only, with an optional position, volume, pitch and category. |
| [`teleport`](/ref/Player/teleport/) | Yaw and pitch left out keep the way they face. |
| [`move_to`](/ref/Player/move_to/) | Moves the player to another room; the client swaps worlds in place. |
| [`travel`](/ref/Player/travel/) | Sends the player to another world of the group, at `pos` or its spawn. |
| [`give`](/ref/Player/give/) | One item: "stone", or { item = "arrow", count = 16 }. |
| [`held`](/ref/Player/held/) | Returns the stack in hand ({ item, count }, plus `id` for a pack item and `damage` for a worn tool), or nil. |
| [`inventory`](/ref/Player/inventory/) | Returns one { item, count } row per filled slot. |
| [`take`](/ref/Player/take/) | Up to `count` (1 unless you say) of what matches, the hand first; answers how many it took. |
| [`set_held`](/ref/Player/set_held/) | The stack in hand, replaced; nil or false empties the hand. |
| [`hotbar`](/ref/Player/hotbar/) | Replaces the nine hotbar slots; a missing index is empty. |
| [`wear`](/ref/Player/wear/) | The four armour slots; a piece left out is bare. |
| [`kill`](/ref/Player/kill/) | 0..20, or nil where the game version has no food bar. The food saturation, or nil where the game version has no food bar. True while the player is on the death screen. Kills the player; returns false on a version with no damage rules. |
| [`hide`](/ref/Player/hide/) | This player stops seeing `other`, or sees them again. |
| [`show`](/ref/Player/show/) | This player sees `other` again after a `hide`. |
| [`can_see`](/ref/Player/can_see/) | True unless `other` is not visible or is hidden from this player. |
| [`effect`](/ref/Player/effect/) | A potion effect by its modern name; `duration` in seconds, math.huge for ever. |
| [`clear_effect`](/ref/Player/clear_effect/) | Takes a potion effect off the player, by its modern name. |
| [`push`](/ref/Player/push/) | A shove in blocks per tick, on top of what they are doing. |
| [`damage`](/ref/Player/damage/) | A hit in half-hearts: the flash, the sound, the resistance window. `false` on a version with no damage rules. |
| [`look_at`](/ref/Player/look_at/) | Turns the player's head to a point, where they stand. |
| [`stop_sound`](/ref/Player/stop_sound/) | Where their view is from: the camera they look out of, or their eyes. One sound by name, or every sound; 1.13 and later. |
| [`kick`](/ref/Player/kick/) | Disconnects the player, with that text on their screen. |
| [`connect`](/ref/Player/connect/) | Asks Minefort to move the player to another server by name: an instance's `id`, the network's name (its default member) or "hub". Minefort decides and does not answer; a player still here was not moved. |
| [`count`](/ref/Player/count/) | Returns how many of an item the player carries, across every slot. |
| [`has`](/ref/Player/has/) | True if the player's groups give them this permission node; operators have every node. |
| [`groups`](/ref/Player/groups/) | Returns the player's groups; `default` is not listed. |
| [`add_group`](/ref/Player/add_group/) | Puts the player in a group until they leave; errors on a group citadel.yml does not define. |
| [`remove_group`](/ref/Player/remove_group/) | Takes the player out of a group. |
| [`supports`](/ref/Player/supports/) | True if this player's client can show the feature. |
| [`look`](/ref/Player/look/) | Returns the unit vector the player faces. |
| [`set_slot`](/ref/Player/set_slot/) | Selects hotbar slot 1..9. |

## Fields

| Field | Purpose |
| --- | --- |
| [`player.gamemode: number`](/ref/Player/gamemode/) | The hotbar slot in hand, 1..9; live. 0 survival, 1 creative, 2 adventure, 3 spectator; writable. |
| [`player.spawn_point: Vec3 ?`](/ref/Player/spawn_point/) | The player's own respawn point (the block of the position), or nil for the room's. Writable; a point a pack sets needs no bed. nil clears it, a bed's point too. |
| [`player.max_health: number ?`](/ref/Player/max_health/) | Their health now, 0 to `max_health`; nil where the game version has no damage rules. Writable: set outright, no flash; 0 is a death; a number above `max_health` stops there. The most health they can have: 20 unless a pack set it; nil where the game version has no damage rules. Writable, 1 to 1024; nil gives the game's own back. A lower maximum takes `health` down to it. It lasts for the session. Every Java client draws its hearts; Bedrock draws none. |
| [`player.speed: number`](/ref/Player/speed/) | The body: what a pack sets on a player. See docs/luau-api.md, "Body and movement". Walk speed as a multiple of normal; 0 pins them. |
| [`player.can_fly: boolean`](/ref/Player/can_fly/) | May fly in a mode that cannot. |
| [`player.visible: boolean ?`](/ref/Player/visible/) | false: no other player is sent this body. The tab line stays. true or nil shows the body again. |
| [`player.scale: number`](/ref/Player/scale/) | 1/16 to 16; 1.20.5 and later, older clients stay as they are. |
| [`player.reach: number`](/ref/Player/reach/) | How far a block can be clicked or dug, 0 to 64 blocks (4.5 by default); 1.20.5 and later. Measured from the camera when there is one. |
| [`player.level: number`](/ref/Player/level/) | The experience bar: the number over it, and how full it is (0..1). |
| [`player.xp: number`](/ref/Player/xp/) | How full the experience bar is, 0..1. |
| [`player.camera: (Camera \| false)?`](/ref/Player/camera/) | What they look out of: a camera from camera.fixed/free/orbit/chase, or nil or false for their own eyes. No delay is needed after creating its target. Ends when the target is destroyed or the player leaves the room. |
| [`player.time: (number \| TimeName \| false)?`](/ref/Player/time/) | This player's sky alone, held at a time of day; nil or false gives them the room's again, as does moving rooms. Reads back in ticks. |
