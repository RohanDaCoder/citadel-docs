--!nonstrict
-- tasks/Tasks.luau
-- One purpose: start every background task — the single registration
-- point for the task layer. Adding a task means adding a task file and
-- one line here.

local TabAnimateTask = require("tasks/TabAnimateTask")
local DiscordBroadcastTask = require("tasks/DiscordBroadcastTask")
local VoidSafetyTask = require("tasks/VoidSafetyTask")
local CycleTask = require("tasks/CycleTask")

local Tasks = {}

function Tasks.start()
    TabAnimateTask.start()
    DiscordBroadcastTask.start()
    VoidSafetyTask.start()
    CycleTask.start()
end

return Tasks
