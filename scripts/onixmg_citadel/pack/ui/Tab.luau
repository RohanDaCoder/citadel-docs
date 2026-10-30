--!nonstrict
-- ui/Tab.luau
-- One purpose: paint the tab list — the two-frame OnixMinigames logo
-- header (in the exact per-letter colours the live server cycled), the
-- yellow gradient line, and the ᴏɴʟɪɴᴇ footer. set(frame) paints one
-- frame; the cycling is tasks/TabAnimateTask's job.

local Tab = {}

-- The logo's two frames, in the exact per-letter colours the live server
-- cycled; the line is the yellow gradient of underscores.
local function logo(frame)
    local f1 = {
        { 0x7A, 0x8B, 0xFA, "O" }, { 0x73, 0x85, 0xEC, "ɴ" },
        { 0x6B, 0x7F, 0xDE, "ɪ" }, { 0x64, 0x79, 0xD0, "x " },
        { 0x5C, 0x73, 0xC2, "M" }, { 0x55, 0x6D, 0xB4, "ɪ" },
        { 0x4D, 0x67, 0xA6, "ɴ" }, { 0x46, 0x61, 0x98, "ɪ" },
        { 0x3E, 0x5B, 0x8A, "ɢ" }, { 0x37, 0x55, 0x7C, "ᴀ" },
        { 0x2F, 0x4F, 0x6E, "ᴍ" }, { 0x28, 0x49, 0x60, "ᴇ" },
        { 0x20, 0x43, 0x52, "s" },
    }
    local f2 = {
        { 0x73, 0x85, 0xEC, "O" }, { 0x7A, 0x8B, 0xFA, "ɴ" },
        { 0x73, 0x85, 0xEC, "ɪ" }, { 0x6B, 0x7F, 0xDE, "x " },
        { 0x64, 0x79, 0xD0, "M" }, { 0x5C, 0x73, 0xC2, "ɪ" },
        { 0x55, 0x6D, 0xB4, "ɴ" }, { 0x4D, 0x67, 0xA6, "ɪ" },
        { 0x46, 0x61, 0x98, "ɢ" }, { 0x3E, 0x5B, 0x8A, "ᴀ" },
        { 0x37, 0x55, 0x7C, "ᴍ" }, { 0x2F, 0x4F, 0x6E, "ᴇ" },
        { 0x28, 0x49, 0x60, "s" },
    }
    local runs = {}
    for _, t in (frame == 1 and f1 or f2) do
        table.insert(runs, {
            t[4],
            color = color(t[1] / 255, t[2] / 255, t[3] / 255),
            bold = true, italic = true,
        })
    end
    return runs
end

local function line()
    local runs = {}
    for i = 1, 36 do
        local f = (i - 1) / 35
        table.insert(runs, {
            "_",
            color = color((0xFF + (0xFF - 0xFF) * f) / 255,
                          (0xFF + (0xFF - 0xFF) * f) / 255,
                          (0x0F + (0x92 - 0x0F) * f) / 255),
        })
    end
    return runs
end

function Tab.set(frame)
    ui.tab{
        header = { line(), logo(frame), "" },
        footer = {
            { { "ᴏɴʟɪɴᴇ: ", color = "gray" }, { tostring(players.count()), color = "yellow" } },
            "",
            line(),
        },
    }
end

return Tab
