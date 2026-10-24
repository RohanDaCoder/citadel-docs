---
title: "Asks type"
description: "What the engine's questions with a deadline have cost this pack, in total and per kind: citadel.budget().asks."
---

What the engine's questions with a deadline have cost this pack, in total and per kind: `citadel.budget().asks`.

[`AskCount`](/ref/AskCount/)

## Fields

| Field                                                    | Purpose                                                               |
| -------------------------------------------------------- | --------------------------------------------------------------------- |
| [`asks.kinds: { [string]: AskCount }`](/ref/Asks/kinds/) | The same counters per kind of question, e.g. `kinds["break"].missed`. |
