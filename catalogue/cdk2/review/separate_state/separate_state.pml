# separate_state — 3 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 2CCH_ATP_C1297.mol2, 2CCH_ATP_C1297
load 4EOJ_ATP_A301.mol2, 4EOJ_ATP_A301
load 8FP5_ATP_A302.mol2, 8FP5_ATP_A302
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
