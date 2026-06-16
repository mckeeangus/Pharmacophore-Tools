# representative — 4 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 5KMF_6U9_A1301.mol2, 5KMF_6U9_A1301
load 6KE5_6UB_B1301.mol2, 6KE5_6UB_B1301
load 5KLS_6UC_C1304.mol2, 5KLS_6UC_C1304
load 6JUH_G3P_C1305.mol2, 6JUH_G3P_C1305
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
