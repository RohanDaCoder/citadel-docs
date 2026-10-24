# SOURCE: Building well

**Plan before code.** Write the plan as a comment at the top of the build:

1. What makes it recognisable at a glance? A keep is tall, square and
   crowned; a market is low and crowded.
2. Its parts, each with bounds, material and joins: footing, body, openings,
   roof, trim, props.
3. Its setting: neighbours, ground, and the way a player approaches.
4. Where detail goes: the skyline, doors, windows, corners, the roof line,
   places a player stops.
   **Build in that order, and look at each stage before the next.** End each
   stage with a render and a check. Name the parts as you go (`b:part`), so
   renders and the check can name them.
   | stage | what is built | look with | ask | | --- | --- | --- | --- |
   | 1. massing | the footprint, the main volumes, the roof shapes | `--view sides,roof` | Does the outline say what it is? Are the proportions right: towers tall enough, roof steep enough, wings in scale? |
   | 2. architecture | openings, wall depth, eaves, how parts join | `--view approach,entrance,plan` and `citadel check` | Are windows holes with sills and frames? Does the way in read? Can a player walk to every floor? |
   | 3. setting and detail | paths, ground, lighting, props, trim | `--view approach,cutaway` and `citadel check` | Does it sit in a place? Is the detail where the eye goes? |
   At each stage:

- Write down the three worst problems the pictures and the check show.
- Fix those, then look again with the same views.
- Finish every fix before the next stage.
- Render again only after a change or for a new question.
  **The four ways a build fails:**
- _Painted flat._ A window keeps its glass in the wall’s plane, with a sill
  and a frame that stand out in front of it; glass pushed behind a wall one
  block thick sits inside the room. Give walls depth: plinths, beams, cornices.
- _Visible boxes._ Taper what grows: a tower narrows, a roof flares at its
  eaves. Break long edges. Let parts overlap and sink into each other.
- _No setting._ Add a path, a fence, a tree, a barrel, a lamp, and shape the
  ground to meet them.
- _Detail everywhere, or nowhere._ Put detail where the eye goes.
  **Half blocks are the detail.** Use `detail = 2` for shapes finer than a
  block: roofs, eaves, sills, steps, cornices, arches. The build turns half
  steps into stairs and slabs. Name `oak_fence` or `glass_pane` and the build
  joins them.
  **Conventions that keep a build square.**
- An axis of symmetry runs through a block’s middle, so a symmetric thing is
  odd: a door 1 or 3 wide, a gate 5, a path 3.
  `build:mirror("x")` of one half gives the other.
- A block is inside a circle when `math.sqrt(dx * dx + dz * dz) <= r + 0.5`.
  The `+ 0.5` gives flat edges.
- Mix a large surface from two or three blocks of one family, chosen by a
  hash of the position. A restart then builds the same wall.
- Write a part once, round its own middle. Place it with `build:rotate` and
  `build:mirror`.

```luau
-- Helpers a pack writes for itself; nothing here is the engine's.
local function hash(x, y, z)                         -- 0..1, the same every time
    local v = math.sin(x * 12.9898 + y * 4.1414 + z * 78.233) * 43758.5453
    return v - math.floor(v)
end
local function mix(x, y, z, blocks)                  -- { "stone_bricks", "stone_bricks", "cracked_stone_bricks" }
    return blocks[math.floor(hash(x, y, z) * #blocks) + 1]
end
local function disc(b, at, r, block)                 -- 2r + 1 across, round the block `at`
    for dx = -r, r do
        for dz = -r, r do
            if math.sqrt(dx * dx + dz * dz) <= r + 0.5 then
                b:block(at + vec3(dx, 0, dz), block)
            end
        end
    end
end
local function cone(b, at, r, height, block)         -- a tower roof, widest at `at`
    for y = 0, height do
        local rr = r * (1 - y / (height + 1))
        for dx = -r, r do
            for dz = -r, r do
                if math.sqrt(dx * dx + dz * dz) <= rr + 0.5 then
                    b:block(at + vec3(dx, y, dz), block)
                end
            end
        end
    end
end
```

**Look at it, and say what you saw.** Only `citadel render` and `citadel check` (see “seeing what you built” and “checking what you built”) prove a
build good.

- Judge only pictures taken after the last edit.
- Fix every `fix` from `citadel check`, or say it is deliberate. Weigh
  advice against the build’s purpose, and say what you chose.
- After an edit to one part, run `citadel check --since` to show the other
  parts did not change.
- The pictures are flat colour. Report textures as unchecked.
- Report what you looked at, what you fixed, and what is left.
