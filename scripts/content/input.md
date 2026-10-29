---
title: "Input"
url: /docs/citadel/input
---

# Input

- One click is one event.
- A held button repeats every 200 ms. That is not a click.
- A left click on the world carries the block under the crosshair, up to
five blocks from the eyes.
- On a pack server, a click never changes the world.
The first `players.on_chat` takes over chat in its room. Each line is then
said once as `<name> text`, unless a listener returns `false`. With several
packs, each gets every line; it is still said once or not at all.
