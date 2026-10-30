--!nonstrict
-- tasks/TabAnimateTask.luau
-- One purpose: animate the tab list — paint frame 1 immediately, then
-- swap the logo's two frames every 3 seconds, as TAB did.

local Tab = require("ui/Tab")

local TabAnimateTask = {}

function TabAnimateTask.start()
    Tab.set(1)
    task.spawn(function()
        local frame = 1
        while true do
            task.wait(3)
            frame = frame == 1 and 2 or 1
            Tab.set(frame)
        end
    end)
end

return TabAnimateTask
