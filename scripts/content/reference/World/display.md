---
title: "world.display"
url: /docs/citadel/reference/World/display
---

# world.display

A model stands in the world through the same call as everything else, and is the one kind that hands back something other than a Display.

```
world.display((opts: { kind: "model", model: Model, at: Vec3?, rotation: Orientation?, scale: (number | Vec3)?, -- models require equal positive axes paint: { [string]: Ink }?, fallback: string?, seats: { Vec3 }?, lead: boolean?, }) -> ModelDisplay) →  & ((opts: { kind: "item" | "text" | "block" | "frame", at: Vec3?, rotation: Orientation?, scale: (Vec3 | number)?, billboard: Billboard?, glow: (Ink | false)?, item: ItemSpec?, canvas: Canvas?, context: Context?, text: Text?, color: Ink?, background: (Ink | false)?, line_width: number?, shadow: boolean?, block: string?, facing: ScreenFacing?, invisible: boolean?, glide: number?, lead: boolean?, }) -> Display)
```


## Parameters


## Returns


## Used in
- [``world.display{ kind = "text", colour = "red" }` stops the script with`API basics](/docs/citadel/api-basics)
- [`world.display{ kind = "text", text = "Bet 50", at = pad }`Client versions](/docs/citadel/client-versions)
- [`| `display` | `world.display`, any kind | 1.19.4 |`Client versions](/docs/citadel/client-versions)
- [`world.display { kind = "text", at = vec3(0.5, 70, 0.5), text = { "WINNER", effect = sparkle } }`Text formatting](/docs/citadel/text-formatting)
- [`local card = world.display{ kind = "frame", at = vec3(3, 65, 7), facing = "up", canvas = deck[12], invisible = true }`Map pictures](/docs/citadel/map-pictures)
- [`local d = world.display{`Displays](/docs/citadel/displays)
- [`world.display{ kind = "item", at = vec3(2.5, 66, 0.5),`Displays](/docs/citadel/displays)
- [`local d = world.display{`3D models](/docs/citadel/3d-models)
