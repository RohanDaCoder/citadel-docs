# SOURCE: Custom blocks

```luau
local crate = game.blocks.define {
    name = "crate",
    looks = "tnt",
    on_use = function(block, player)
        block:become("primed_tnt", { fuse = 20 })
        return "used"
    end,
}

world.set_block(vec3(10, 65, 10), crate)   -- the handle, or "rave:crate"
```

It is a real block: saved under its own name, broken, used and ticked like
any other. Every client that has never heard of your pack draws it as TNT.
Three rules apply:

- **The engine adds the namespace.** `"crate"` becomes `"rave:crate"`, after
  your pack. A colon in the name is an error. The handle `define` returns
  works wherever a block name works.
- **`looks` is all a client sees.** Pick an inert block state that reads
  right. A name this version lacks is an error, not air. `|` takes the first name that
  exists: `looks = "crimson_planks|nether_brick"`.
- **Hooks record changes; the engine applies them.** `block:become` takes
  effect when your hook returns.

## The definition

```luau
game.blocks.define {
    name = "crate",              -- no namespace: yours is added
    looks = "tnt",               -- or { "wheat[age=0]", "wheat[age=7]" }, one per state
    hardness = 0.5,              -- seconds-scale; below zero is unbreakable
    resistance = 6,              -- what an explosion has to chew through
    material = { solid = true, covers = false, firm = true, liquid = false, burns = false },
    opacity = 15,                -- what a step through it takes off the light
    light = 0,                   -- what it gives off, 0..15
    tick_every = 0.5,            -- seconds between block:schedule() and on_tick
    drops = { { item = "stick", count = 2 } },   -- or "table"; "none" or false for nothing; a row may be a pack item
    item = { item = "furnace", name = "Crate" },  -- the block in a hand; see "the block as an item"; false for no item
    texture = "textures/crate.png",  -- its own picture on 1.21.4+; see "blocks with their own pictures"
    model = models.crate,        -- or its own shape, in place of texture; see "blocks drawn from a model"
    facing = true,               -- turns its front to whoever places it
    power = 0,                   -- what it gives a redstone circuit, 0 or 15; see "power"
    label = "Crate",             -- the name of the item a textured block comes with
    extends = "tnt",             -- a name, a handle, a plain table, or a list
    on_use = function(block, player, held, base) end,
}
```

- Every field except `name` and `looks` has a default.
- Call `define` only **while your pack loads**.
- Define blocks at the top of `main.luau`. A reload runs `define` again and
  keeps the world.

## Blocks with their own pictures

`texture` gives a block its own picture on 1.21.4 and later. `facing = true`
turns its front to whoever places it, like a furnace:

```luau
local side = game.texture(16, 16)
side:noise(0, 0, 16, 16, { "#8a8a8a", "#7d7d7d", "#969696" }, 3)
side:frame(0, 0, 16, 16, "#5a5a5a")
local front = side:copy()
front:rect(4, 4, 8, 8, "#303030")

local macerator = game.blocks.define {
    name = "macerator",
    looks = "dispenser",                  -- what an older client sees; left out, stone
    texture = { side = side, top = side, bottom = side, front = front },
    facing = true,
    label = "Macerator",                  -- the item's name
}
player:give(macerator.item)
```

- `texture` is one picture for all six faces, or a table of `all`, `side`,
  `top`, `bottom`, `front`, `back`, or a face by name (`north`, `up`, …).
  `front` is the side a facing block faces; `back` is opposite. A missing
  face uses `side`, and `side` uses `all`.
- Several states take a list, one per state:
  `texture = { idle, working }` with `looks = { "furnace", "furnace[lit=true]" }`.
- `facing = true` gives every state four facings. `block.state` counts only
  your states. `block.facing` reads and turns the facing (`"north"`,
  `"south"`, `"west"`, `"east"`). The `looks` block turns too if it can.
- A textured block comes with its item. `label` names it. `item` sets
  another item underneath. `item = false` gives the block no item.
