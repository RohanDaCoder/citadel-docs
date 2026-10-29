---
title: Server settings
section: systems
order: 8
description: The server's citadel.yml — mode, packs, the bind addresses for Java, resource packs, Bedrock RakNet and NetherNet, game, world_dir, operators, online_mode, nethernet_tls and store_dir; the mode decision order and how a player's identity is decided.
tags:
  [citadel.yml, configuration, mode, bind, operators, online_mode, min_client]
---

# Server settings

> **In short:** beside the server runs a `citadel.yml` — the server's own
> configuration, separate from a pack's manifest. It picks the mode, where
> the packs and the world live, what to listen on, the operators and how a
> player's identity is checked. Every key is optional; an unknown key stops
> the server. This page is the key table and the two decisions the file
> makes: the mode, and identity.

## The file

```yaml
# citadel.yml
mode: lite # "full" = Citadel plays the game, "lite" = the packs are the game
packs: packs # where the packs are, relative to this folder
bind: # what to listen on; each line left out is this default
  java: 0.0.0.0:25565
  packs: 0.0.0.0:25566 # resource packs over HTTP; give a second server on one machine its own
  bedrock: 0.0.0.0:19132 # Bedrock over RakNet (UDP); "" turns it off
  nethernet: 0.0.0.0:19132 # Bedrock over NetherNet (TCP signaling, the same number as RakNet on UDP); "" turns it off
game: a0.1.0 # the game version, "1.8.9" (the default) or "a0.1.0"
world_dir: worlds/a0 # the world folder; a world keeps the game it was written by
operators: # players with every permission, by uuid (Minefort writes the owner here)
  - 069a79f4-44e9-4726-a5be-fca90e38aaf5
online_mode: true # check each player with Mojang, as vanilla does; this is the default
nethernet_tls: # the certificate for Bedrock clients that dial HTTPS; not used behind a proxy with a forwarding secret
  cert: fullchain.pem
  key: privkey.pem
store_dir: data/store # where `stores` keeps its files when no platform store was named; this is the default
```

## The keys

| Key                           | Default in the block above | Meaning                                                                                      |
| ----------------------------- | -------------------------- | -------------------------------------------------------------------------------------------- |
| `mode`                        | —                          | `"full"` = Citadel plays the game, `"lite"` = the packs are the game.                        |
| `packs`                       | `packs`                    | Where the packs are, relative to this folder.                                                |
| `bind.java`                   | `0.0.0.0:25565`            | The Java listeners' address and port.                                                        |
| `bind.packs`                  | `0.0.0.0:25566`            | Resource packs over HTTP.                                                                    |
| `bind.bedrock`                | `0.0.0.0:19132`            | Bedrock over RakNet (UDP); `""` turns it off.                                                |
| `bind.nethernet`              | `0.0.0.0:19132`            | Bedrock over NetherNet (TCP signaling, the same number as RakNet on UDP); `""` turns it off. |
| `game`                        | `1.8.9`                    | The game version: `"1.8.9"` (the default) or `"a0.1.0"`.                                     |
| `world_dir`                   | —                          | The world folder; a world keeps the game it was written by.                                  |
| `operators`                   | —                          | Players with every permission, by uuid; Minefort writes the owner here.                      |
| `online_mode`                 | `true`                     | Check each player with Mojang, as vanilla does.                                              |
| `nethernet_tls.cert` / `.key` | —                          | The certificate for Bedrock clients that dial HTTPS.                                         |
| `store_dir`                   | `data/store`               | Where `stores` keeps its files when no platform store was named.                             |
| `min_client`                  | —                          | Refuses old clients (see [Client versions](/appendix/client-versions)).                      |

Every key is optional, and so is the file. With no `packs` key, a `packs`
folder beside the world is used when one exists. **An unknown key or mode
stops the server.**

> **Gotcha:** `bind.packs` is its own listener. Give a second server on one
> machine its own `bind.packs` port — two servers cannot serve resource packs
> on the same address.

A pack has its own `citadel.yml` manifest — `entry`, `world`, `spawn_point`
and the rest — documented in [Pack anatomy](/wiki/pack-anatomy); the world
keys are covered in [Terrain generation](/wiki/terrain-generation).

## The mode decision order

The mode is decided in this order:

1. A `--full` or `--lite` flag.
2. This file.
3. What the packs agree on in their own manifests.
4. Survival, when there are no packs.

A flag or the server file overrules a pack that names the other mode.

## A player's identity

A player's identity comes from one of three places:

| Where                                          | Who vouches for the name    |
| ---------------------------------------------- | --------------------------- |
| Behind a proxy with `MODERN_FORWARDING_SECRET` | The proxy signs it.         |
| No proxy, `online_mode: true`                  | Citadel checks with Mojang. |
| `online_mode: false`                           | Nobody is checked.          |

> **Gotcha:** with `online_mode: false`, **anyone can join with any name, an
> operator's too** — and the log warns at start.

## Where the store lives

`store_dir` names where `stores` keeps its files when no platform store was
named — `data/store` by default. Two servers on one laptop need two
directories. See [Shared stores](/wiki/shared-stores#where-the-data-lives-without-a-socket).

## Old clients

Features differ by client: guard a version-gated call with
`player:supports(...)` and offer something else when it answers false — the
full feature table is in [Client versions](/appendix/client-versions). Or set
`min_client` in citadel.yml to refuse old clients.

## See also

- [Pack anatomy](/wiki/pack-anatomy) — the pack's own `citadel.yml` manifest
  and the load limits.
- [Shared stores](/wiki/shared-stores) — what `store_dir` moves.
- [Client versions](/appendix/client-versions) — `player:supports` and the
  full feature table.
- [What is Citadel](/wiki/what-is-citadel) — lite, full and plugin modes.
