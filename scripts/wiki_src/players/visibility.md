---
title: Visibility and teams
section: players
order: 4
description: Who sees whom — player.visible removes a body from every client, viewer:hide removes it from one viewer only, and can_see reads the two together; what hidden means, how long it lasts and what a new session resets.
tags: [visibility, hide, show, teams, lobby, invisibility]
---
# Visibility and teams

> **In short:** a player sees others in their room who are in view. Two
> settings remove a player's body from a client: `player.visible = false`
> (from everyone) and `viewer:hide(player)` (from that viewer only). The
> teams pattern pairs `hide`/`show` with `player.data.team`. Hidden is not the
> `invisibility` effect, the tab list still shows hidden players, and a new
> session resets everything.

## Who sees whom

A player sees others in their room who are in view. Two settings remove a
player's body from a client:

```luau
player.visible = false        -- from everyone; true or nil brings it back
viewer:hide(player)           -- from this viewer only; viewer:show(player) undoes it
viewer:can_see(player)        -- what the two add up to
```

| Setting | Effect |
| --- | --- |
| [`player.visible = false`](/ref/Player/visible) | No other player is sent this body. `true` or `nil` shows the body again. |
| [`viewer:hide(player)`](/ref/Player/hide) | This viewer stops seeing `player`. |
| [`viewer:show(player)`](/ref/Player/show) | This viewer sees `player` again after a `hide`. |
| [`viewer:can_see(player)`](/ref/Player/can_see) | True unless `player` is not visible or is hidden from this viewer. |

> **Note:** `player.visible = nil` shows the player again, because a player is
> visible by default.

## Two patterns

The source's own examples — a lobby, and teams.

A lobby where nobody sees anyone:

```luau
-- a lobby where nobody sees anyone
room.players.on_join(function(p) p.visible = false end)
room.players.on_leave(function(p) p.visible = true end)
```

Teams: each side sees only its own. The loops pair every player against every
player — [`players.list()`](/ref/Players/list) returns every player in the
room — and `data.team` decides:

```luau
-- teams: each side sees only its own
for _, a in players.list() do
    for _, b in players.list() do
        if a.data.team ~= b.data.team then a:hide(b) else a:show(b) end
    end
end
```

Run the pairing again whenever a player joins, leaves or changes team. The
cookbook walks the full pattern in [Teams](/wiki/cookbook-teams).

## What hidden means

- A hidden player is gone from that client: no body, name, armour or hitbox.
- The `invisibility` effect differs: it shows armour and the held item.
- The tab list still shows hidden players.
- Free/orbit cameras hide the body too, independently of potion effects (see
  [Movement and cameras](/wiki/movement)).

> **Gotcha:** Hiding a player is not the `invisibility` effect. The effect
> leaves armour and the held item drawn; `hide` and `visible = false` remove
> body, name, armour and hitbox from the client entirely.

## How long it lasts

Both settings last across rooms. `hide` is by account — it survives the other
player's rejoin. Only a new session resets: nothing hidden, and `visible` is
true again.

## See also

- [Teams](/wiki/cookbook-teams) — the full teams pattern with `player.data`.
- [Player lifecycle](/wiki/player-lifecycle) — sessions, joins and leaves.
- [Rooms and dimensions](/wiki/rooms-and-dimensions) — a player sees others in their room.
- [Movement and cameras](/wiki/movement) — `free`/`orbit` cameras hide the body too.
