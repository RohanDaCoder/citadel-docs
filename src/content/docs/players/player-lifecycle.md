---
title: 'Player lifecycle'
description: 'The four player events — on_join, on_leave, on_death and on_respawn — the one player value and its per-session data table, what survives a reconnect, and moving a player to another server with player:connect.'
---

:::note[In short]
a player is one Luau value for as long as they are connected —
every event hands you that same value, and your own state lives on it as
`player.data`. Four events mark the path: join, leave, death and respawn.
One twist: the global `players` table and a room's own `room.players` fire
`on_join` at different moments. Nothing of `data` survives a rejoin, so
persist what matters in `storage`. A player can also leave for another
server entirely, with `player:connect`.
:::

## Joining and leaving

Which table you subscribe on decides when the event fires.

- The global [`players.on_join`](/ref/Players/on_join/) fires **on connect**, in
  the main room. A room's own `room.players.on_join` fires **on each move
  into it** — after every `player:move_to(room)`.
- `players.on_leave` matches: the same player value `on_join` had; it can no
  longer be sent to.

```luau
room.players.on_join(function(p) end)  -- fires after move_to as well
print(player.room == room)             -- rooms compare by identity; nil while moving
```

:::note
On a script reload, `players.on_join` runs again for every online
player. Make it safe to run twice.
:::

## The four events

Every lifecycle subscription returns a connection; `connection:cancel()`
unsubscribes (see [The event model](/concepts/events/)).

| Event                                           | Callback                         | Fires                                                                   |
| ----------------------------------------------- | -------------------------------- | ----------------------------------------------------------------------- |
| [`players.on_join`](/ref/Players/on_join/)       | `(player)`                       | A client connects (global table); each move into a room (room's table). |
| [`players.on_leave`](/ref/Players/on_leave/)     | `(player)`                       | The same player value `on_join` had; it can no longer be sent to.       |
| [`players.on_death`](/ref/Players/on_death/)     | `(player?, cause, message, by?)` | A player dies; `player` is nil once they have left.                     |
| [`players.on_respawn`](/ref/Players/on_respawn/) | `(player?)`                      | A player respawns; `player` is nil once they have left.                 |

Delivery is guaranteed where it matters:

- Joins, leaves, deaths and respawns are retained in order and never evicted
  by ordinary traffic or skipped because the tick budget was spent. They carry
  the original player session, so a delayed leave still has its `player.data`
  after a reconnect.
- This is in-process delivery, not a durable journal across a server crash.
  Keep lifecycle callbacks short so their retained backlog drains.

:::note
The tick budget does not cover `players.on_join` — input events and
task threads keep the 100 ms runaway limit instead. See
[Runtime](/concepts/runtime/).
:::

## Death: cause, message, by

`cause` in `players.on_death` says what killed them:

| Cause                                                                    | What it is                    |
| ------------------------------------------------------------------------ | ----------------------------- |
| `fall`, `drown`, `suffocate`, `void`, `lava`, `fire`, `cactus`, `starve` | The environment.              |
| `attack`                                                                 | A mob's or a player's hit.    |
| `shot`                                                                   | An arrow.                     |
| `blast`, `magic`                                                         | An explosion, magic.          |
| `other`                                                                  | A pack's own `player:damage`. |

`message` is the broadcast English death line. `by` is the player who hit or
shot them, or `nil`. What happens at zero health — and what does not — is on
[Health and damage](/players/health/).

## A player is one value while connected

Every event passes the same `player`:

- `a == b` compares players, and a player can be a table key.
- `player.data` holds your own state. You need no table keyed by name.

The identifying fields:

| Field         | Holds                                                                     |
| ------------- | ------------------------------------------------------------------------- |
| `player.name` | The player's name.                                                        |
| `player.uuid` | The account's own id: the one name for a player a rename does not change. |
| `player.at`   | Where they stand now.                                                     |
| `player.room` | The Room the player is in; nil while they move between rooms.             |
| `player.data` | Your own table, kept on the player for as long as they are connected.     |

## player.data

`data` is the per-session state holder: your own table on the player, gone
when the player is.

- In `players.on_leave`, `player.name` and `player.data` still read. `data` is
  kept for 10 seconds after they leave; after that a value you still hold
  reads an empty table.
- `data` may name the player (`p.data.state = { player = p }`, a function that
  uses `p`); it is let go with them all the same.
- A player who rejoins is a new value with empty `data`.

```luau
players.on_join(function(p) p.data.coins = 0 end)
players.on_leave(function(p) storage.set("coins." .. p.uuid, p.data.coins) end)
```

:::caution[Gotcha]
Nothing in `data` survives a reconnect. A rejoining player is a
new value with empty `data` — and a new session resets the session settings
too (hidden players, `visible`; see
[Visibility and teams](/players/visibility/)). Write what matters to
[storage](/systems/storage/) in `on_leave` and read it back in `on_join`.
:::

## Leaving for another server

[`player:connect(server)`](/ref/Player/connect/) asks Minefort's proxy to move
the player: a BungeeCord `Connect` for a Java player, a `Transfer` to that
name for a Bedrock player. It returns nothing and does not yield.

| `server` is        | The player goes to                                        |
| ------------------ | --------------------------------------------------------- |
| an instance's `id` | that instance (see [Network](/systems/network/))              |
| the network's name | its default member; `network.info().network` is that name |
| `hub`              | Minefort's hub                                            |

The fine print:

- The name is 1 to 128 characters of letters, digits, `.`, `_` and `-`. Any
  other name is an error, and nothing is sent.
- Minefort decides. It does not move a player to a server out of the network,
  and it does not tell the pack.
- The call does not tell the pack the result. A player who is still here some
  seconds later was not moved.
- It moves a Bedrock player, and a Java player on 1.7 or later. A Java player
  on an older version stays.
- On a local run there is no proxy. A Java player stays. A Bedrock client
  reads the name as an address, and leaves the server.

## See also

- [Health and damage](/players/health/) — death causes, respawn and the damage calls.
- [Movement and cameras](/players/movement/) — `move_to` and rooms in context.
- [Visibility and teams](/players/visibility/) — what a new session resets.
- [Storage](/systems/storage/) — persisting per-player state across sessions.
- [The event model](/concepts/events/) — connections, cancellation and budgets.
