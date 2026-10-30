--!nonstrict
-- ui/MenuKit.luau
-- The shared building blocks every menu uses (DRY): pane padding, the
-- opening click sound, and the repeated item shapes (Back arrow, Close
-- barrier, player head, glinted game icon). One place to change a look
-- that was copy-pasted across nine menus.

local MenuKit = {}

MenuKit.PANE = "gray_stained_glass_pane"

-- Fill a sparse item table out to a full rows x 9 grid with panes.
function MenuKit.pad(items, rows)
    local out = {}
    local n = rows * 9
    for i = 1, n do
        out[i] = items[i] or { item = MenuKit.PANE, name = " " }
    end
    return out
end

-- The click every menu opened with.
function MenuKit.open_sound(p)
    p:sound("ui.button.click", { volume = 0.5, pitch = 1.2 })
end

function MenuKit.back_item(lore)
    return { item = "arrow", name = { { "Back", color = "red", bold = true } }, lore = { lore } }
end

function MenuKit.close_item(lore)
    return { item = "barrier", name = { { "Close", color = "red", bold = true } }, lore = { lore } }
end

function MenuKit.head(name)
    return {
        item = "player_head",
        skin = name,
        name = { { name, color = "aqua" } },
    }
end

-- The old game icons: named, bold, with glint.
function MenuKit.game_icon(g)
    return {
        item = g.icon or "paper",
        name = { { g.name, color = g.title_color or "yellow", bold = true } },
        glint = true,
    }
end

return MenuKit
