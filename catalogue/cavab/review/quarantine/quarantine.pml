# quarantine — 1 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 6JUH_G3P_C1305.mol2, 6JUH_G3P_C1305
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
