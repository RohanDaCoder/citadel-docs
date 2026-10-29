# SOURCE: Your first pack

## 1. Create the pack

Make a folder named `first` and put this `citadel.yml` inside it:

```yaml
# citadel.yml
name: first
entry: main.luau
motd: My first Citadel pack
spawn_point: [0.5, 65.0, 0.5]
gamemode: 2
mode: lite
world: script
```

`entry` names the script to run. `world: script` means that script supplies
the terrain, and `mode: lite` makes your pack the game. Adventure mode
(`gamemode: 2`) lets players explore without breaking the floor.
`spawn_point` places their feet one block above the floor, in the centre
of the gold marker you will create next.

## 2. Add the script

Create `main.luau` beside `citadel.yml`:

```luau
--!strict
-- A small lobby: solid ground, a welcome, and a way back to spawn.

world.on_generate(function(chunk)
    chunk:fill(
        vec3(chunk.min.x, 64, chunk.min.z),
        vec3(chunk.max.x, 64, chunk.max.z),
        "stone"
    )
    chunk:set(vec3(0, 64, 0), "gold_block")
end)

players.on_join(function(player)
    player.ui.title{
        title = "Welcome",
        subtitle = player.name,
        color = "aqua",
    }
    player:message("Walk around, then type /spawn to return to the gold block.", "aqua")
end)

commands.add("spawn", function(player)
    player:teleport(world.spawn_point)
    player:message("You are back at spawn.", "green")
end, { help = "Return to the lobby spawn" })
```

Read the three callbacks in order:

- `world.on_generate` fills each chunk with a stone floor at y = 64, then
  marks `(0, 64, 0)` with gold. `chunk:set` ignores positions outside its
  chunk. `vec3(x, y, z)` describes a position; y is height.
- `players.on_join` receives the player who joined. The title and message
  go to that player. Register the callback once; Citadel calls it when
  needed.
- `commands.add` registers `spawn` without a slash. When a player types
  `/spawn`, `player:teleport(world.spawn_point)` returns them to the point
  from the manifest. Reading it avoids repeating the coordinates.

## 3. Run it and check your work

With `citadel` on your `PATH`, run this from the directory containing `first`:

```sh
citadel --lite --pack ./first
```

Keep the server running and join `localhost:25565` from Minecraft Java
Edition, or use the address and port configured for your server. You should
see a welcome and stand on the gold block. Walk away, type `/spawn`, and
check that you return to it with a confirmation in chat.

## 4. Make an edit

Change `title = "Welcome"` to `title = "My lobby"` and save. Citadel reloads
`.luau` files while players stay connected, and runs the join callback for
those players again. The new title should appear. If it does not, check
the server log for a script error.
Reloading keeps existing chunks: edits to `world.on_generate` affect newly
generated terrain. Restart after editing `citadel.yml`. As a next exercise,
add a `/hello` command that sends a message to the player who uses it.
