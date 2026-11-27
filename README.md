# Scrapheap

Adds Scrapheap, the town from the Fallout 1 demo, as a world map location. Scrapheap takes the Hub's old square,, the Hub takes Necropolis' old square, and Necropolis moves southwest of Lost Hills.

This one folder works in both **FISSION** (running Fallout 1) and **Fallout Et Tu**.

## Install

**FISSION:** copy the `mod_scrapheap.dat` folder into the game's `mods\` folder, then
start the game twice. FISSION switches new mods on by itself.

**Et Tu:** copy the same folder into Et Tu's `mods\` folder, then add this line to
`mods\mods_order.txt`, after `fo1_base`:

```
mod_scrapheap.dat\ettu
```

In the game's `ddraw.ini` (the one next to the Et Tu executable, not the copy
inside this mod), set `WorldMapSlots=13`. sfall reads that file only. 13 fits
the existing location-tab art.

Keep the folder name exactly as it is. FISSION only loads folders named `mod_<name>.dat`.

## Credits

- Uncle Phosgene (NMA): Inspired concept
- Golbolco: Lead designer and programmer
- Hoglord: Programming assistance for rebuilding the mod in FISSION
- Nonebit: Playtester
- Pax Venire: Playtester
- Hrudgar: Playtester
- Cambragol: Provided new Scrapheap nameplate art

