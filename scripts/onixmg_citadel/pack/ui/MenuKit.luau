--!nonstrict
-- ui/MenuKit.luau
-- The chest-menu kit: every menu's look AND layout in one place (DRY).
--
-- MenuKit.menu is the chest handler. A menu says WHAT it shows —
--
--   kit.menu(p, {
--       title   = <runs>,
--       rows    = 3,                        -- optional; auto when left out
--       content = {                         -- what goes in the chest
--           { items = { ...specs... }, spacing = 1 },  -- a centered row
--           { slot = 11, item = <spec> },              -- or an exact slot
--       },
--       back    = "Return to ...",          -- Back arrow in the last row
--       close   = "Click to close",         -- Close barrier in the last row
--       on_pick = function(who, key) end,
--   })
--
-- — and the kit works out WHERE. A row's items are centered in the
-- nine-wide chest with `spacing` empty slots between neighbours (a row
-- too long for its spacing wraps onto further centered rows); the rows
-- sit vertically centered above the Back/Close line; the chest is sized
-- to what the content needs (1..6 rows) unless `rows` fixes it; panes
-- fill everything left over.
--
-- Picks come back BY KEY, not by slot: any item spec may carry
-- key = <any value> and on_pick receives it, so no menu knows a slot
-- number or re-derives what a clicked slot held. Items without a key
-- are decoration and never fire.
--
-- The helpers stay: pad (the pane filler menu() uses), open_sound, the
-- item shapes (Back arrow, Close barrier, head, game icon), and grid(),
-- which chunks a flat list into centered content rows.

local MenuKit = {}

MenuKit.PANE = "gray_stained_glass_pane"

local function pane()
    return { item = MenuKit.PANE, name = " " }
end

-- Fill a sparse item table out to a full rows x 9 grid with panes.
function MenuKit.pad(items, rows)
    local out = {}
    for i = 1, rows * 9 do
        out[i] = items[i] or pane()
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

-- --- the layout engine --------------------------------------------------

-- How many items with this spacing fit on one nine-wide row: the width
-- (k-1)*(spacing+1)+1 must stay within 9.
local function per_row(spacing)
    return math.floor((9 + spacing) / (spacing + 1))
end

-- The 1-based slots of a centered chest row: k items, `spacing` empty
-- slots between neighbours, on chest row `row` (1-based).
local function row_slots(row, k, spacing)
    local width = (k - 1) * (spacing + 1) + 1
    local col = math.floor((9 - width) / 2) + 1
    local base = (row - 1) * 9
    local slots = {}
    for i = 1, k do
        slots[i] = base + col + (i - 1) * (spacing + 1)
    end
    return slots
end

-- The spec the chest sees: the caller's table minus the pick key.
local function display(spec)
    local out = {}
    for k, v in spec do
        if k ~= "key" then out[k] = v end
    end
    return out
end

-- Chunk a flat list into content rows of `cols` items — the shape for
-- head grids and other lists that may outgrow one row.
function MenuKit.grid(list, cols, spacing)
    local rows = {}
    local i = 1
    while i <= #list do
        local chunk = {}
        for _ = 1, cols do
            if i > #list then break end
            table.insert(chunk, list[i])
            i = i + 1
        end
        table.insert(rows, { items = chunk, spacing = spacing or 0 })
    end
    return rows
end

-- The chest handler (see the header). Returns the ui.menu handle.
function MenuKit.menu(p, opts)
    local placed = {}   -- slot -> the display spec
    local keys = {}     -- slot -> the pick key
    local max_slot = 0
    local layout = {}   -- the {items, spacing} rows the engine centers

    -- Content: exact slots go straight in; item rows are collected (a
    -- row longer than its spacing allows wraps onto further rows).
    for _, entry in opts.content or {} do
        if entry.slot then
            local spec = entry.item
            if spec.key then keys[entry.slot] = spec.key end
            placed[entry.slot] = display(spec)
            if entry.slot > max_slot then max_slot = entry.slot end
        else
            local spacing = entry.spacing or 0
            local size = per_row(spacing)
            local i = 1
            while i <= #entry.items do
                local chunk = {}
                for _ = 1, size do
                    if i > #entry.items then break end
                    table.insert(chunk, entry.items[i])
                    i = i + 1
                end
                table.insert(layout, { items = chunk, spacing = spacing })
            end
        end
    end

    -- The Back/Close line: one centered row at the bottom of the chest.
    local nav = {}
    if opts.back then
        local it = MenuKit.back_item(opts.back)
        it.key = "back"
        table.insert(nav, it)
    end
    if opts.close then
        local it = MenuKit.close_item(opts.close)
        it.key = "close"
        table.insert(nav, it)
    end

    -- Chest size: the rows the content needs, unless fixed outright.
    local rows = opts.rows
    if not rows then
        rows = #layout + (#nav > 0 and 1 or 0)
        local needed = math.ceil(max_slot / 9)
        if needed > rows then rows = needed end
    end
    if rows < 1 then rows = 1 elseif rows > 6 then rows = 6 end

    -- Place the item rows, vertically centered above the nav line.
    local first = math.ceil((rows - #nav - #layout) / 2) + 1
    if first < 1 then first = 1 end
    for ri, row in layout do
        local slots = row_slots(first + ri - 1, #row.items, row.spacing)
        for i, spec in row.items do
            local slot = slots[i]
            if slot and slot <= rows * 9 then
                if spec.key then keys[slot] = spec.key end
                placed[slot] = display(spec)
            end
        end
    end
    if #nav > 0 then
        local slots = row_slots(rows, #nav, 1)
        for i, spec in nav do
            local slot = slots[i]
            if slot and slot <= rows * 9 then
                keys[slot] = spec.key
                placed[slot] = display(spec)
            end
        end
    end

    MenuKit.open_sound(p)
    return p.ui.menu{
        title = opts.title,
        items = MenuKit.pad(placed, rows),
        on_pick = function(who, n)
            local key = keys[n]
            if key ~= nil and opts.on_pick then
                opts.on_pick(who, key)
            end
        end,
    }
end

return MenuKit
