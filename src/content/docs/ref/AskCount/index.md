---
title: "AskCount type"
description: "What one kind of ask has cost this pack, and what every kind has together"
---

What one kind of ask has cost this pack, and what every kind has together. An ask is a question the engine puts to a pack with a deadline on it; an answer that does not arrive in time is not used.

## Fields

| Field                                                   | Purpose                                                             |
| ------------------------------------------------------- | ------------------------------------------------------------------- |
| [`askCount.asks: number`](/ref/AskCount/asks/)          | Questions the engine put to this pack.                              |
| [`askCount.answered: number`](/ref/AskCount/answered/)  | Answers that arrived in time.                                       |
| [`askCount.missed: number`](/ref/AskCount/missed/)      | Deadlines that passed with no answer.                               |
| [`askCount.late: number`](/ref/AskCount/late/)          | Answers that arrived after the engine had acted, and were dropped.  |
| [`askCount.skipped: number`](/ref/AskCount/skipped/)    | Asks never sent, because this kind is switched off for this pack.   |
| [`askCount.disabled: boolean`](/ref/AskCount/disabled/) | True once the engine has stopped asking this pack this kind at all. |
