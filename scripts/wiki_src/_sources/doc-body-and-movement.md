# SOURCE: Body and movement

- `player:connect(server)` asks Minefort’s proxy to move the player: a BungeeCord `Connect` for a Java player, a `Transfer` to that name for a Bedrock player. It returns nothing and does not yield.
  - `server` is a server name: the `id` of an instance (see Network), the name of the network, or `hub`.
  - The name of the network sends the player to its default member. `network.info().network` is that name. `hub` is Minefort’s hub.
  - The name is 1 to 128 characters of letters, digits, `.`, `_` and `-`. Any other name is an error, and nothing is sent.
  - Minefort decides. It does not move a player to a server out of the network, and it does not tell the pack.
  - The call does not tell the pack the result. A player who is still here some seconds later was not moved.
  - It moves a Bedrock player, and a Java player on 1.7 or later. A Java player on an older version stays.
  - On a local run there is no proxy. A Java player stays. A Bedrock client reads the name as an address, and leaves the server.
- On a pack server, only `damage` and `health` hurt a player. Creative and
  spectator players take no damage.
- At zero health the player dies. `players.on_death` fires with cause
  `"other"`, and the client shows the respawn screen.
- On a pack server a death drops and clears nothing. The hotbar is a menu,
  not an inventory.
