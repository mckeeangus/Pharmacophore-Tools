# separate_state — 2 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 6KLZ_BCT_A303.mol2, 6KLZ_BCT_A303
load 5Y2S_CO2_A302.mol2, 5Y2S_CO2_A302
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
