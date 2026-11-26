"""Build the FISSION (Fallout 1 numbering) versions of the Scrapheap demo scripts.

Sources: Et Tu's demo scripts + the mod author's JunkDemo.ssl, unchanged except for the
patches listed below. Headers: Et Tu's own headers, untouched; the Fallout 1 / FISSION
numbers come from scrapheap_fission.h, which every patched source includes after define.h.

usage: build_fission.py <ettu src dir> <ettu headers dir> <work dir> <sslc compile.exe>
"""
import os
import re
import shutil
import subprocess
import sys

src_in, hdr, work, sslc = sys.argv[1:5]
src_out = os.path.join(work, "src")
int_out = os.path.join(work, "int")
pp_out = os.path.join(work, "pp")
for d in (src_out, int_out, pp_out):
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)

# FISSION mod GVAR numbers: 4096 + djb2("scrapheap:<symbol lowercase>") % 4096
MOD_GVARS = [
    ("QUEST_GANG_WAR", 7789, 0, "Pip-Boy quest: 0 hidden, 1 active, 2 completed"),
    ("GANG_WAR_STATE", 4796, 0, "gang scripts' state flag: 0 quiet, 1 gangs gathering, 2 gangs leaving, 69 demo finished"),
    ("QUEST_FIX_POWER", 5754, 0, "Pip-Boy quest: 0 inactive, 1 active, 2 completed"),
    ("TOWN_REP_SCRAPHEAP", 6810, 0, "town reputation"),
    ("DOG_HIRED", 7387, 0, "the dog follows you"),
    ("GANG_1_FLAG", 4444, 0, "set by a citizen's line"),
    ("FOOLS_SCOUTED", 5263, 0, "player walked into the Fools' area"),
    ("CRYPTS_SCOUTED", 4785, 0, "player walked into the Crypts' area"),
    ("ETTU_OPTION_OFF", 5706, 0, "stands in for Et Tu option switches; always 0"),
    ("COMPUTER_FIXED", 5556, 0, "computer: was local variable 4"),
    ("COMPUTER_GAVE_XP", 5134, 0, "computer: was local variable 5"),
    ("GENERATOR_SCIENCE_CHECK", 5651, 0, "generator: was local variable 0"),
    ("GENERATOR_REPAIR_CHECK", 6076, 0, "generator: was local variable 1"),
]
NUM = {name: num for name, num, _, _ in MOD_GVARS}

# Et Tu name -> mod GVAR
REMAP = {
    "GVAR_QUEST_DEMO_GANG_WAR": "GANG_WAR_STATE",
    "GVAR_QUEST_DEMO_FIX_POWER": "QUEST_FIX_POWER",
    "GVAR_TOWN_REP_SCRAPHEAP": "TOWN_REP_SCRAPHEAP",
    "GVAR_DEMODOG_HIRELING_STATUS": "DOG_HIRED",
    "GVAR_GANG_1_GVAR": "GANG_1_FLAG",
    "GVAR_FSCOUT_1": "FOOLS_SCOUTED",
    "GVAR_CSCOUT_1": "CRYPTS_SCOUTED",
    "GVAR_ENABLE_DEBUG_MESSAGES": "ETTU_OPTION_OFF",
    "GVAR_ENABLE_FO2_SEASONAL_LIGHTING": "ETTU_OPTION_OFF",
}

header = [
    "/*",
    "   Scrapheap - FISSION (Fallout 1) numbers for the demo scripts.",
    "",
    "   Et Tu numbers every global variable differently from Fallout 1, so the demo",
    "   scripts must not use Et Tu's numbers when they run on FISSION. Every global",
    "   variable the demo scripts touch is redirected here to one of the mod's own",
    "   variables (data/gvar_scrapheap.txt). Include this right after define.h.",
    "*/",
    "",
    "#pragma once",
    "",
]
for ettu_name, sym in REMAP.items():
    header += [f"#undef  {ettu_name}", f"#define {ettu_name:38s} ({NUM[sym]})   // {sym}"]
