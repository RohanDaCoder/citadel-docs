# SOURCE: Permissions

- `casino.*` covers everything under `casino`. `*` covers everything.
- A leading `-` takes a node away.
- The most specific node wins. Between two equally specific nodes, the `-`
wins.
The pack’s `citadel.yml` defines groups. Every player is in `default`.
```yaml
permissions:
  default: { nodes: [casino.play] }
  vip:     { inherits: [default], nodes: [casino.vip] }
  staff:   { inherits: [vip], nodes: [minecraft.command.gamemode, "casino.*", "-casino.debug"] }
```
The script puts players in groups:
```yaml
player:add_group("vip")    # errors on a group citadel.yml does not define
player:remove_group("vip")
player:groups()    # { "vip" }; `default` is not listed
player:has("casino.vip")    # true
```
- Groups last until the player leaves. Store them and re-add them in
`players.on_join`.
- Server operators (`operators:` in the server’s `citadel.yml`) have every
node.
- Gate your own commands with `player:has`.
- Same-name groups in two packs merge.
- The server stops on a group that inherits an undefined group, or on a
group named `operator`.
