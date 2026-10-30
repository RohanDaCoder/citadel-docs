--!nonstrict
-- util/Text.luau
-- Run-list helpers. Citadel messages are lists of { text, color=, bold= }
-- runs; `cat` joins two run lists into one (Luau has no `..` for tables).

local Text = {}

function Text.cat(a, b)
    local out = {}
    for _, run in a do table.insert(out, run) end
    for _, run in b do table.insert(out, run) end
    return out
end

return Text
