---
title: "Hit type"
description: "What players.on_click hands its callback: the button, the slot, and the player, entity, block and face the click met."
---

What `players.on_click` hands its callback: the button, the slot, and the player, entity, block and face the click met.

## Fields

| Field                                                                   | Purpose                                                                                                              |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| [`hit.button: "left" \| "right"`](/ref/Hit/button/)                     | "left" is an attack or swing, "right" is an interact or use.                                                         |
| [`hit.slot: number`](/ref/Hit/slot/)                                    | The hotbar slot in hand, 1..9.                                                                                       |
| [`hit.player: Player ?`](/ref/Hit/player/)                              | Another player, when that is what was clicked.                                                                       |
| [`hit.entity: (Display \| Hitbox \| Npc \| Puppet)?`](/ref/Hit/entity/) | The thing clicked, as the handle the script holds for it.                                                            |
| [`hit.entity_id: number ?`](/ref/Hit/entity_id/)                        | Its raw entity id, which is all there is for something the engine made itself, such as one of a screen's own frames. |
| [`hit.block: Vec3 ?`](/ref/Hit/block/)                                  | The block, when the click hit one.                                                                                   |
| [`hit.face: Face ?`](/ref/Hit/face/)                                    | The face of the block that was clicked.                                                                              |
