---
title: "Block type"
description: "One block the game version has, in its own numbers, from game.block(name): hardness, light, fire and material."
---

One block the game version has, in its own numbers, from `game.block(name)`: hardness, light, fire and material.

## Fields

| Field                                                                                      | Purpose                                                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`block.name: string`](/ref/Block/name/)                                                   | The block's canonical name.                                                                                                                                                                                       |
| [`block.behaviour: string ?`](/ref/Block/behaviour/)                                       | The rule Citadel runs for it, such as "grass", "flowing", "torch" or "falling"; nil for a block that does nothing on its own.                                                                                     |
| [`block.hardness: number`](/ref/Block/hardness/)                                           | Seconds-scale hardness in this version's numbers; below zero is unbreakable.                                                                                                                                      |
| [`block.random_ticks: boolean`](/ref/Block/random_ticks/)                                  | Whether the random-tick pass acts on it.                                                                                                                                                                          |
| [`block.opaque: boolean`](/ref/Block/opaque/)                                              | Whether it is an opaque full cube, which is not the material's question.                                                                                                                                          |
| [`block.light: number`](/ref/Block/light/)                                                 | What it gives off, 0..15, and what a step through it takes away.                                                                                                                                                  |
| [`block.light_filter: number`](/ref/Block/light_filter/)                                   | What a step through it takes off the light, 0 to 15.                                                                                                                                                              |
| [`block.resistance: number ?`](/ref/Block/resistance/)                                     | The three the block-update tables own: nil in a game that has none.                                                                                                                                               |
| [`block.flammability: { catches: number, burns_away: number }?`](/ref/Block/flammability/) | Fire's two numbers: how readily it catches and how fast it burns away. Nil in a game with no block-update tables.                                                                                                 |
| [`block.material: Material ?`](/ref/Block/material/)                                       | The jar's Material as five questions; nil in a game with no block-update tables.                                                                                                                                  |
| [`block.drops: boolean ?`](/ref/Block/drops/)                                              | The one field a pack writes. Whether a block of this kind that the world breaks by itself leaves its item: true leaves it on a lite world too, false never, nil is the world's default. Reads what this pack set. |
