---
title: "network.start"
url: /docs/citadel/reference/network/start
---

# network.start

Starts an instance of `member`. Answers at once; it is online later.

```
network.start(options: {member: string, label: string, slots: number, data: any}) → (NetworkStarted?, string?)
```


## Parameters


## Returns


## Used in
- [`- `network.start{ member, label, slots, data? }` starts an instance of `member`. It returns `{id, state}` at once, with `state = "starting"`: the instance comes online later. `slots` is the number of players the instance takes. `data` is the pack's own value for the instance, read there with `network.info()`.`Network](/docs/citadel/network)
