# Scrapheap for FISSION and Et Tu: how it works and what was done

One folder, `mod_scrapheap.dat`, now holds both versions of the mod. FISSION reads the
files at the top of the folder. Et Tu reads only the `ettu\` folder inside it. Neither
game ever looks at the other's files, so nothing has to detect which game it is in.

**Status:** it loads cleanly in FISSION (checked in a test copy of Fallout 1), but
nobody has played it in either game yet. The checklist at the end says what still
needs a play-test.

## Install

**FISSION (Fallout 1)**

1. Put FISSION (`fallout-fission-x64.exe` and `fission.dat`) in a Fallout 1 folder, next to `MASTER.DAT`.
2. Copy the whole `mod_scrapheap.dat` folder into that folder's `mods\` folder.
3. Start the game, quit, and start it again. FISSION finds and switches on new mods by itself; the second start makes sure everything is loaded.

**Et Tu**

1. Copy the same `mod_scrapheap.dat` folder into Et Tu's `mods\` folder.
2. Open `mods\mods_order.txt` and add this line after `fo1_base`:

```
mod_scrapheap.dat\ettu
```

## What is in the folder

| Path | Read by | What it is |
| --- | --- | --- |
| `data\*_scrapheap.txt`, `data\mod_scrapheap.cfg` | FISSION | Town, map, quest, world map and variable definitions |
| `maps\JUNKDEMO.MAP`, `.GAM`, `.edg` | FISSION | Et Tu's copy of the Scrapheap map, its starting map variables, and its scroll edges |
| `data\MAPS\` | FISSION | A second copy of the same three map files (see "Open questions") |
| `scripts\*.int` | FISSION | 20 demo scripts and `gl_scrapheap`, compiled for Fallout 1's numbering |
| `scripts_src\` | nobody (reference) | Sources of those scripts, `scrapheap_fission.h`, and the build script |
| `text\english\dialog\*.msg` | FISSION | Dialogue for the demo characters (Et Tu's files) |
| `text\english\game\*_scrapheap.msg` | FISSION | Town name, entrance label, Pip-Boy quest text |
| `ettu\` | Et Tu | The Et Tu mod, version 0.2, unchanged |

## What was wrong

- **No way out of town.** The Scrapheap map inside Fallout 1's `MASTER.DAT` has no exit grids. Et Tu's copy adds 50 of them and moves some blockers so you can reach them.
- **17 script files missing.** The Fallout 1 map does have scripts assigned to its characters, but Fallout 1 never shipped the script files, so nothing in town did anything.
- **No map variables.** The demo scripts keep the gang and generator state in 19 map variables. Their starting values come from `JUNKDEMO.GAM`, which Fallout 1 does not have.
- **Et Tu's scripts cannot be copied over.** Et Tu numbers every global variable differently from Fallout 1 (none of Fallout 1's 618 match), so a script compiled for Et Tu reads and writes the wrong variables on FISSION.
- **Wrong area number.** `gl_scrapheap` moved Scrapheap using `881362`. The command needs the area slot, `3967`, so the move failed on every load.
- **The Pip-Boy quest was tied to the wrong variable.** The demo's "gang war" variable is a state flag for the gang scripts: 1 tells the gangs to gather, and it drops back to 0 when the fight starts. `gl_scrapheap` set it to 1 at the gate to show the quest, which would have started the war the moment you walked in.

## Every step taken

1. Unpacked both zips (the FISSION mod and Et Tu 0.2) and compared them file by file.
2. Downloaded the source code of FISSION and of Et Tu from GitHub, to read how each game loads mods, maps, scripts and variables.
3. Worked out the formulas FISSION uses for its numbers and checked them against the numbers already in the mod: area slot 3967, map 1236, and variables 7789 and 5754 all came out the same.
4. Found the wrong area number in `gl_scrapheap` (see above).
5. Pulled Fallout 1's script list and the Scrapheap map out of `MASTER.DAT`. The map uses 23 script slots; 17 of those script files do not exist in Fallout 1.
6. Compared the Fallout 1 map with Et Tu's. Et Tu's has 50 exit grids, different blockers, a scripted door, and cows that use `brahmin` instead of `cow`. Everything else is the same.
7. Checked that Et Tu's map can run on Fallout 1's data. All 2,003 objects use object and art numbers that mean the same thing in Fallout 1, the floor tiles are all within Fallout 1's list, and both games number scripts the same way. FISSION accepts Et Tu's map format (version 20).
8. Read how FISSION loads a map. The first time a map loads, it takes the map variables from `maps\<name>.GAM`. So shipping `JUNKDEMO.GAM` gives the scripts their 19 variables with the right starting values.
9. Compared Et Tu's global variable numbers with Fallout 1's. None match, so the scripts had to be recompiled for FISSION.
10. Ran every demo script through the compiler's preprocessor and listed what it really uses: 9 global variables, standard game commands, and `sprintf`. No other Et Tu features.
11. Compared each script's local variables with what Fallout 1's script list allows. Nine scripts used more than allowed, which would overwrite other scripts' variables.
12. Checked FISSION for the commands the map script needs. `set_exit_grids` and `sprintf` are there; `add_extra_msg_file` is not.
13. Read how the gang scripts use the "gang war" variable. It is a state flag, not a quest tracker (see "What was wrong"), so the Pip-Boy quest got a variable of its own.
14. Wrote `scrapheap_fission.h`, which points the 9 global variables at the mod's own variables, and patched the script sources (table below).
15. Compiled the 20 scripts and `gl_scrapheap` with the same compiler and settings Et Tu uses for its releases (`-q -l -p -s -O1`).
16. Compared each compiled script with Et Tu's own compiled copy. The ones with no logic changes are the same size byte for byte and differ only in the numbers that were meant to change.
17. Rewrote `gl_scrapheap` for FISSION: it uses slot 3967 and no longer touches the quests or shows the greeting.
18. Rebuilt `data\gvar_scrapheap.txt` with the 13 variables the scripts now use.
19. Put the folder together: FISSION files at the top, Et Tu 0.2 untouched in `ettu\`.
20. Cross-checked the finished folder: all 23 script slots the map uses are present (20 from the mod, 3 from Fallout 1), and all 421 dialogue lines the scripts ask for exist.
21. Read sfall's code for `mods_order.txt` to confirm a line may point at a folder inside another folder.
22. Made a test copy of Fallout 1, added FISSION and the mod, and started the game twice (closing it at the intro each time).
23. Read the reports FISSION wrote in `data\lists\` and its debug log. The mod was switched on automatically, Scrapheap is in slot 3967 at 1123,672, Necropolis is at 473,622, the map is 1236, and all 13 variables have the numbers listed below. No errors and no collision pop-ups.

## Script changes

Sources are Et Tu's demo scripts and the Et Tu mod's `JunkDemo.ssl`. Nothing else was changed.

| Script | Change | Why |
| --- | --- | --- |
| All 20 | Include `scrapheap_fission.h` after `define.h` | Use the mod's variables instead of Et Tu's numbers |
| `LENNY` | Local variable 4 becomes 2 | Fallout 1 gives the script 4 local variables (0 to 3) |
| `LEX`, `RAYZE` | Local variables 4, 5 become 0, 1 | Same |
| `PHRAX`, `ROCK` | Local variables 4, 5, 6 become 0, 1, 2 | Same |
| `PEZ`, `SKIPPY` | Local variable 4 becomes 0 | Same |
| `DEMOCOMP` | Its 2 local variables become mod global variables | Fallout 1 gives the script no local variables |
| `DEMOGEN` | Its 2 local variables become mod global variables | Same |
| `DEMOGEN` | Sets the generator quest to 2 when the "you fix the power generator" message shows | Nothing ever completed that quest (FISSION-only addition) |
| `JUNKDEMO` | Greeting is plain text in the script | FISSION has no `add_extra_msg_file` |
| `JUNKDEMO` | Switches the Pip-Boy gang war quest on at first entry, and marks it done at either ending | The Pip-Boy needs its own variable (FISSION-only addition) |
| `gl_scrapheap` | Rewritten (step 17) | Wrong area number; quest and greeting code removed |

`SMELL` was left out: Fallout 1 ships its own.

## Numbers

FISSION works these out from the mod's name and each entry's name, so they are the same on every PC. `data\lists\` in the game folder shows them after the game has run.

| Thing | Number |
| --- | --- |
| Scrapheap area slot | 3967 |
| Necropolis area slot | 5 |
| Scrapheap map | 1236 |

| Variable in `gvar_scrapheap.txt` | Number | Stands in for |
| --- | --- | --- |
| `QUEST_GANG_WAR` | 7789 | Nothing in Et Tu: the Pip-Boy entry (0 hidden, 1 active, 2 done) |
| `GANG_WAR_STATE` | 4796 | Et Tu's `GVAR_QUEST_DEMO_GANG_WAR` (0 quiet, 1 gangs gathering, 2 gangs leaving, 69 demo finished) |
| `QUEST_FIX_POWER` | 5754 | `GVAR_QUEST_DEMO_FIX_POWER` (0 off, 1 active, 2 done) |
| `TOWN_REP_SCRAPHEAP` | 6810 | `GVAR_TOWN_REP_SCRAPHEAP` |
| `DOG_HIRED` | 7387 | `GVAR_DEMODOG_HIRELING_STATUS` |
| `GANG_1_FLAG` | 4444 | `GVAR_GANG_1_GVAR` |
| `FOOLS_SCOUTED` | 5263 | `GVAR_FSCOUT_1` |
| `CRYPTS_SCOUTED` | 4785 | `GVAR_CSCOUT_1` |
| `ETTU_OPTION_OFF` | 5706 | Two Et Tu option switches; always 0 here |
| `COMPUTER_FIXED` | 5556 | Computer's local variable 4 |
| `COMPUTER_GAVE_XP` | 5134 | Computer's local variable 5 |
| `GENERATOR_SCIENCE_CHECK` | 5651 | Generator's local variable 0 |
| `GENERATOR_REPAIR_CHECK` | 6076 | Generator's local variable 1 |

## Keeping it up to date

- **The map changed in Et Tu.** Copy `JUNKDEMO.MAP`, `JUNKDEMO.GAM` and `JUNKDEMO.edg` to three places: `ettu\maps\`, `maps\` and `data\MAPS\`. If the map gained new kinds of objects or scripts, check they exist in Fallout 1 too.
- **Other Et Tu files changed.** Replace the contents of `ettu\` with the new Et Tu version. This build has 0.2 in it.
- **A demo script changed.** Rebuild the FISSION copies with `scripts_src\build_fission.py`. It applies every patch above and stops if one no longer fits:

```
python build_fission.py <folder with Et Tu's 99demo .ssl files plus JunkDemo.ssl saved as JUNKDEMO.ssl> <Et Tu's Mapper\source\scripts\headers> <empty work folder> <path to compile.exe>
```

  The compiled files land in `<work folder>\int`. Copy them to `scripts\`.

## Open questions

- **Not played yet.** FISSION was started in a test copy to confirm the mod loads (steps 22 and 23), but nothing was played, so the map, scripts and exit grids are untested in game. Et Tu was not run at all.
- **Slot or Area ID.** FISSION's area report says to use Scrapheap's "Area ID" (881362) in scripts. Its source code for `wm_area_set_pos` takes the slot (3967), which is what `gl_scrapheap` now uses. If Scrapheap does not move on an old save, check this first.
- **Two copies of the map for FISSION.** FISSION's source code looks for maps in `maps\` at the top of the mod. Its quick start guide says `data\MAPS\`. Both are filled in so it works either way; once tested, the unused copy can go.
- **The Et Tu part is 0.2.** Anything added to the Et Tu version after 0.2 is not in here.
- **Pip-Boy quests are a design choice.** Et Tu itself has no Pip-Boy entries for the demo. On FISSION, "Stop the gang war" appears the first time you enter town and is crossed off at either ending. "Repair the generator" appears when Lex or a citizen asks for it and is crossed off on the "you fix the power generator" message. Say if you want different triggers.
- **Not re-checked:** whether Scrapheap is hidden on the world map at the start, and the encounter changes in `worldmap_scrapheap.txt` (format checked only). Both are as they were in the FISSION mod.

## Play-test checklist

- [x] FISSION starts with no "collision" pop-ups, and `data\lists\area_list.txt` shows SCRAPHEAP in slot 3967 (done, step 23)
- [ ] Scrapheap is at 873,722, the Hub at 1123,672, and Necropolis at 473,622, on a new game and on an old save. Scrapheap stays unknown until you travel to it
- [ ] Entering Scrapheap shows the greeting once and puts "Stop the gang war" in the Pip-Boy
- [ ] The gangs do not start fighting just because you walked in
- [ ] Walking onto an exit grid at the edge of town returns you to the world map
- [ ] Lex, Baka, Rayze, Phrax, Rock, Skippy, Lenny, Skizzer and a citizen all talk, with no "Error" lines
- [ ] Either ending crosses "Stop the gang war" off in the Pip-Boy
- [ ] Cutting the generator wires with a Multi Tool shows the ending line
- [ ] The fridge, the computer, and the dog and Phil scene work
- [ ] Saving and loading inside Scrapheap keeps the gang and generator state
- [ ] Necropolis and Junktown still behave as normal
- [ ] Et Tu: the mod loads from the `mod_scrapheap.dat\ettu` line and plays as 0.2 did
