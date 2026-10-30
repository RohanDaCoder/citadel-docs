--!nonstrict
-- commands/Commands.luau
-- Every slash command the pack registers: /vote, /startgame, /stopgame,
-- /settimer, /changemapstate, /eliminate, /spawn, /center, /discord,
-- /list, /profile, /adminpanel. Cooldowns match the live Skript's
-- (/spawn 3s, /startgame and /stopgame 2s). main.luau calls register()
-- once after the modules are wired.

local state = require("core/GameState")
local registry = require("core/GameRegistry")
local Arena = require("core/Arena")
local Messages = require("core/Messages")
local VoteBook = require("core/VoteBook")
local CycleDriver = require("core/CycleDriver")
local Menus = require("ui/Menus")
local Sidebar = require("ui/Sidebar")
local Cooldown = require("commands/Cooldown")
local Perms = require("util/Perms")

local Commands = {}

function Commands.register()
    commands.add("vote <game:word>", function(p, args)
        VoteBook.cast(p, args.game)
    end, {
        help = "Vote for the next minigame",
        suggest = {
            game = function()
                return state.phase == "Lobby" and registry:votable() or {}
            end,
        },
    })

    commands.add("startgame", function(p)
        if not Perms.is_admin(p) then return "You do not have permission." end
        if Cooldown.check(p, "cmd_startgame", 2) then return end

        if not state.running then
            CycleDriver:start()
            Messages.tell(p, "System started.", "green")
            return
        end
        if not CycleDriver:skipVote(p) then
            Messages.deny_runs(p, {
                { "Server is in ", color = "gray" },
                { state.phase, color = "yellow" },
                { " state.", color = "gray" },
            })
        end
    end, { help = "Skip the vote wait" })

    commands.add("stopgame", function(p)
        if not Perms.is_admin(p) then return "You do not have permission." end
        if Cooldown.check(p, "cmd_stopgame", 2) then return end
        if not CycleDriver:stop() then
            Messages.deny(p, "System is already disabled!")
        end
    end, { help = "Shut the cycle down" })

    commands.add("settimer <seconds:integer 1..>", function(p, args)
        if not Perms.is_admin(p) then return "You do not have permission." end
        CycleDriver:setTimer(args.seconds, p)
    end, { help = "Set the current timer" })

    commands.add("changemapstate [state:word]", function(p, args)
        if not Perms.is_admin(p) then return "You do not have permission." end
        if state.phase == "Ingame" then
            return "The map cannot change during a game."
        end
        if args.state then
            if not Arena:show(args.state) then
                return "No map state named " .. args.state .. "."
            end
            Arena:send(p, "lobby")
            Sidebar.refresh()
        else
            Menus.map_states(p)
        end
    end, {
        help = "Open the map state picker, or paste a state directly",
        suggest = { state = function() return Arena:maps() end },
    })

    commands.add("eliminate <target:player>", function(p, args)
        if not Perms.is_admin(p) then return "You do not have permission." end
        if not CycleDriver:eliminate(args.target) then
            return "That player is not in a round."
        end
    end, { help = "Remove a player from the round" })

    -- /spawn [player]: 3-second cooldown, admins may send someone else —
    -- and spawn() runs for the sender at the end either way.
    commands.add("spawn [target:player]", function(p, args)
        local now = time.now()
        local last = p.data.spawn_last or -100
        if now - last < 3 then
            Messages.tell(p, string.format(
                "Please wait %d seconds before using /spawn again.",
                math.ceil(3 - (now - last))), "red")
            return
        end
        p.data.spawn_last = now

        if args.target and args.target ~= p then
            if not Perms.is_admin(p) then
                Messages.tell(p, "Only administrators can teleport other players.", "red")
                return
            end
            CycleDriver:lobby(args.target)
            p:message({
                { "You have teleported ", color = "gray" },
                { args.target.name, color = "white" },
                { " to spawn.", color = "gray" },
            })
        end

        if state.phase == "Ingame" and state:in_roster(p) then
            CycleDriver:eliminate(p)
        else
            CycleDriver:lobby(p)
        end
    end, { aliases = { "hub" }, help = "Return to spawn" })

    commands.add("center [yaw:number] [pitch:number]", function(p, args)
        if not Perms.is_admin(p) then
            return "You do not have permission to center yourself."
        end
        local at = p.at
        local rot = p.rotation
        p:teleport(
            vec3(math.floor(at.x) + 0.5, math.floor(at.y), math.floor(at.z) + 0.5),
            { yaw = args.yaw or rot.yaw, pitch = args.pitch or rot.pitch }
        )
        Messages.tell(p, "You have been centered!", "yellow")
        p:sound("entity.enderman.teleport", { volume = 0.5, pitch = 2 })
    end, {
        help = "Snap to the centre of your block",
        suggest = {
            yaw = { "0", "90", "180", "-90" },
            pitch = { "0", "90", "-90" },
        },
    })

    commands.add("discord", function(p)
        Messages.discord_broadcast(p)
        p:sound("entity.experience_orb.pickup", { volume = 0.5, pitch = 1 })
    end, {
        aliases = { "dc", "dcserver", "discordserver", "onixdiscord" },
        help = "Join the official discord server",
    })

    commands.add("list", function(p)
        local names = {}
        for _, q in players.list() do table.insert(names, q.name) end
        Messages.tell(p, "There are " .. #names .. " players online: " .. table.concat(names, ", "))
    end, { help = "See who else is online" })

    commands.add("profile [target:player]", function(p, args)
        Menus.profile(p, args.target or p)
    end, { help = "Your stats, or another player's" })

    commands.add("adminpanel", function(p)
        Menus.admin(p)
    end, { aliases = { "ap" }, help = "Open the admin panel" })
end

return Commands