header += [
    "",
    "// Pip-Boy entry for the gang war. The demo's own gang war variable is a state flag",
    "// that drops back to 0 when the fight starts, so it cannot drive the Pip-Boy itself.",
    f"#define GVAR_SCRAPHEAP_PIPBOY_GANG_WAR         ({NUM['QUEST_GANG_WAR']})",
    "",
    "// Computer and generator: Fallout 1 gives these two scripts no local variables,",
    "// so their four flags live in mod global variables instead.",
    f"#define GVAR_SCRAPHEAP_COMPUTER_FIXED          ({NUM['COMPUTER_FIXED']})",
    f"#define GVAR_SCRAPHEAP_COMPUTER_GAVE_XP        ({NUM['COMPUTER_GAVE_XP']})",
    f"#define GVAR_SCRAPHEAP_GENERATOR_SCIENCE_CHECK ({NUM['GENERATOR_SCIENCE_CHECK']})",
    f"#define GVAR_SCRAPHEAP_GENERATOR_REPAIR_CHECK  ({NUM['GENERATOR_REPAIR_CHECK']})",
    "",
]
with open(os.path.join(src_out, "scrapheap_fission.h"), "w", newline="\r\n") as f:
    f.write("\n".join(header))

# local variable renumbering: Fallout 1's scripts.lst gives these scripts 4 local variables
RENUMBER = {
    "LENNY": {"LVAR_Known": 2},
    "LEX": {"LVAR_Known": 0, "LVAR_Following": 1},
    "PEZ": {"LVAR_my_tile": 0},
    "PHRAX": {"LVAR_Once_Fool": 0, "LVAR_Once_Fridge": 1, "LVAR_Once_Generator": 2},
    "RAYZE": {"LVAR_Crypt_Liar": 0, "LVAR_Herebefore": 1},
    "ROCK": {"LVAR_Known": 0, "LVAR_Float": 1, "LVAR_Herebefore": 2},
    "SKIPPY": {"LVAR_Known": 0},
}
TO_GVAR = {
    "DEMOCOMP": {"LVAR_Fixed": "GVAR_SCRAPHEAP_COMPUTER_FIXED", "LVAR_GiveXP": "GVAR_SCRAPHEAP_COMPUTER_GAVE_XP"},
    "DEMOGEN": {"LVAR_Science_Check": "GVAR_SCRAPHEAP_GENERATOR_SCIENCE_CHECK", "LVAR_Repair_Check": "GVAR_SCRAPHEAP_GENERATOR_REPAIR_CHECK"},
}
GREETING = ("Amid endless sands, you come across an oasis of rust and scrap. "
            "The harsh glares from the gate guards hardly invite you to look any closer.")

log = []


def sub(text, pattern, repl, name, what, count=None, flags=0):
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n == 0 or (count is not None and n != count):
        raise SystemExit(f"PATCH FAILED in {name}: {what} matched {n} times (wanted {count or '1+'})")
    log.append(f"{name}: {what} ({n}x)")
    return new


