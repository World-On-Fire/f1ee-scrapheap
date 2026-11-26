## Fallout 1 Scrapheap

Adds Scrapheap, the town from the Fallout 1 demo, as a world map location. Scrapheap is placed on the Hub's old square, the Hub is moved to Necropolis's old square, and Necropolis is moved southwest of Lost Hills. Scrapheap stays unknown until you travel to it. Leaving Scrapheap returns you to the world map.

### Features

- [x] Scrapheap on world map
- [x] Necropolis moved to lore-accurate position
- [x] Encounter tables flipped
- [x] Demo behavior from Et Tu overridden
- [x] Fallbacks in place for motorcycle behavior from Et Tu
- [ ] Art assets for Scrapheap town map/button selector
- [ ] Art assets for world map change

### Installation

To use this mod, add the mod folder name to the mods_order.txt file inside the /mods/ directory. If the mods_order.txt doesn't exist, start the game once for it to be created. List it after `fo1_base`.

Set `WorldMapSlots=13` in the game's `ddraw.ini`, next to the Et Tu executable. sfall does not read `ettu/ddraw.ini`. The stock setting is 12, one slot for each vanilla town, so Scrapheap is left off the location list. 13 still uses the stock tab art.