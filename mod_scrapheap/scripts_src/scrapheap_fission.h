/*
   Scrapheap - FISSION (Fallout 1) numbers for the demo scripts.

   Et Tu numbers every global variable differently from Fallout 1, so the demo
   scripts must not use Et Tu's numbers when they run on FISSION. Every global
   variable the demo scripts touch is redirected here to one of the mod's own
   variables (data/gvar_scrapheap.txt). Include this right after define.h.
*/

#pragma once

#undef  GVAR_QUEST_DEMO_GANG_WAR
#define GVAR_QUEST_DEMO_GANG_WAR               (4796)   // GANG_WAR_STATE
#undef  GVAR_QUEST_DEMO_FIX_POWER
#define GVAR_QUEST_DEMO_FIX_POWER              (5754)   // QUEST_FIX_POWER
#undef  GVAR_TOWN_REP_SCRAPHEAP
#define GVAR_TOWN_REP_SCRAPHEAP                (6810)   // TOWN_REP_SCRAPHEAP
#undef  GVAR_DEMODOG_HIRELING_STATUS
#define GVAR_DEMODOG_HIRELING_STATUS           (7387)   // DOG_HIRED
#undef  GVAR_GANG_1_GVAR
#define GVAR_GANG_1_GVAR                       (4444)   // GANG_1_FLAG
#undef  GVAR_FSCOUT_1
#define GVAR_FSCOUT_1                          (5263)   // FOOLS_SCOUTED
#undef  GVAR_CSCOUT_1
#define GVAR_CSCOUT_1                          (4785)   // CRYPTS_SCOUTED
#undef  GVAR_ENABLE_DEBUG_MESSAGES
#define GVAR_ENABLE_DEBUG_MESSAGES             (5706)   // ETTU_OPTION_OFF
#undef  GVAR_ENABLE_FO2_SEASONAL_LIGHTING
#define GVAR_ENABLE_FO2_SEASONAL_LIGHTING      (5706)   // ETTU_OPTION_OFF

// Pip-Boy entry for the gang war. The demo's own gang war variable is a state flag
// that drops back to 0 when the fight starts, so it cannot drive the Pip-Boy itself.
#define GVAR_SCRAPHEAP_PIPBOY_GANG_WAR         (7789)

// Computer and generator: Fallout 1 gives these two scripts no local variables,
// so their four flags live in mod global variables instead.
#define GVAR_SCRAPHEAP_COMPUTER_FIXED          (5556)
#define GVAR_SCRAPHEAP_COMPUTER_GAVE_XP        (5134)
#define GVAR_SCRAPHEAP_GENERATOR_SCIENCE_CHECK (5651)
#define GVAR_SCRAPHEAP_GENERATOR_REPAIR_CHECK  (6076)
