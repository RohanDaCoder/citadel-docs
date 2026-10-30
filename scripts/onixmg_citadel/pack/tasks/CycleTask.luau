--!nonstrict
-- tasks/CycleTask.luau
-- One purpose: launch the round cycle (core/CycleLoop) in the background.

local CycleLoop = require("core/CycleLoop")

local CycleTask = {}

function CycleTask.start()
    task.spawn(function() CycleLoop:run() end)
end

return CycleTask
