# SOURCE: Armour

```luau
player:wear{ head = "iron_helmet", chest = { item = "leather_chestplate", dye = colors.blue },
             legs = "chainmail_leggings", feet = "golden_boots" }
player:wear{ head = "carved_pumpkin" }   -- replaces all four: the three left out are bare
player:wear{}                            -- all off
npc:wear{ chest = "diamond_chestplate" } -- the same on an npc
```

`wear` fills the armour slots of a player or an npc. Each piece is an item (see “items”), so `dye` and `glint` work.

- The inventory, the body and the armour bar show the pieces. Armour does not reduce damage yet.
- Nearby clients draw the pieces from 1.8.
- Any item goes on the head. Other slots draw only armour made for them.
- On a pack server, only the pack takes armour off.
- On a survival server, these are the real armour slots. `wear` replaces their contents, and the player can take pieces off.
