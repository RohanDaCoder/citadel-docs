# SOURCE: Game data

```luau
game.version    -- "a0.1.0"
game.world_height    -- 128; a 1.8.9 world is 256
game.sea_level
game.entities.names { mob = true }    -- {"pig", "sheep", "cow", ...}
```
## Blocks
`game.block(name)` returns one block in **this version’s** numbers, or `nil`
if this game lacks it. `behaviour` is the rule Citadel runs for the block
(`"grass"`, `"flowing"`, `"torch"`, `"falling"`), or `nil` for an inert
block.
```luau
local stone = game.block("stone")
print(stone.hardness)    -- 1.5 in a0.1.0
print(stone.behaviour)    -- nil: stone just sits there
print(game.block("grass_block").behaviour)    -- "grass"
print(game.block("water").random_ticks)    -- does the random tick land on it
print(game.block("torch").light)    -- 14; what it gives off, 0..15
print(game.block("glass").light_filter)    -- 0; what a step through it takes away
print(game.block("obsidian").resistance)    -- what an explosion ray loses to it
print(game.block("oak_planks").flammability)    -- { catches = 5, burns_away = 20 }
print(game.block("water").material.liquid)    -- the jar's Material, as its five questions: solid, covers (grass under it dies), firm (snow and ice need it), liquid, burns
```
`resistance`, `flammability` and `material` are `nil`, not zero, in a game
with no block-update tables.
Everything above is read-only.
### drops — true , false and nil
`drops` is the field of a game block that a pack writes. It says whether a
block of this kind leaves its item when the world breaks it by itself: a
torch whose wall is gone, a leaf that decays, a block an explosion or a
piston breaks, sand that cannot land.
On a `mode: lite` world, the world leaves no such item. The pack switches a
block on:
```luau
game.block("torch").drops = true    -- a torch that falls off leaves a torch
game.block("wall_torch").drops = true    -- a torch on a wall is another block
print(game.block("torch").drops)    -- true
game.block("torch").drops = nil    -- the pack says nothing: the world's default
```
| Value | Meaning |
| --- | --- |
| `true` | The world leaves the block’s normal drops, on a lite world too. |
| `false` | The world leaves nothing for this block, with `survival` on too. |
| `nil` | The pack sets nothing. The world’s default applies. |
- The world’s default is off on a `mode: lite` world and in a room made by
`rooms.create`. It is on on a `mode: full` world and after
`world.rules{ survival = true }`.
- The value is for every state of the block, and for this block name only.
`oak_planks` and `spruce_planks` are two blocks.
- It reads what this pack set, not another pack’s value. Where two packs
disagree, `false` wins.
- It is not a player’s dig. Without `survival`, a dig reaches no block.
- Use it for the game’s blocks. A block from `game.blocks.define` leaves the
drops its definition lists.
- A reload removes a value that the script does not set again.
- `true` is an error in a game version with no items on the ground.
## Items
`game.item(name)` does the same for items: the item’s table, or `nil`. It
never raises an error.
```luau
if game.item("bucket") then player:give("bucket") end
print(game.item("stone").stack_size)    -- 64
```
## Entity kinds
A kind is a `mob` when the game gives it health and a mind of its own: a cow,
a zombie. An arrow, an item and a boat are not mobs. A player is not an
entity here: players are in `players`, never in `world.entities`. `game.entities.<kind>`
has the facts of one kind of the game. `game.entities.cow` and `game.entities.Cow` are the same
kind. A kind that this game does not have is `nil`:
`if game.entities.creeper then`.
```luau
local cow = game.entities.cow
print(cow.max_health, cow.width, cow.height, cow.speed)   -- cow.health is an error: a kind has a maximum
print(cow.drop)                      -- "leather"
print(cow.hostile)                   -- false
print(cow.registry_name)             -- "Cow", this version's own spelling
print(cow.mob)                    -- true: a cow is a mob

for name, kind in game.entities do   -- every mob kind this version has, in its own order
    if kind.hostile then print(name) end
end

local arrow = game.entities.arrow    -- a kind that is not a mob has a row too
print(arrow.mob)                  -- false
print(arrow.width, arrow.height, arrow.physics)

game.entities.names()                    -- every kind: the pack's own and the game's, mob or not
game.entities.names { mob = true }    -- the mob kinds only
game.entities.names { mob = false }   -- the kinds that are not mobs
```
- Use `for name, kind in game.entities do`, not `pairs(game.entities)`.
- A game kind that is not a mob (an arrow, a boat, primed TNT) has the facts
`name`, `mob` (`false`), `width`, `height` and `physics` (`"item"`,
`"falling"`, `"vehicle"` or `"none"`). Every other fact is `nil`. A write to
`spawn`, `attacks` or `interact` is an error, and so is `:amend`: they are
for mob kinds.
- Iteration and `game.entities.names()` cover all kinds, once each. Use
`game.entities.names { mob = true }` or check `kind.mob` for mob settings.
- A pack kind (`rave:rocket`) reads as a definition handle, with `name` and
`mob = false`. Pass it to `world.spawn` just like the handle from `define`.
- `define`, `amend` and `names` are functions on the same table (see “Custom
entities”). `game.entities.cow:amend { ... }` is the same as
`game.entities.amend("cow", { ... })`.
Everything above is read-only.
## Spawn rules — true , false and nil
`spawn` is the field of a mob kind that a pack writes. It says whether the
kind is in this world by itself.
On a `mode: lite` world, no mob spawns by itself. The pack switches
a kind on:
```luau
game.entities.cow.spawn = true    -- cows are in this world, as the game has them
```
Cows now spawn by the game’s own rule. No other kind spawns. A player’s right
click on a cow with a bucket gives milk.
```luau
game.entities.cow.spawn = false    -- cows never spawn by themselves in this world
print(game.entities.cow.spawn)    -- false
game.entities.cow.spawn = nil    -- the pack says nothing: the world's default
print(game.entities.cow.spawn)    -- nil
```
| Value | Meaning |
| --- | --- |
| `true` | The kind is in this world as the game defines it. It spawns by the game’s own rule, and it is the game’s entity in full. |
| `false` | The kind never spawns by itself. |
| `nil` | The pack sets nothing. The world’s default applies. |
- The world’s default is off on a `mode: lite` world and in a room made by
`rooms.create`: no mob spawns by itself. The default is on on a `mode: full`
world and after `world.rules{ survival = true }`: each kind spawns by the
game’s own rule. `world.rules{ survival = false }` sets the default to off
again.
- `true` makes the kind the game’s entity in full, on a lite world too. It
spawns by the game’s own rule. Its hits hurt players and a player’s right
click on it has the game’s effect. See “`attacks` and `interact`” below.
- A monster that comes to a sleeping player obeys the same value.
- `true` does not make a kind spawn where the game cannot spawn it. On 1.8.9
the game takes the kinds it spawns from the biome. A world with no biomes (a world the
scripts make) spawns nothing, and `true` is an error there.
- `false` stops natural spawning only. A spawner block, `world.spawn`,
`/summon` and breeding still make the entity.
- Mobs already in the world stay.
- Reading gives what this pack set: `true`, `false` or `nil`. It does not
give the game’s own rule or the value of a different pack.
- Each pack has its own value. If one pack sets `false`, the kind does not
spawn. If no pack sets `false` and one pack sets `true`, the kind is on.
- The value is for one room. `game` is the main room’s table. A room from
`rooms.create` has its own: `room.game.entities.cow.spawn = true`.
- On a script reload, the values of the last run stay until the new script
has loaded. Then each value that the new script did not set is removed.
- On a game with no natural spawning, every write is an error, `nil` included.
a0.1.0 to a0.1.3 are such games.
- An error is a plain string for `pcall`.
## attacks and interact
`attacks` and `interact` are two more fields of a mob kind that a pack writes. Each is `true`,
`false` or `nil`. A different value is an error.
```luau
game.entities.zombie.attacks = false    -- a zombie's hit does not hurt a player
game.entities.cow.interact = false    -- a right click on a cow does nothing
game.entities.zombie.attacks = nil    -- the pack says nothing
```
| Field | `true` | `false` |
| --- | --- | --- |
| `attacks` | The entity’s hits hurt players. | The entity’s hits do not hurt players. |
| `interact` | A player’s right click on the entity has the game’s effect (milk from a cow, a saddle on a pig). | The right click has no effect. |
With `nil`, the engine uses the first line that applies:
1. The kind has `spawn = true`: the field is on.
2. The room’s rule: `damage` for `attacks`, `survival` for `interact`.
- **The kind’s own setting is stronger than the room’s rule.** Thus
`game.entities.zombie.spawn = true` makes a zombie’s hit hurt in a room with
`world.rules{ damage = false }`. To keep the zombie harmless there, set
`game.entities.zombie.attacks = false`.
- A zombie from `world.spawn` on a lite world does not hurt players until
the pack sets `spawn = true` or `attacks = true` for zombies, or the room
has the `damage` rule.
- `interact` changes the item in the player’s hand as the game does: an empty
bucket becomes a bucket of milk.
- `interact` is not available on 1.8.9: that game version has no right click on a
mob in Citadel. `interact = true` is an error there, and `spawn = true` does not
give the right click.
- `attacks` covers the entity’s own hit, its arrow and its blast. An arrow
keeps the kind of its shooter, so the arrow of a dead skeleton follows
`game.entities.skeleton.attacks`. The blast of a creeper follows
`game.entities.creeper.attacks`.
- `attacks = false` stops the damage to players only. The blast of a creeper
still breaks blocks, as the game says, and still hurts other entities.
- A blast of TNT, of a bed and of `world.explode` has no kind. It follows the
room’s `damage` rule.
- The fields are for one room and one pack, as `spawn` is. If one pack sets
`false`, the field is off.
To put mobs in a world, use `world.spawn(name, pos)` (see “Mobs and
drops”), `/summon`, or a dungeon spawner the terrain placed.
> **a0.1.0 spawns nothing on its own.** Only its dungeon spawner makes mobs.
**a0.1.0 spawns nothing on its own.** Only its dungeon spawner makes mobs.
## Terrain
`game.terrain` describes this world’s overworld: `snow`, and `steps` in the
shape `citadel.yml` uses. It is read-only, and `nil` where the engine has no
list.
```luau
for i, step in ipairs(game.terrain.steps) do
  print(i, step.step, step.block, step.count)   -- 1 dungeons nil 8
end
print(game.terrain.snow)                        -- false
```
