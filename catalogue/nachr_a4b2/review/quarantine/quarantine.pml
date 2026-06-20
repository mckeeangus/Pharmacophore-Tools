# quarantine — 1 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 2YME_CWB_J1207.mol2, 2YME_CWB_J1207
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
