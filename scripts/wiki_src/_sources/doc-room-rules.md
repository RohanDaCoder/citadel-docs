# SOURCE: Room rules

A `mode: full` server has them all on. A pack can turn one off.
A rule is `true` or `false`. A rule that you leave out keeps its value, and
so does a rule you write as `nil`. Any other value is an error:
`world.rules{ fall = 0 }` and `world.rules{ fall = "off" }` stop the script.
`redstone` is on in every room until a pack turns it off. With it off, no
signal moves: a lever lights no wire, a piston stays in, a pack block’s
`power` gives nothing and `block.powered` reads `false`. What was lit when
the rule changed stays as it is until something beside it changes.
`anticheat` checks what each Java player’s client claims:

- A player who flies, runs too fast, sends moves faster than the game ticks, or walks through full blocks goes back to the last legal position.
- A claim to stand on nothing does not prevent fall damage.
- A hit on something the player does not look at, or faster than 20 per second, does not land.
- After enough failed checks in a short time, the engine removes the player. The message names the check.
- The flight check skips creative and spectator players, a player who may fly (`player.can_fly`), a rider and a dead player.
- `player:push` and a movement effect (`speed`, `jump_boost`, `levitation`, `slow_falling`, `dolphins_grace`) exempt the player while they last. `player:teleport` is always allowed.
- A pack that moves players in any other way turns `anticheat` off: `world.rules{ anticheat = false }`.
  `survival` gives the room to the engine’s survival, as on a `mode: full`
  server:
- A broken block drops its normal drops.
- A block the world breaks by itself drops them too: a torch whose wall is
  gone, a leaf that decays, a block an explosion or a piston breaks, sand
  that cannot land.
- Placing uses up the stack.
- The inventory and a crafting table craft.
- A death drops the inventory, and the respawn button works.
- The engine saves the player’s inventory.
- It also turns on `fall`, `damage`, `hunger`, `anticheat` and `day_cycle`.
  Without `survival`, a dig reaches no block, and a block the world breaks by
  itself leaves no item. `game.block(name).drops = true` switches one block of
  the game back on (see “Blocks”). A pack block still leaves the drops its
  definition lists; `drops = "table"` is the game’s own drop and leaves
  nothing. A survival pack puts `world.rules{ survival = true }` at the top,
  and runs the same on either kind of server.
  Anything that is not a rule is the pack’s job: `player:damage` for a hit,
  `player.health` to heal, `players.on_death` and `players.on_respawn` for what
  happens next, and `hit.player` in `players.on_click` for one player hitting
  another:

```luau
world.rules{ fall = true }
players.on_click(function(player, hit)
    if hit.button == "left" and hit.player then
        hit.player:damage(2)
        hit.player:push(player:look() * 0.5 + vec3(0, 0.3, 0))
    end
end)
```
