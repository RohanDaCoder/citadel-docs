---
title: "TimeName type"
description: "A named time of day that world.time holds the sky at: sunrise, day, noon, sunset, night or midnight."
---

A named time of day that `world.time` holds the sky at: sunrise, day, noon, sunset, night or midnight.

`"sunrise"` | `"day"` | `"noon"` | `"sunset"` | `"night"` | `"midnight" x: number, y: number, z: number, magnitude: (self: Vec3) -> number, unit: (self: Vec3) -> Vec3, dot: (self: Vec3, other: Vec3) -> number, cross: (self: Vec3, other: Vec3) -> Vec3, distance: (self: Vec3, other: Vec3) -> number, lerp: (self: Vec3, other: Vec3, t: number) -> Vec3, floor: (self: Vec3) -> Vec3, with: (self: Vec3, fields: { x: number ?, y: number ?, z: number ? }) -> Vec3,`
