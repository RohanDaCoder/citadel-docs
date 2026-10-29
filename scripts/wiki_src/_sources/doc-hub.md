# SOURCE: Hub

```luau
task.spawn(function()
    for _, s in network.browse('featured') or {} do print(s.name, s.players) end
    for _, e in hub.experiences() do print(e.slot, e.experience) end
    for _, h in network.instances() or {} do print(h.name, h.players) end
    print(network.online())
end)
```
- `hub.role(player)` returns the player’s rank on Minefort: `"owner"`, `"admin"`, `"moderator"` or `"builder"`, and nil for everyone else. It also takes a uuid, with or without dashes.
- Minefort sends the ranks every minute. Anywhere but a hub, they are nil.
- `hub.role(player)` returns the player’s rank on Minefort: `"owner"`, `"admin"`, `"moderator"` or `"builder"`, and nil for everyone else. It also takes a uuid, with or without dashes. Minefort sends the list every minute, so a new rank reaches the hub within one. Anywhere but a hub, it is nil.
- `hub.experiences()` returns a list of `{slot, experience, title, pitch, icon, banner, players}`. `experience` is the name `/play` takes. A slot that is not in the list has no experience.
- A `banner` is a 1024×512 PNG its creator uploaded and Minefort checked: 8 by 4 maps. Read it with `http.get(banner, { cache = 86400 }):image()`; a new banner has a new URL, so the cache never shows an old one.
- `hub.rent(player, slot, product, experience)` offers a portal of the grounds for Gems, like `shop.prompt`: `product` is one of the hub’s rentals, such as `portal_24h`, and `experience` the name `/play` takes of any published experience, which the portal then leads to. It returns a request id, or nil; `shop.on_paid` hands the purchase over. Renting your own portal again adds time, and may leave `experience` out to keep what it shows.
- `hub.point(player, slot, experience)` turns the player’s own live portal to another published experience, as often as they like. It returns whether it did.
- Minefort decides who may rent or point what: a stand someone else holds, or a name that is no published experience, is a no. Anywhere but its hub, every answer is no.
- Minefort keeps the lists up to date. The first call of `experiences` waits at most two seconds for them, so call it from a task.
