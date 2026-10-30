# Onix Minigames — the Citadel port

The live Paper/Purpur server (`OnixMinigames`, onixminigames.minefort.com,
Paper 1.21.11) was the source of truth, read through the Minefort MCP on
2026-10-30: every Skript under `plugins/Skript/scripts`, the six FAWE
schematics under `plugins/FastAsyncWorldEdit/schematics`, the LuckPerms
prefix export, the LPC/TAB/Essentials/DiscordSRV configs and
`server.properties`. The original Skript lives on in `reference/` with the
configs it ran against; `pack/` is the Citadel pack this produced, deployed
on the Citadel workload `onixmg` (onixmg.minefort.com).

## What maps to what

| Live server | Citadel pack |
| --- | --- |
| `Core/0_Variables.sk` (prefixes, perms, game list) | `core.luau` prefix runs, permission nodes, `core.register` |
| `Core/1_CoreSystem.sk` (cycle, votes, rounds) | `core.luau` `run`/`play`/`finish`/`eliminate` |
| `Commands/1_GameCommands.sk` | `main.luau` commands, `menus.luau` map picker |
| `Games/1_Spleef.sk` … `4_Sumo.sk` | `games/*.luau` |
| `Utils/1_Spawn.sk` (spawn/center/join/respawn) | `main.luau` + `arena.luau` |
| `Utils/2_Discord.sk` (/discord + 2-min broadcast) | `main.luau` + `core.discord_broadcast` |
| `/si give spleef_shovel` / `hotpotato` items | hotbar items (`golden_shovel`, `baked_potato`) |
| `paste schematic "OnixMG_state_*.schem" at (-47,-20,38)` | `arena.show(name)` pasting the same `.schem` at its own `Offset + SHIFT` |
| LPC chat format `{prefix}{name}: {message}` | `players.on_chat` in `main.luau`, returning false |
| LuckPerms owner tag `&8[gradient ᴏᴡɴᴇʀ] ` | `owner_tag()` runs, letter-for-letter colours |
| TAB header/footer (animated logo, ᴏɴʟɪɴᴇ footer) | `set_tab()` + the 3-second frame loop |
| Essentials `motd.txt` (the four gold welcome lines) | `essentials_motd()` on join |
| vanilla `/list` | a pack `/list` |
| `server.properties` MOTD (`» Onix Minigames «`) | the workload MOTD (update-workload) |
| map-state chest GUI (slots 10/12/14/16/28 + barriers) | `menus.map_states`, same slots, same items |
| `ItemTag` red-dye "Shutdown" lobby item | not carried (a physical world item, not Skript) |

## Message parity

Every chat line, title, action bar and sound is the Skript's own, in the
Skript's own colours — including the two-tone and three-tone ones
(`&e%name% &cwas eliminated from the game!`, `&c&lBOOM! &e%name%
&7exploded!`, the gold/bold game headers, the winner line, the vote
broadcast with its `[VOTE]` token, the vote-phase and start-phase action
bars, `&7Server is in &e%state%&7 state.`, `&e%player% &7skipped waiting
time.`, `&7System shutdown!`, `&7Returning to lobby...`, `&c&lThe game
has ended!` and its trailing blank line). The prefix is
`<#7A8BFA><b>Onix<#204352><b>MG <#555555>|` as exact colour runs;
`sendDebug` is `<#aa0000><b>ᴅᴇʙᴜɢ <#555555>|<reset>` with the same glyphs.

Skript's `volume 10` is Citadel's full volume (1). `/vote`, `/startgame`
and `/stopgame` keep their live cooldowns (none / 2 s / 2 s); `/spawn`
keeps its 3 seconds and its remaining-time message; `/center` keeps its
tab completions (0/90/180/-90 and 0/90/-90).

## Where the vote went

`0_Variables.sk` on the live server adds only **Spleef** and **TNT Run**
to `{minigames::list::*}` — Sumo and Hot Potato are the commented-out line
right under it. The port keeps all four games registered and running, but
the vote list is the live server's two, with the same shape as the
commented Skript: `votable = false` on `sumo` and `hotpotato` in
`games/*.luau`. Flip that flag to put a game back in the vote.

## The maps

The six schematics are the live server's own files, byte for byte,
downloaded from its FAWE folder. The live paste (Fawesk at
`(-47, -20, 38)`) reproduces each map at its `Offset`, so the port pastes
at `Offset + SHIFT` with `SHIFT = (5, 117, -35)`, lifting the old world's
`y -53..-9` into Citadel's range.

Every spawn point is the live Skript's own coordinate, kept exactly and
lifted by the same SHIFT. Each point sits *inside* its map's invisible
light pillar — a column of `light[level=15]` blocks standing over the
arena floor — so a teleported player falls to the floor and takes the
game's own fall damage, exactly as on Paper:

