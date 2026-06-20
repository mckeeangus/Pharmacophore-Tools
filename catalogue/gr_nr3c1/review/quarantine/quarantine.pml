# quarantine — 1 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 8A9G_QJK_B303.mol2, 8A9G_QJK_B303
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
