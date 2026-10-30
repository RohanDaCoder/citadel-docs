--!nonstrict
-- events/Events.luau
-- One purpose: bind every Citadel player event to its handler module —
-- the single registration point for the event layer. Adding an event
-- means adding a handler file and one line here.

local ChatHandler = require("events/handlers/ChatHandler")
local JoinHandler = require("events/handlers/JoinHandler")
local LeaveHandler = require("events/handlers/LeaveHandler")
local RespawnHandler = require("events/handlers/RespawnHandler")
local ClickHandler = require("events/handlers/ClickHandler")
local DamageHandler = require("events/handlers/DamageHandler")

local Events = {}

function Events.install()
    players.on_chat(ChatHandler.handle)
    players.on_join(JoinHandler.handle)
    players.on_leave(LeaveHandler.handle)
    players.on_respawn(RespawnHandler.handle)
    players.on_click(ClickHandler.handle)
    players.on_damage(DamageHandler.handle)
end

return Events