| map | live point (1_Spawn.sk / 1_CoreSystem.sk) | in Citadel | fall | damage |
| --- | --- | --- | --- | --- |
| lobby | (-46.5, -18, 38.5), yaw -90 | (-41.5, 99, 3.5) | 2 | none |
| spleef | (1.5, -20, 35.5), yaw 90 | (6.5, 97, 0.5) | 11 | 8 |
| tntrun | (-23.5, -20, 38.5), yaw 90 | (-18.5, 97, 3.5) | 12 | 9 |
| hotpotato | (1.5, -20, 35.5), yaw 90 | (6.5, 97, 0.5) | 30 | 27 (lethal) |
| sumo | (4.5, -15, 33.5), yaw 90 | (9.5, 102, -1.5) | 8 | 5 |

Hot Potato's spawn drop is lethal at full health — it was on Paper too,
which is presumably why that game was `votable = false` there. Respawn
follows 1_Spawn.sk verbatim (`on respawn → spawn(player)`): always the
lobby point, never a re-drop into an arena. `main.luau` logs what the
world really holds at the exact lobby point (and whether the engine's
`light` block is solid) the first time a join loads its chunk — a
registry remap would show in the console, not in play.

The void check is the Skript's `y < -48`, lifted with the same SHIFT
(`arena.VOID_Y = 69`), for the three games that had one. Hot Potato never
had a `y`-check on the live server — its floor sits *below* the other
games' kill line — so it keeps none.

The `game: "1.12.2"` registry was probe-verified (2026-10-30) to know all
64 block names the maps use, pale oak, froglight, tuff bricks and blue ice
included, so nothing is remapped.

## Deliberate deviations — all because the live Skript was broken

1. **Quitting mid-round.** The Skript's `on disconnect: mg_eliminate({_p})`
   passed an unset variable, so its guard stopped the function and a
   quitter was never removed — the roster kept ghosts that could win. The
   port runs the full elimination (broadcast, lava sound, roster removal).
2. **Hot Potato's fuse.** The Skript's `while {timer} <= 0` could never
   run: the potato was taken back the second it was given and the BOOM
   never fired. The port plays the obvious intent — a 30 s fuse, the
   explode sound, `BOOM! %name% exploded!`, the holder eliminated, a new
   random holder. The pass direction is the live one: the holder's hits
   are cancelled, and anyone else hitting a player passes the potato to
   the victim.
3. **The winner.** mg_end_game's `else if {_w} is not set: first element`
   always fires (the `else` picking a random player is dead code), so the
   live winner is the first roster player left standing, and an empty
   roster prints `&8[&7Nobody&8]` as the winner. Both are kept. The port's
   old random-winner and draw inventions are gone.
4. **/startgame near the end of a vote.** Live set the timer to 5 even
   from 3, extending the wait; the port only ever cuts time short.
5. **/stopgame's restart.** Live deleted `{minigames::*}`, leaving the
   system dead until a script reload. The port's `/startgame` (and the
   panel button) can start it again.
6. **Mid-game map pastes.** Live let `/changemapstate` paste a map under
   a running round, stranding the arena. The port refuses during Ingame.
7. **Damage.** The old code refused all out-of-game damage and sumo's
   knockback was a script push; the port answers only Hot Potato's
   holder question and leaves the rest to the engine, as the live server
   did.
8. **Additions the live Skript never had:** the sidebar, the vote compass
   and profile hotbar items, the profile and admin panel (those two come
   from the repo's `legacy` branch, `Commands/2_Profile.sk` and
   `3_AdminPanel.sk`, which the live server did not run), per-player stats
   in storage, and the lobby re-paste tasks are absent — no world reads
   happen at boot at all. The hotbar, the sidebar and `/list` exist
   because Citadel chat cannot click; the address is the message for
   `/discord` because it cannot open URLs either.

## Deploying

`scripts/push_onix_citadel.sh` pushes `pack/` to the `citadel` branch of
RohanDaCoder/OnixMinigames. The deploy key lives in `.secrets/`
(`gen_deploy_key.py onix_repo`), is mirrored into the main repo's
`.git/config` (`sync.onixrepokey`) against container recycles, and must be
registered on GitHub with write access. After a code change, upload with
`scripts/onix_fetch.py upload <workload> <local> <remote>` — the running
pack hot-reloads each file.

The Paper reference server holds the canon: `reference/skript` (the nine
`.sk` files), `reference/configs` (plugins, MOTD, the LuckPerms export),
`reference/fawe` (the schematics) and `reference/configs/latest.log`.
