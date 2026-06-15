# quarantine — 1 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 6YZT_Q3E_A302.mol2, 6YZT_Q3E_A302
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
