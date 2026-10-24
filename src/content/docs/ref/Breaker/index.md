---
title: 'Breaker type'
description: 'What took a block out, and with what.'
---

What took a block out, and with what.

## Fields

| Field | Purpose |
| --- | --- |
| [`breaker.cause: "player" \| "fire" \| "explosion" \| "water" \| "support"`](/ref/Breaker/cause/) | What took the block out: a player, fire, an explosion, flowing water, or the loss of what held it up ("support"). |
| [`breaker.tool: string ?`](/ref/Breaker/tool/) | The item in hand, or nil for a bare hand and for the four causes that have none. |
| [`breaker.creative: boolean`](/ref/Breaker/creative/) | Whether a creative player broke it; creative takes the block and leaves nothing. False for the four causes with no player. |
