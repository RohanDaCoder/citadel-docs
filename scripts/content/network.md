---
title: "Network"
url: /docs/citadel/network
---

# Network

An instance has a **label**. One member can run in several ways, such as `2v2` and `4v4`. The label says which. Minefort stores the label and filters on it, and does nothing else with it.
**Any server of the network can call `network`.** The pack names a member and a label. Minefort decides the network, the instance’s id and where the instance runs.
```luau
-- The default member: a place where players pick how to play.
-- This author calls an instance of "bedwars-arena" an arena.
local waiting = {} -- instance id -> the players who go there when it is online

commands.add("join <label:word>", function(player, args)
    local arena, why = network.find{
        label = args.label,   -- "2v2"
        party = player,       -- room for the player's whole party
        start = { member = "bedwars-arena", slots = 8, data = { map = "castle" } },
    }
    if not arena then return "No arena now: " .. tostring(why) end
    if arena.state == "online" then
        player:connect(arena.id)
    else
        -- It is still starting. Keep the player here until it is online.
        waiting[arena.id] = waiting[arena.id] or {}
        table.insert(waiting[arena.id], player)
    end
end)

network.on_instance(function(instance)
    if instance.state ~= "online" then return end
    for _, player in waiting[instance.id] or {} do player:connect(instance.id) end
    waiting[instance.id] = nil
end)

network.on_gone(function(id) waiting[id] = nil end)

```
```luau
-- The member "bedwars-arena": it says how much room it has.
local me = network.info()                 -- `me.id` is nil on a server that is not an instance
local map = me and me.data and me.data.map or "castle"

players.on_join(function()
    if me and me.id then network.status{ open = math.max(0, me.slots - #players.list()), status = "waiting" } end
end)
-- When the round starts: network.status{ open = 0, status = "playing" }
-- When the round ends, each player goes back to the default member:
--   player:connect(me.network)     -- the name of the network

```
The calls:
- `network.start{ member, label, slots, data? }` starts an instance of `member`. It returns `{id, state}` at once, with `state = "starting"`: the instance comes online later. `slots` is the number of players the instance takes. `data` is the pack’s own value for the instance, read there with `network.info()`.
- `network.find{ label, players?, party?, start? }` returns `{id, state}` for the instance to send `players` players to, or nil when no instance has room.
  - It picks an `online` instance with that label and that much `open`, the fullest first.
  - The room is held for 10 seconds, so two calls do not both get the last place.
  - `players` is 1 unless you set it.
  - `party` is a player, or their uuid. When they lead a `/party`, Minefort holds room for every member. Connect the leader, and the party follows them there. A player who leads no party needs room for one.
  - With `start = { member, slots, data? }`, Minefort starts an instance when none has room, and holds the room on it. The `state` is then `"starting"`.
  - Use `find` with `start`, not `find` and then `start`. The default runs on many servers, and each would start its own instance.
- `network.list(label?)` returns a list of the network’s instances. Each one is the instance table below.
- `network.stop(id)` stops an instance of this network. It returns `true` when Minefort accepted it.
- `network.info()` returns `{network}` on every server of a network. `network` is the name of the network.
  - On an instance it returns `{network, id, member, label, slots, data}`.
  - `id` is nil on a server that is not an instance.
- `network.status{ open, status?, meta? }` says where this instance is. It returns nothing and does not yield.
  - `open` is the number of players the instance takes now. `0` closes it to `find`.
  - `status` is the pack’s own word, such as `"waiting"` or `"playing"`.
  - `meta` is the pack’s own value. Other servers of the network read it.
  - Minefort takes one status a second. The first call goes at once. Of the calls in the second after it, only the last goes.
- `network.on_instance(fn)` calls `fn(instance)` when an instance starts or changes. It returns a connection.
- `network.on_gone(fn)` calls `fn(id)` when an instance is gone. It returns a connection.
An instance table:
| Field | Set by | Meaning |
| --- | --- | --- |
| `id` | Minefort | The instance’s name. `player:connect` takes it. |
| `member`, `label` | the pack that started it | Which member, and which label. |
| `state` | Minefort | `"starting"`, then `"online"`, then `"stopping"`. |
| `open` | the instance | The number of players it takes now. |
| `status` | the instance | Its own word, or nil. |
| `players` | Minefort | The number of players on it. |
| `meta` | the instance | Its own value, or nil. |
**`network` does not move players. `player:connect(id)` does.** The instance’s `id` is the server name it takes. The name of the network, `network.info().network`, sends a player back to the default member. Do not send a player to an instance that is `"starting"`: keep the player until the instance is `"online"`.
**Events come to the default member’s servers only.** Call `network.list()` once at the start, then keep the list from `on_instance` and `on_gone`. An event can be lost. Call `network.list()` again, once a minute at most, to repair the list.
**A failed call returns nil and a reason.** `start`, `find` and `info` return `nil, reason`. `list` returns `{}, reason`. `stop` returns `false, reason`. The reason is Minefort’s word, or one of these:
- `"unavailable"`: there is no network here. Every local run answers this.
- `"io"`: the request was not sent.
- `"timeout"`: no answer came in 35 seconds. A `start` may have happened.
`find` returns `nil` with no reason when no instance has room.
Limits. A value out of these is an error, and nothing is sent:
- `label`: 1 to 32 characters of `a-z`, `0-9` and `-`.
- `member`: 1 to 40 characters of `a-z`, `0-9` and `-`.
- `slots`: 1 to 200. `players`: 1 to 64. `open`: 0 to 200.
- `data`: at most 4096 bytes as JSON. `meta`: at most 512 bytes as JSON.
- `status`: at most 32 characters.
- An unknown field in a table is an error.
- A network has at most 20 instances in a region, and one `start` a second.
- Minefort removes an instance with no players for 60 seconds after its first player, or for 5 minutes without one.
Calls yield, like `stores`, but for `status` and the two events. Call from scripts, callbacks or tasks.
