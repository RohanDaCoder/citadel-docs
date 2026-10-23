---
title: "network.list"
url: /docs/citadel/reference/network/list
---

# network.list

The network's instances, or only those with `label`.

```
network.list(label: string?) → ({NetworkInstance}, string?)
```


## Parameters


## Returns


## Used in
- [`- `network.list(label?)` returns a list of the network's instances. Each one is the instance table below.`Network](/docs/citadel/network)
- [`**Events come to the default member's servers only.** Call `network.list()` once at the start, then keep the list from `on_instance` and `on_gone`. An event can be lost. Call `network.list()` again, once a minute at most, to repair the list.`Network](/docs/citadel/network)