names = sorted(f[:-4] for f in os.listdir(src_in) if f.lower().endswith(".ssl"))
names = [n for n in names if n.upper() != "SMELL"]   # Fallout 1 ships its own smell.int
for name in names:
    text = open(os.path.join(src_in, name + ".ssl"), encoding="latin-1", newline="").read()
    up = name.upper()
    text = sub(text, r'(#include "define\.h"[^\n]*\n)', r'\1#include "scrapheap_fission.h"\r\n', up,
               "include scrapheap_fission.h after define.h", 1)
    for lv, idx in RENUMBER.get(up, {}).items():
        text = sub(text, rf"(#define\s+{lv}\s+)\(\d+\)", rf"\g<1>({idx})", up, f"{lv} renumbered to {idx}", 1)
    for lv, gv in TO_GVAR.get(up, {}).items():
        text = sub(text, rf"#define\s+{lv}\s+\(\d+\)[^\n]*\n", "", up, f"{lv} define removed", 1)
        text = sub(text, rf"\bset_local_var\(\s*{lv}\s*,", f"set_global_var({gv},", up, f"set_local_var({lv}) -> set_global_var")
        text = sub(text, rf"\blocal_var\(\s*{lv}\s*\)", f"global_var({gv})", up, f"local_var({lv}) -> global_var")
        if re.search(rf"\b{lv}\b", text):
            raise SystemExit(f"{up}: {lv} still referenced after patch")
    if up == "DEMOGEN":
        text = sub(text, r"(display_msg\(mstr\(114\)\);)",
                   r"\1\r\n            set_global_var(GVAR_QUEST_DEMO_FIX_POWER, 2); // FISSION: Pip-Boy quest done",
                   up, "complete the generator quest when message 114 (generator fixed) shows", 1)
    if up == "JUNKDEMO":
        text = sub(text, r'display_msg\(message_str_game\(add_extra_msg_file\("SCRAPHEAP\.msg"\),\s*100\)\);',
                   f'display_msg("{GREETING}");\r\n'
                   '      set_global_var(GVAR_SCRAPHEAP_PIPBOY_GANG_WAR, 1); // FISSION: Pip-Boy quest on', up,
                   "greeting as plain text (FISSION has no add_extra_msg_file) + Pip-Boy gang war quest on", 1)
        text = sub(text, r"(set_fo1_demo_completed;)",
                   r"\1\r\n      set_global_var(GVAR_SCRAPHEAP_PIPBOY_GANG_WAR, 2); // FISSION: Pip-Boy quest done",
                   up, "Pip-Boy gang war quest done at both endings", 2)
    open(os.path.join(src_out, name + ".ssl"), "w", encoding="latin-1", newline="").write(text)

gl = """/*

   Scrapheap (FISSION build) - global script.

   Puts Necropolis and Scrapheap on their world map squares again every time a
   game loads and every time a map is entered, so saves made before the mod was
   installed pick the move up too. New games already get both positions from
   data/city_scrapheap.txt.

   The numbers are FISSION area slots (data/lists/area_list.txt):
   5 = 05_Necropolis, 3967 = SCRAPHEAP.

*/

procedure start;
procedure map_enter_p_proc;
procedure place_towns;

procedure place_towns begin
   wm_area_set_pos(5, 473, 622);
   wm_area_set_pos(3967, 1123, 672);
end

procedure start begin
   if (game_loaded) then begin
      set_global_script_type(0);
      call place_towns;
   end
end

procedure map_enter_p_proc begin
   call place_towns;
end
"""
open(os.path.join(src_out, "gl_scrapheap.ssl"), "w", newline="\r\n").write(gl)
names.append("gl_scrapheap")

failed = []
for name in names:
    for mode, out in (("-P", os.path.join(pp_out, name + ".pp")), (None, os.path.join(int_out, name + ".int"))):
        cmd = [sslc, "-q", "-l", "-p", "-s", "-O1", "-I" + hdr]
        if mode:
            cmd.append(mode)
        cmd += [name + ".ssl", "-o", out]
        p = subprocess.run(cmd, cwd=src_out, capture_output=True, text=True)
        txt = (p.stdout or "") + (p.stderr or "")
        bad = [l for l in txt.splitlines() if re.search(r"\[Error\]|error|warning", l, re.I)]
        if mode is None and (p.returncode != 0 or not os.path.isfile(out) or os.path.getsize(out) == 0 or bad):
            failed.append(name)
            print(f"--- {name}: rc={p.returncode}")
            print("\n".join(txt.splitlines()[-12:]))

print("\n".join(log))
print(f"\ncompiled {len(names) - len(failed)} of {len(names)}; failed: {failed}")
for f in sorted(os.listdir(int_out)):
    print(f"  {f:22s} {os.path.getsize(os.path.join(int_out, f))} bytes")
with open(os.path.join(work, "gvar_scrapheap.txt"), "w", newline="\r\n") as f:
    f.write("# Scrapheap - global variables (FISSION gives each one a fixed number, listed at the bottom)\n")
    for name, num, default, note in MOD_GVARS:
        f.write(f"{name} = {default}\n")
    f.write("\n# Numbers, for reference (data/lists/gvars_list.txt shows the same):\n")
    for name, num, default, note in MOD_GVARS:
        f.write(f"# {num}  {name:24s} {note}\n")
