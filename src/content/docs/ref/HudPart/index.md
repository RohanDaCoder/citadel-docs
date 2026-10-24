---
title: "HudPart type"
description: "One item of a shown layout, hud.hp: its live values"
---

One item of a shown layout, `hud.hp`: its live values. They tween.

## Fields

| Field                                                 | Purpose                                                                   |
| ----------------------------------------------------- | ------------------------------------------------------------------------- |
| [`hudPart.fill: number`](/ref/HudPart/fill/)          | How much of a box or picture shows, from its left edge: 0 to 1.           |
| [`hudPart.text: string`](/ref/HudPart/text/)          | A label's words.                                                          |
| [`hudPart.visible: boolean ?`](/ref/HudPart/visible/) | Whether it shows; nil shows it again.                                     |
| [`hudPart.color: Ink ?`](/ref/HudPart/color/)         | A box's colour, a picture's tint, a label's ink; reads back as "#rrggbb". |