- The picture is a full, opaque cube: see-through pixels draw solid. A
  server has room for about a thousand textured blocks.
- A client from 1.21.4 draws a textured cube on a note block state, so it
  hears a note block (wood) when the block is hit or broken. An older client
  hears the `looks` block.
- A block a pack places is never drawn as a textured block. A pale moss
  carpet with moss up its sides can show as a bare one.
- The block collides as its `looks` block does. One that looks like a rail
  or a carpet is drawn on a state a client walks through or over; a server
  has room for about a hundred of each. See “blocks drawn from a model”.

## Blocks drawn from a model

`model` draws a block from a model on 1.21.4 and later, in place of
`texture`. This is a conveyor belt whose top runs by itself:

```luau
local belt = models.new("belt", function(m)
    local frame = m:material("frame", colors.gray, { grain = 0.2 })
    local strip = m:texture(16, 16, { scroll = "up", speed = 2 })   -- two texels a tick, on the client
    strip:fill(colors.black)
    strip:rect(0, 0, 16, 2, colors.gray)
    m:part("body"):box(vec3(-8, 0, -8), vec3(8, 16, 8), frame, { faces = { up = strip } })
end)

local DIR = { north = vec3(0, 0, -1), south = vec3(0, 0, 1), west = vec3(-1, 0, 0), east = vec3(1, 0, 0) }

game.blocks.define {
    name = "belt",
    looks = "stone",                      -- what an older client sees; left out, stone
    model = belt,
    facing = true,
    label = "Conveyor Belt",
    on_step = function(block, body)       -- carry what lies on it toward the block's front
        if body.kind ~= "item" then return end
        local at, dir = block.at, DIR[block.facing]
        for _, it in world.entities { near = vec3(at.x + 0.5, at.y + 1, at.z + 0.5), radius = 1.5 } do
            if it.id == body.id then it:push(vec3(dir.x * 0.05, 0, dir.z * 0.05)) end
        end
    end,
}
```

- The model stays inside its block: `-8 .. 8` across and `0 .. 16` up. A box
  outside that is an error. A bigger shape is a display.
- **A block collides as its `looks` block does**, for the server and for
  every client. `looks` picks what the model is drawn on:
  - A full cube (`"stone"`, the default): players stand on it, and the
    client does not draw the sides of its neighbours that touch it. Where
    the model leaves the side of the cube open, you see through the
    neighbour. Fill the block’s sides.
  - A block you walk through (`"rail"`, `"stone_pressure_plate"`): the model
    can be any low shape, and nothing around it is hidden. A stack dropped on
    it lies on the block below, and `on_step` still hears it. A client from
    1.21.4 breaks it at a touch, whatever its `hardness`; a `hardness` below
    zero still cannot be broken.
  - A carpet (`"white_carpet"`): a sixteenth of a block high.
  - Any other shape (a slab, a fence) is drawn on a full cube.
- A low belt is the same definition with `looks = "rail"` and a model two
  units high. It needs a floor under it. Give it `opacity = 0`, or the block
  is dark inside.
- A block draws the model in its rest pose. It plays no animation and takes
  no `paint`. A see-through material draws solid.
- A texture with `scroll` moves by itself on the client, with nothing sent:
  `"up"`, `"down"`, `"left"` or `"right"`, at `speed` texels a tick. A speed
  is a whole number, or `0.5`, `0.25`, `0.2` for one texel every few ticks.
  On a top face, `"up"` runs toward the model’s front (`-z`), which is where
  `block.facing` points. A display draws a scrolling texture still.
- `model` is one model for every state, or a list with one per state, like
  `texture`. `texture` and `model` together are an error.
- Like a textured block, it comes with its item, and it uses one spare state
  per state and facing.

## The block as an item

`item` is the block in a hand, with the block’s name as its `id`. Placing
it puts **this** block down. Breaking the block leaves it, unless `drops`
says otherwise:

