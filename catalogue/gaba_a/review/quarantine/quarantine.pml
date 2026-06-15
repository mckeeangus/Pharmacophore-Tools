# quarantine — 1 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 7QND_EI7_E501.mol2, 7QND_EI7_E501
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
