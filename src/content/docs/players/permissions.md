---
title: 'Permissions'
description: 'Permission nodes — wildcards, a leading minus, most-specific-wins — groups in the pack''s citadel.yml with inheritance, putting players in groups from script until they leave, operators with every node, and gating commands with player:has.'
---

:::note[In short]
a permission node is a dotted name. `casino.*` covers
everything under `casino`, `*` covers everything, and a leading `-` takes a
node away; the most specific node wins. Groups are defined in the pack's
`citadel.yml` under `permissions:` — every player is in `default` — and the
script puts players in groups with `player:add_group`, which lasts until
they leave. Gate your own commands with `player:has`.
:::

## Node syntax

| Node            | What it covers             |
| --------------- | -------------------------- |
| `casino.play`   | Exactly this node.         |
| `casino.*`      | Everything under `casino`. |
| `*`             | Everything.                |
| `-casino.debug` | Takes the node away.       |

The resolution rules:

- A leading `-` takes a node away.
- The most specific node wins. Between two equally specific nodes, the `-`
  wins.

So `"casino.*"` plus `"-casino.debug"` in one group's nodes grants the whole
`casino` tree except `casino.debug`.

## Groups in citadel.yml

The pack's `citadel.yml` defines groups. Every player is in `default`, and a
group may inherit the nodes of others with `inherits`:

```yaml
permissions:
  default: { nodes: [casino.play] }
  vip: { inherits: [default], nodes: [casino.vip] }
  staff:
    {
      inherits: [vip],
      nodes: [minecraft.command.gamemode, "casino.*", "-casino.debug"],
    }
```

| Key        | Meaning                                    |
| ---------- | ------------------------------------------ |
| `nodes`    | The group's permission nodes.              |
| `inherits` | The other groups this group inherits from. |

The `staff` group shows all three node forms at once: an exact node, a
wildcard, and a negation — and it inherits `vip`, which inherits `default`.

## Putting players in groups

| Call                                                     | Returns      | Purpose                                       |
| -------------------------------------------------------- | ------------ | --------------------------------------------- |
| [`player:add_group(group)`](/ref/Player/add_group/)       | —            | Puts the player in a group until they leave.  |
| [`player:remove_group(group)`](/ref/Player/remove_group/) | —            | Takes the player out of a group.              |
| [`player:groups()`](/ref/Player/groups/)                  | `{ string }` | The player's groups; `default` is not listed. |

- Groups last until the player leaves. Store them and re-add them in
  `players.on_join` — see [Player lifecycle](/players/player-lifecycle/).
- `add_group` errors on a group citadel.yml does not define.

## Operators

Server operators — the `operators:` list in the **server's** `citadel.yml`,
by uuid — have every node. Minefort writes the server owner there.

## Checking permissions

Gate your own commands with [`player:has(node)`](/ref/Player/has/): true if
the player's groups give them the node (and always true for an operator).

```luau
if player:has("casino.vip") then
    -- the node the vip group grants
end
```

Commands take a `permission` option directly — without the node, a player
does not see or run the command (see [Commands](/systems/commands/)). One name,
several shapes: calls with one name, such as `"tekkit"` and
`"tekkit give <item:word>"`, make one command, and each shape has its own
permission. The engine's `/help` lists every command a player may run.

## Merging and errors

- Same-name groups in two packs merge.
- The server stops on a group that inherits an undefined group, or on a group
  named `operator`.

:::caution[Gotcha]
A group named `operator` — or an `inherits` pointing at a group
that is not defined — stops the server at load. Name groups anything else.
:::

## See also

- [Commands](/systems/commands/) — the `permission` option of `commands.add`.
- [Server settings](/systems/server-settings/) — the server's `citadel.yml` and the `operators` list.
- [Pack anatomy](/concepts/pack-anatomy/) — the pack's `citadel.yml` manifest.
- [Player lifecycle](/players/player-lifecycle/) — re-adding groups in `on_join`.
