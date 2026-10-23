# SOURCE: Scoreboard with a button

```luau
-- main.luau
world.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "stone")
end)

local board = world.screen{ at = vec3(-2, 68, -10), facing = "south", width = 4, height = 2 }

local function redraw()
    board:clear(colors.black)
    board:text(16, 12, "TAPS", colors.yellow, 40)
    local y = 64
    for _, p in players.list() do
        local score = storage.get("taps." .. p.name) or 0
        board:text(16, y, p.name, colors.white, 28)
        board:text(board.width - 16 - board:measure(tostring(score), 28), y, tostring(score), colors.cyan, 28)
        y += 34
    end
end

players.on_join(function(player)
    player:hotbar{ [1] = { item = "lapis_block", name = "Tap me" } }
    player:message("Right click the block in your hand.", colors.cyan)
    redraw()
end)

players.on_leave(function()
    redraw()
end)

players.on_click(function(player, hit)
    if hit.slot ~= 1 or hit.button ~= "right" then
        return
    end
    local key = "taps." .. player.name
    storage.set(key, (storage.get(key) or 0) + 1)
    sound.play("block.note_block.hat", { at = player.at, pitch = 1.5 })
    redraw()
end)
```
