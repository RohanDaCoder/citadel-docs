---
title: 'Screen type'
description: 'A wall or floor of map frames showing a picture, from world.screen; it draws like a canvas and can answer clicks by pixel.'
---

A wall or floor of map frames showing a picture, from `world.screen`; it draws like a canvas and can answer clicks by pixel.

[`Picture`](/ref/Picture/)

## Functions

| Call | Purpose |
| --- | --- |
| [`on_click`](/ref/Screen/on_click/) | Called with the pixel the player points at and the button, when a player clicks the screen. nil or false takes the hook off. |
| [`view`](/ref/Screen/view/) | Returns this player's own layer over the screen; only they see it, and the shared picture shows where it is see-through. |
| [`destroy`](/ref/Screen/destroy/) | Removes the screen. |
