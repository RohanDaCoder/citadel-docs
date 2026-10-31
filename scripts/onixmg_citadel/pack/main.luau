--!nonstrict
-- main.luau — the pack entry and composition root.
--
-- This file only wires: it registers the four games, installs and shows
-- the arena, logs the boot lines, installs the event handlers, registers
-- the commands, starts the background tasks and logs ready. Every
-- behaviour lives in exactly one single-purpose module:
--   core/     GameState, Arena, Messages, Stats, GameRegistry, VoteBook,
--             Lobby, Eliminator, RoundRunner, ResultSequence, CycleLoop,
--             CycleControls
--   games/    Game (base) + Spleef, TNTRun, Sumo, HotPotato
--   ui/       MenuKit, Sidebar, ActionBar, Titles, Tab, Motd, Hotbar,
--             menus/ (one file per menu)
--   events/   Events installer + handlers/ (one file per player event)
--   tasks/    Tasks installer + one file per background task
--   commands/ Registrar (shared plumbing) + Commands catalog +
--             standalone/ (one file per player command) + onix/
--             (the grouped /onix tree, one file per subcommand)
--   boot/     BootLog, SpawnProbe

local GameRegistry = require("core/GameRegistry")
local Arena = require("core/Arena")
local Events = require("events/Events")
local Commands = require("commands/Commands")
local Tasks = require("tasks/Tasks")
local BootLog = require("boot/BootLog")

-- Register the four games. Spleef and TNT Run are votable; Sumo and Hot
-- Potato register with votable = false (commented out on the live server).
GameRegistry:register(require("games/Spleef"))
GameRegistry:register(require("games/TNTRun"))
GameRegistry:register(require("games/Sumo"))
GameRegistry:register(require("games/HotPotato"))

Arena:install()
Arena:show("lobby")

BootLog.log()
Events.install()
Commands.register()
Tasks.start()

citadel.log("[onixmg] ready")
