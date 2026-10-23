---
title: "hub.experiences"
url: /docs/citadel/reference/hub/experiences
---

# hub.experiences

The portals of the experience grounds. `experience` is what `/play` takes.

```
hub.experiences() → { {slot: number, experience: string, title: string, pitch: string?, icon: string?, banner: string?, players: number?} }
```


## Returns


## Used in
- [`for _, e in hub.experiences() do print(e.slot, e.experience) end`Hub](/docs/citadel/hub)
- [`- `hub.experiences()` returns a list of `{slot, experience, title, pitch, icon, banner, players}`. `experience` is the name `/play` takes. A slot that is not in the list has no experience.`Hub](/docs/citadel/hub)
