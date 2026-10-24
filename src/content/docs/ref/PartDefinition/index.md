---
title: "PartDefinition type"
description: "A named part of a stored world (world: <folder>) and the generator that writes it"
---

A named part of a stored world (`world: <folder>`) and the generator that writes it. Declared, not run: `citadel generate <pack> --part <name>`, or `/part generate <name>` in build mode, runs it; a changed file runs it again while nobody has edited the part. See "parts" in docs/luau-api.md.

## Functions

| Call                                  | Purpose                         |
| ------------------------------------- | ------------------------------- |
| [`build`](/ref/PartDefinition/build/) | Exactly a world.build function. |

## Fields

| Field                                                            | Purpose                                                           |
| ---------------------------------------------------------------- | ----------------------------------------------------------------- |
| [`partDefinition.name: string`](/ref/PartDefinition/name/)       | Unique; a path, "downtown/tower-3", nests.                        |
| [`partDefinition.at: Vec3`](/ref/PartDefinition/at/)             | Where the build's block (0, 0, 0) lands.                          |
| [`partDefinition.detail: number ?`](/ref/PartDefinition/detail/) | 1 (whole blocks, the default) or 2 (half blocks), as world.build. |
