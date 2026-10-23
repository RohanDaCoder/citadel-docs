# SOURCE: Cancelling events

```luau
players.on_break(function(player, pos, block) return false end) -> connection
players.on_place(function(player, pos, block) return false end) -> connection
--   player is the handle, pos is the block, block is its canonical name:
--   what is about to be broken, or what is about to be put down
players.on_damage(function(player, hit) return false end) -> connection
--   asked before damage lands on a player; false refuses all of it
--   hit.amount   the damage, in half hearts, before armour
--   hit.cause    "fall", "drown", "suffocate", "void", "lava", "fire", "cactus",
--                "starve", "attack", "shot", "blast" or "magic"
--   hit.by       the player who hit, or who shot the arrow; nil for anything else
--   hit.kind     the kind's name ("Skeleton") when a mob did it; else nil
```
```luau
-- No friendly fire, and nobody is hurt at the spawn.
players.on_damage(function(player, hit)
    if hit.by and hit.by.data.team == player.data.team then return false end
    if player.at:distance(SPAWN) < 8 then return false end
end)
```
- A refused arrow bounces off, as off a creative player.
- A pack’s own `player:damage` is not asked about, in this pack or another.
- An entity of a pack’s own has the same question as a hook: `on_damage`
in `game.entities.define`, which answers `"take"` or `"ignore"`.
```luau
-- A spawn area nobody digs in.
players.on_break(function(player, pos, block)
    if math.abs(pos.x) < 16 and math.abs(pos.z) < 16 then
        player:message("not here", colors.red)
        return false
    end
end)
```
- Only `false` is a veto.
- A handler that returns **nothing** allows the action.
- A handler that *errors* is not a veto. It counts as a missed deadline.
Also:
- **The observe-only events come after.** A vetoed break never reaches
`world.on_block_break` or `world.on_block_place`.
- **Across packs, any `false` wins.** One `false` cancels the action.
- **These handlers can delay the tick.** The engine waits **two milliseconds**
for your pack, then stops waiting. `task.wait` and anything that blocks are
errors here.
## What a missed deadline means
Each hook the engine waits on states what a missed deadline does:
| hook | a missed deadline means | why |
| --- | --- | --- |
| `players.on_break` | **the break is denied** | Protection fails closed on timeout, error, overflow, or a disabled handler. |
| `players.on_place` | **the place is denied** | The same protection guarantee applies. |
| `players.on_damage` | **the damage is denied** | The same protection guarantee applies. |
The rule: **fail open only where the default is safe**. A pack block’s own
`on_break` (it comes with pack blocks) fails *closed* to the drops its
definition declares.
The engine counts misses at `citadel.budget().asks.kinds["break"].missed`.
After enough misses, it stops asking your pack for that kind and logs this
once. See “Limits and reload”.
