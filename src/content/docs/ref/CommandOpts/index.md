---
title: 'CommandOpts type'
description: 'The options of commands.add: a permission node, aliases, the /help line and suggestions per argument.'
---

The options of `commands.add`: a permission node, aliases, the /help line and suggestions per argument.

## Fields

| Field | Purpose |
| --- | --- |
| [`commandOpts.permission: string ?`](/ref/CommandOpts/permission/) | A permission node; without it the command is not shown and not run. |
| [`commandOpts.aliases: { string }?`](/ref/CommandOpts/aliases/) | More names for the same command: { "hub", "lobby" }. |
| [`commandOpts.help: string ?`](/ref/CommandOpts/help/) | The line /help shows after the usage. |
| [`commandOpts.suggest: { [string]: { Suggestion } \| Suggester }?`](/ref/CommandOpts/suggest/) | Per argument name: the words to offer, or a function that returns them. |
