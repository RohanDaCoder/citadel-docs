---
title: 'TextRuns type'
description: 'Words wherever the API shows them: a string, or a table of runs'
---

Words wherever the API shows them: a string, or a table of runs. A table's entries are its runs in order (each a string or another table), and its named fields are the style of all of them; a run that names its own style keeps it. See "text" in docs/luau-api.md.

## Fields

| Field | Purpose |
| --- | --- |
| [`textRuns.color: Ink ?`](/ref/TextRuns/color/) | The colour of every run that does not pick its own: a colour value, a name or hex. |
| [`textRuns.bold: boolean ?`](/ref/TextRuns/bold/) | Bold for every run that does not say otherwise. |
| [`textRuns.italic: boolean ?`](/ref/TextRuns/italic/) | Italic for every run that does not say otherwise. |
| [`textRuns.underline: boolean ?`](/ref/TextRuns/underline/) | Underlined for every run that does not say otherwise. |
| [`textRuns.strike: boolean ?`](/ref/TextRuns/strike/) | Struck through for every run that does not say otherwise. |
| [`textRuns.effect: Effect ?`](/ref/TextRuns/effect/) | Called for every letter, every frame the text is on screen: hands back how that letter looks, or nil to leave it. |
