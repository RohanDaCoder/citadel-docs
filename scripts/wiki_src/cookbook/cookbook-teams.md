---
title: Teams
section: cookbook
order: 5
description: Set up teams with player.data, make members visible only to their own team, and keep the assignments alive across joins and reloads.
tags: [teams, visibility, player.data, pattern]
---

# Teams

> **In short:** a team is a field on the player — `player.data.team` — plus
> two rules: apply visibility when the team is set, and re-apply it when
> anyone joins. The visibility calls are `viewer:hide(player)` and
> `viewer:show(player)`.

## Assigning teams

```luau
local TEAMS = { "red", "blue" }

commands.add("team <name:red|blue>", function(player, args)
    player.data.team = args.name
    player:message(`You are on team {args.name}.`, args.name)
end, { help = "Pick a team" })
```

`player.data` is a table that lives as long as the player is connected, and
players compare by identity (`a == b`), so it is the natural home for team
membership during a match. The enum argument type (`red|blue`) makes the
command validate itself — the parser only accepts the listed words.

## Applying team visibility

The docs' own teams pattern — each side sees only its own:

```luau
local function apply_teams()
    for _, a in players.list() do
        for _, b in players.list() do
            if a.data.team ~= b.data.team then a:hide(b) else a:show(b) end
        end
    end
end
```

The rules that shape it:

- `viewer:hide(player)` removes the player **from this viewer only**;
  `viewer:show(player)` undoes it. `viewer:can_see(player)` reads what the
  two settings add up to.
- A hidden player is gone from that client: no body, name, armour or hitbox.
  The `invisibility` effect differs — it shows armour and the held item.
- The tab list still shows hidden players.
- `hide` is **by account**, so it lasts when the other player rejoins.
- A new session resets both: nothing hidden, and `visible` is true.

## Keeping teams alive

Re-apply when someone joins — and remember the global `players.on_join` fires
in the main room, a room's own fires on each move in:

```luau
players.on_join(function(player)
    if not player.data.team then
        player.data.team = TEAMS[math.random(#TEAMS)]     -- or a balancing pick
    end
    apply_teams()
end)
```

> **Gotcha:** `player.data` resets when the player reconnects, and a script
> reload runs `players.on_join` again for every online player. Make
> `apply_teams` safe to run twice — it is, because `hide`/`show` are
> idempotent writes. For teams that outlive the session, store the team in
> [storage](/wiki/storage) keyed by `player.uuid` and restore it in
> `on_join`.

## Team scoring

Scoreboards and bars follow the same shape — the Coin rush sidebar, split by
team:

```luau
local function show_scores()
    local sum = {}
    for _, p in players.list() do
        local t = p.data.team or "?"
        sum[t] = (sum[t] or 0) + p.data.coins
    end
    local lines = {}
    for _, t in TEAMS do
        table.insert(lines, `{t}:  {sum[t] or 0}`)
    end
    ui.sidebar{ title = "TEAM SCORES", lines = lines }
end
```

## Friendly fire

The cancellable damage ask is where teams meet combat — return `false` to
veto a hit between team-mates:

```luau
players.on_damage(function(player, hit)
    if hit.by and hit.by.data.team == player.data.team then return false end
end)
```

`hit.by` is the player who hit, or who shot the arrow; `nil` for anything
else. Answer at once — the engine waits two milliseconds (see
[The event model](/wiki/events)).

## See also

- [Visibility](/wiki/visibility) — the full hide/show/visible rules.
- [The event model](/wiki/events) — the damage ask and its deadline.
- [Leaderboards](/wiki/cookbook-leaderboards) — the sidebar patterns.
- [Permissions](/wiki/permissions) — when teams should be groups instead.
