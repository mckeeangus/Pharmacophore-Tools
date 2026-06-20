# quarantine — 2 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 9FR2_A1IE9_A301.mol2, 9FR2_A1IE9_A301
load 4EOJ_SGM_B502.mol2, 4EOJ_SGM_B502
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