```luau
local macerator = game.blocks.define {
    name = "macerator", looks = "furnace",
    item = { item = "furnace", name = "Macerator", lore = { "grinds ore into dust" } },
}
player:give(macerator.item)       -- a Macerator; place it and it is one
game.recipes.shaped{ pattern = { "FFF", "F F", "FFF" }, keys = { F = "flint" }, result = macerator.item }
```

Placing it fires `players.on_place`, then the block’s `on_place` with the
placer and an empty `block.data`.

## The block handle

Every hook gets the block it is about. Fields read; methods act:
For crop stages, give one `looks` per stage and write `block.state = 3`. The
value must be in that list. A state change keeps the block: `block.data`
stays, and `on_removed` and `on_added` are not called.

## block.data

`block.data` holds what a block remembers besides its state, such as a
chest’s contents. It is a [data view](#data-views): nested edits and whole-record
assignments are tracked, just like a pack-defined entity’s `data`. Read and write its fields:

```luau
on_use = function(block, player)
    block.data.clicks = (block.data.clicks or 0) + 1
    player:message(`clicked {block.data.clicks} times`)
    return "used"
end,
```

- `block.data` belongs to the **position**. It saves with the chunk, through
  reloads and restarts.
- Each write is checked at the assignment by the `storage.set` rules. A
  bad value is an error that names the key.
- When the block goes, its data goes.
- Pack-wide facts, such as a leaderboard, go in `storage`.

## Data views

`block.data` and a pack-defined entity’s `data` are attached records. Nested
records and lists are attached too: `e.data.stats.wins += 1` writes back without
assigning the whole record again. This works on handles from `world.spawn` and
`world.entities`, as well as handles passed to hooks.

```luau
e.data = { stats = { wins = 0 }, history = {} }
local stats = e.data.stats
stats.wins += 1
data.insert(e.data.history, { score = 12 })
e.data.history[1].score += 3
local last = data.remove(e.data.history) -- removes and returns a detached value
local snapshot = data.copy(e.data)      -- an ordinary, detached Lua table
snapshot.stats.wins = 99               -- does not change the entity
```

- Roots are records with string keys. Values can be finite numbers, strings,
  booleans, records, or contiguous lists starting at index 1. Functions, handles,
  cycles, sparse lists, and tables mixing list indices and record keys raise an
  error before any part of that assignment changes the record.
- Set a record field to `nil` to delete it. Write `list[#list + 1] = value` to
  append, or use `data.insert(list, value)` / `data.insert(list, index, value)`.
  `data.remove(list, index?)` shifts following elements; its default is the last
  element. Assigning `nil` only removes the last list element. An empty nested
  `{}` becomes a list on the first insertion; the root always stays a record.
- `#view` counts entries. Use `for key, value in view do` to iterate. Data views
  are userdata, so use `data.copy(view)` before ordinary `table.*`, `pairs`, or
  `ipairs` operations. `storage.set(key, view)` accepts views directly.
- A nested alias follows its path in the current record. Replacing that path
  with another record or list updates what the alias sees. Deleting it or
  replacing it with a scalar makes the alias raise an error.
- Entity `on_steer`/`on_tick` and block hooks edit a draft applied when the engine
  accepts the hook’s answer. Their views expire when the callback batch finishes,
  including on error. Use `data.copy` inside the hook to keep a snapshot, or
  obtain a current entity handle to edit later. Live entity views remain valid
  while the entity exists. An unchanged draft does not overwrite entity data.
- `player.data` remains an ordinary Lua table for the player’s session. It can
  hold Lua objects such as HUD handles; it is not saved automatically. Persistent
  entity data saves only with `persist = "save"`; block data saves with its chunk.
  Migration: direct and nested assignments now write through on every supported
  handle. Replace table operations on persistent data with the `data` helpers or
  operate on `data.copy(...)` and assign the result back. Mutating the Lua table
  originally assigned to a record does not mutate the stored record.

## The hooks

Every hook gets the block first and `base` last:

| hook             | called when                                      | arguments                      | answers                              |
| ---------------- | ------------------------------------------------ | ------------------------------ | ------------------------------------ |
| `on_use`         | somebody right-clicked it                        | `block, player, held, base`    | `"used"` or `"pass"`                 |
| `on_break`       | something broke it                               | `block, player, by, base`      | `"none"`, `"table"`, or a drops list |
| `on_step`        | a body is standing on it                         | `block, body, base`            | nothing                              |
| `on_tick`        | a scheduled tick came due                        | `block, base`                  | nothing                              |
| `on_random_tick` | the random pass landed on it                     | `block, base`                  | nothing                              |
| `on_place`       | a player put it down                             | `block, player, base`          | nothing                              |
| `on_neighbour`   | a neighbour changed                              | `block, from, announced, base` | nothing                              |
| `on_trigger`     | lit, blasted or burnt                            | `block, cause, base`           | nothing                              |
| `on_power`       | a redstone signal started or stopped reaching it | `block, powered, base`         | nothing                              |
| `on_added`       | it has just been stored, whatever stored it      | `block, base`                  | nothing                              |
| `on_removed`     | it has just gone                                 | `block, base`                  | nothing                              |

- `player` is a handle. It is `nil` for a break with no player, or once that
  player left.
- `held` is the item in hand.
- `by` is `{ cause = "player" | "fire" | "explosion" | "water" | "support", tool, creative }`.
- `body` is `{ id, kind = "player" | "mob" | "item" | "other" }`. `body.kind` is
  `"mob"` for a cow or a zombie.
- `cause` is `"ignite"`, `"explosion"` or `"fire"`. A redstone signal is
  not a cause: it has `on_power`.
- `powered` is `true` when the signal started and `false` when it stopped.
- `from` is a `vec3`. `announced` is the name the notifying block gave.
  **A hook exists only if you write it.** There is no flag such as
  `random_ticks = true`. A block with no `on_step` is never asked about steps.
  **Hooks answer with words, never booleans.** `"used"` takes the click;
  `"pass"` does not. `"none"` leaves nothing. `"table"` leaves what the breaker
  would normally leave. An answer nothing reads is an error that names it.

## Extends, and base

`extends` takes a handle, a game block’s name, a plain table, or a list of
those, **innermost first**. Data fields merge; hooks _wrap_.

```luau
-- A mixin is only a table.
local glowing = { light = 12 }
game.blocks.define { name = "lamp", looks = "gold_block", extends = glowing }

-- A crate that is a tnt underneath.
game.blocks.define {
    name = "bomb",
    looks = "tnt",
    extends = "tnt",
    drops = { { item = "stick", count = 1 } },
    on_break = function(block, player, by, base)
        base(block, player, by)    -- a0.1.0 lights every tnt a player digs
        return "none"              -- ...but this one leaves what *we* said
    end,
}
```

Every hook takes **`base` as its last argument**. Call it to extend the
block underneath; leave it out to replace it. Its effects land when your hook
returns, and a second call counts once.
Two rules for merging:

- **A game block’s data is the floor**, wherever it is in the list.
  `extends = "tnt"` gives tnt’s hardness and blast resistance unless you or a
  mixin set them. Your values beat inherited ones.
- **A hook you do not write is not asked.** The block underneath answers it.
  Extending tnt with no hooks costs nothing, even while your pack sleeps.

## Amending the game’s own

```luau
game.blocks.amend("tnt", {
    on_break = function(block, player, by, base)
        player:message("careful")
        base(block, player, by)
    end,
})
```

- **Hooks only.** A data field is an error that names it. For different
  numbers, use `game.blocks.define { extends = "tnt" }`.
- **Only the game’s own blocks.** Never another pack’s.

## What a missed deadline means, per hook

These rows add to the table under “saying no”. Each hook has a deadline.
This is what a miss means:

| hook                                                                                                                   | a missed deadline means                                                          | why                                                                                                                                                                                                                                     |
| ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `on_use`                                                                                                               | **the click passes through** (`"pass"`)                                          | fail-open. A busy pack must not stop people using the rest of the world, and a click that did nothing is visible where a click that was silently eaten is not.                                                                          |
| `on_break`                                                                                                             | **the block leaves the drops its definition declared** — never the looks block’s | fail-**closed**. `drops = "table"` on a crate that looks like TNT would drop TNT, and anything that makes items must never make them twice. A definition that declared nothing leaves nothing.                                          |
| `on_step`, `on_tick`, `on_random_tick`, `on_place`, `on_neighbour`, `on_trigger`, `on_power`, `on_added`, `on_removed` | **the block did not react this tick**                                            | fail-open, and it costs nothing: the engine had already decided what it was doing. These are batched — five hundred crops taking their random tick are one message under one deadline — and answered at the end of the tick that asked. |
| `can_stay`, `can_place_at` and `power` are **not** pack hooks. A pack block                                            |
| answers them from its definition’s data and what it extends: `power` is a                                              |
| field, below.                                                                                                          |

## Power

A block gives a redstone circuit power, hears one, or both. A script flips
it from anywhere with `world.block(pos)`:

```luau
-- A card reader: a click gives power for two seconds.
game.blocks.define {
    name = "reader",
    looks = { "iron_block", "redstone_block" },
    power = { 0, 15 },                    -- one value per state
    tick_every = 2,
    on_use = function(block) block.state = 2  block:schedule()  return "used" end,
    on_tick = function(block) block.state = 1 end,
}

-- A receiver: something happens when a wire reaches it.
game.blocks.define {
    name = "receiver",
    looks = "note_block",
    on_power = function(block, powered)
        if powered then sound.play("block.note_block.pling", { at = block.at }) end
    end,
}

local door = world.block(vec3(10, 65, 10))   -- the block there, or nil where the chunk is not loaded
if door and door.powered then print(door.name, "has a signal") end
world.block(vec3(4, 65, 4)).state = 2        -- a timer, a command or a zone turns the reader there on
```

`power` says what a state gives:

- A number is every face: `power = 15`. A list is one value per state, like
  `looks`.
- A table keyed by face gives it on those faces only, with the names
  `texture` takes: `power = { top = 15 }`, `power = { 0, { front = 15 } }`.
  `front` and `back` need `facing = true`.
- A value is 0 or 15. The game’s signal has one strength, and a wire fades
  it by itself. Any other number is an error.
- It is the power a block of redstone gives: it lights the wire, lamp or
  piston that touches the face, and does not pass through a solid block.
- A state change that changes the power tells the neighbours. There is no
  `block:notify()` to remember.
- Without `power`, a block gives what it extends gives: `extends = "lever"`.
- Before 1.13 the client draws a wire’s shape itself, from the `looks`
  block. A wire only bends toward a block that looks like a redstone part.
  `on_power` says when the signal changed:
- It is called once when a signal starts to reach the block and once when
  it stops, not for every change beside it. `block.powered` reads it at any
  time, in any hook.
- The signal is the one a lamp reacts to: a lever or a lit wire beside the
  block, or a powered solid block next to it. The block’s own power counts
  when it comes back through a wire.
- The last answer is saved with the block, so a restart repeats nothing.
  For a block of the game (`game.blocks.amend`) it is kept in memory: after
  a restart the first change beside it reports the signal as it is.
- A block of the game that becomes another block when it is powered is two
  blocks: `redstone_lamp` and `lit_redstone_lamp`.
- A pack’s part reacts at the end of the tick, so it is a tick behind the
  game’s own. For exact timing, extend a repeater.
  `world.block(pos)` is the handle a hook gets, for any block:
- Reads are the world as it is now. What it does lands on the next tick,
  like `world.set_block`.
- `block.state` and `block.data` are for blocks this pack defined. On any
  other block they are an error.
- A handle you keep does nothing once its block is gone.
  `world.rules{ redstone = false }` stops every signal in a room. See “Room
  rules”.
