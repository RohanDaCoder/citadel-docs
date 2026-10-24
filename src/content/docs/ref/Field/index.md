---
title: "Field type"
description: "A number at every block, as a recipe the engine works out"
---

A number at every block, as a recipe the engine works out. Sums (`+ - * / ^` and unary minus) and the methods make new fields; a plain number is a field too. A field above 0.5 is "true" where a rule asks a question.

## Functions

| Call                           | Purpose                                                                                         |
| ------------------------------ | ----------------------------------------------------------------------------------------------- |
| [`abs`](/ref/Field/abs/)       |                                                                                                 |
| [`floor`](/ref/Field/floor/)   |                                                                                                 |
| [`sqrt`](/ref/Field/sqrt/)     |                                                                                                 |
| [`min`](/ref/Field/min/)       |                                                                                                 |
| [`max`](/ref/Field/max/)       |                                                                                                 |
| [`gt`](/ref/Field/gt/)         | 1 where this is the larger, else 0.                                                             |
| [`lt`](/ref/Field/lt/)         | 1 where this is the smaller, else 0.                                                            |
| [`clamp`](/ref/Field/clamp/)   |                                                                                                 |
| [`smooth`](/ref/Field/smooth/) | 0 at `from`, 1 at `to`, smooth between. `from` may be the larger.                               |
| [`curve`](/ref/Field/curve/)   | Straight lines through `{ { input, output }, ... }`, inputs rising.                             |
| [`at`](/ref/Field/at/)         | This field read `dx, dy, dz` blocks away: `fields.water:at(1, 0, 0)` is the water east of here. |
