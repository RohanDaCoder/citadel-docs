# SOURCE: Your first pack

## Before you start
You need Minecraft Java Edition, a text editor, and a Citadel server you
can run or edit. On your own machine, the commands below assume the
`citadel` executable is on your `PATH`. If you built it from source, use
the path to `target/release/citadel` instead.
A **pack** is a folder containing configuration and Luau scripts. Citadel
runs those scripts on the server; players join with their normal Minecraft
client. You do not need to compile the scripts or install a client mod.
This guide uses **lite mode**, where your pack supplies the world and the
game’s behaviour. By the end, a player will spawn on a gold block, see a
welcome, and be able to walk away and return with `/spawn`.
## 1. Create the two files
Make a folder named `first`. Inside it, create these two files:
```text
first/
  citadel.yml
  main.luau
```
Put this in `citadel.yml`:
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
| Setting | What it does here |
| --- | --- |
| `name` | Names this pack `first`. |
| `entry` | Tells Citadel to run `main.luau` when the pack loads. |
| `motd` | Sets the description shown in Minecraft’s server list. |
| `spawn_point` | Places a joining player’s feet at x = 0.5, y = 65, z = 0.5. |
| `gamemode: 2` | Uses adventure mode, so players can explore without breaking the floor. |
| `mode: lite` | Selects a game controlled by your scripts. |
| `world: script` | Asks your script to generate the terrain. |
This is the **pack’s** `citadel.yml`. A separate `citadel.yml` in the
directory where you start the server configures things such as its port.
Keep the pack inside `first`, and run the local commands below from the
directory containing `first`.
Start `main.luau` with `--!strict`. This enables strict checking in an
editor configured with Citadel’s `citadel.d.luau` type definitions. The
pack can run without that editor setup.
## 2. Give players ground to stand on
Add this below `--!strict` in `main.luau`:
```luau
-- main.luau
world.on_generate(function(chunk)
    chunk:fill(
        vec3(chunk.min.x, 64, chunk.min.z),
        vec3(chunk.max.x, 64, chunk.max.z),
        "stone"
    )
    chunk:set(vec3(0, 64, 0), "gold_block")
end)
```
Minecraft divides the world into **chunks**, each 16 blocks wide and 16
blocks deep. `world.on_generate` registers a function that Citadel calls
when it needs a chunk’s terrain. The `chunk` argument is the chunk being
built.
`vec3(x, y, z)` describes a position: x and z are horizontal; y is height.
`chunk:fill` fills the box between two corners, including both corners.
Using the chunk’s x and z bounds and y = 64 for both corners makes a stone
floor one block thick. Every generated chunk gets that floor.
`chunk:set` replaces one floor block with gold. It ignores coordinates
outside the current chunk, so only the chunk containing `(0, 64, 0)` gets
the marker. The spawn point is one block above it; the `.5` coordinates
place the player in the centre of the block.
Keep terrain generation repeatable: the same chunk should receive the same
blocks each time the function is called.
## 3. Run the pack and join
From the directory containing `first`, run:
```sh
citadel --lite --pack ./first
```
Leave that terminal open. In Minecraft, choose **Multiplayer → Direct
Connection**, enter `localhost:25565`, and join. If your server uses a
different port, use that port instead.
On a hosted Minefort server, put the `first` folder in the server’s `packs`
directory, select lite mode, and start the server. Join using the address
shown for that server.
**Check:** you should stand on a gold block surrounded by a flat stone
floor. Walk a few blocks and look back at the marker. There is no welcome
message or `/spawn` command yet; you will add those next.
## 4. Welcome each player
Append this after the terrain code:
```luau
-- main.luau
players.on_join(function(player)
    player.ui.title{
        title = "Welcome",
        subtitle = player.name,
        color = "aqua",
    }
    player:message("Walk around, then type /spawn to return to the gold block.", "aqua")
end)
```
`players.on_join` registers another function, this time for a player joining.
Citadel passes that player into the function as `player`. `player.name`
reads their name; `player.ui.title` shows them a title; `player:message`
sends them a chat message. These calls address that one player.
The code inside the function runs when the event happens. Register the
function once at the top level of the script; you do not need a loop that
keeps checking for new players.
Save `main.luau` while connected. Citadel reloads the script and runs its
join callbacks for players already online too.
**Check:** a “Welcome” title should appear with your name underneath it,
and chat should explain `/spawn`. That command is the next step.
## 5. Add a command that does something
Append this below the welcome code:
```luau
-- main.luau
commands.add("spawn", function(player)
    player:teleport(world.spawn_point)
    player:message("You are back at spawn.", "green")
end, { help = "Return to the lobby spawn" })
```
`commands.add` registers the name `"spawn"` without the slash. When a player
types `/spawn`, Citadel calls the function with the player who used it.
The `help` text describes the command.
`world.spawn_point` reads the spawn configured in `citadel.yml`, so you do
not need to repeat its coordinates in the script. `player:teleport` moves
the player there, and the message confirms the action.
Notice the colon in `player:teleport(...)` and `chunk:fill(...)`: these are
methods acting on a particular player or chunk. Namespace functions such
as `commands.add(...)` and `player.ui.title(...)` use a dot. Follow the
signature shown in the reference when using a new API.
**Check:** save, walk away from the gold block, and type `/spawn`. You
should return to the marker and see “You are back at spawn.” in chat.
## 6. Make a change and check it
Change `title = "Welcome"` to `title = "My lobby"`, then save. The new title
should appear without disconnecting you. Try `/spawn` again to confirm the
rest of the pack still works.
A script reload keeps the existing world. Changing the floor in
`world.on_generate` affects newly generated chunks; it does not repaint the
stone already around you. Restart after changing the pack manifest.
If a step does not work, check the server log first:
| What you see | What to check |
| --- | --- |
| The server cannot find the pack | Run from the directory containing `first`, or pass the full folder path to `--pack`. |
| You cannot connect | Keep the server running and use its configured address and port. |
| There is no floor | Check `world: script`, the `entry` filename, and any error reported while loading `main.luau`. |
| `/spawn` is unknown | Check that you saved the command block in the loaded pack and that the script reloaded successfully. |
| An edit does not take effect | Look for a filename and line number in the log. If loading the new script fails, Citadel keeps the previous working script. |
## The complete script
Your final `main.luau` should look like this. Use it to compare with your
file, or replace the file with it; do not append a second copy.
```luau
-- main.luau
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
You have used three entry points: terrain generation for the world,
`players.on_join` for a player’s arrival, and `commands.add` for an action
the player chooses.
## Try this next
- Change the welcome text and its colour, save, and check the result.
- Add a `/hello` command that sends a message to the player who uses it.
- Add another gold marker in the terrain function, then look for it in a
newly generated chunk.
Continue with **Coin rush** to add an objective, a score, and repeating
rounds. It builds on the pack structure and event callbacks you used here.
