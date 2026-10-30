--!nonstrict
-- util/Perms.luau
-- Permission checks. `onix.admin` is the staff node (citadel.yml grants it
-- to the staff group); in a development workload everyone is an admin so
-- the panel and admin commands are testable solo.

local Perms = {}

function Perms.is_admin(p)
    if p:has("onix.admin") then return true end
    return citadel.env == "development"
end

return Perms
