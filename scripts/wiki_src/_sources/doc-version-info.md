# SOURCE: Version info

```luau
citadel.log("anything", 42)    -- to the server log, under this pack's name
citadel.version    -- the engine version
citadel.game    -- the game version from citadel.yml, "1.8.9"
citadel.env    -- "development", "unlisted" or "published"
citadel.budget()    -- this pack's slice of a tick, and what it did with it
citadel.on_slow(function(slow) end)    -- a batch that ran out of budget; see "Limits and reload"
```
`citadel.version` is the engine build (`0.1.0`).
`citadel.env` is:
- `"development"` on the Minefort workload where an experience is built.
- `"unlisted"` or `"published"` on an experience’s instances, by visibility.
- `"published"` on a Minefort server that is not an experience.
- `"development"` anywhere else.
Gate debug tools on it:
```luau
if citadel.env == "development" then
    -- builder-only commands, verbose logs, …
end
```
Build mode (`/build`, `/part`; see “Named parts”) exists on `"development"` only.
