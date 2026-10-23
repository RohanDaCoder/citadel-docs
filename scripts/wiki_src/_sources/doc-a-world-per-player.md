# SOURCE: A world per player

```luau
-- main.luau
local COURSE = { vec3(0, 65, 4), vec3(4, 66, 8), vec3(-3, 68, 12) }

world.on_generate(function(chunk)
    chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "stone")
end)

players.on_join(function(player)
    player.ui.title{ title = "Lobby", subtitle = "type /play", color = colors.cyan }
end)

commands.add("play", function(player)
    local mine = rooms.create{
        spawn_point = vec3(0.5, 65, 0.5),
        generate = function(chunk)
            chunk:fill(vec3(chunk.min.x, 64, chunk.min.z), vec3(chunk.max.x, 64, chunk.max.z), "stone")
            for _, at in COURSE do
                chunk:set(at, "gold_block")
            end
        end,
    }
    mine.players.on_join(function(p)
        p:message("Reach every gold block.", colors.yellow)
        mine.ui.title{ title = "Go", color = colors.lime }
    end)
    mine.players.on_leave(function()
        if mine.players.count() == 0 then mine:destroy() end   -- the last one out closes it
    end)
    player:move_to(mine)
end)
```
