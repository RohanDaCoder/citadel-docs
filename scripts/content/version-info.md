---
title: "Version info"
url: /docs/citadel/version-info
---

# Version info

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
