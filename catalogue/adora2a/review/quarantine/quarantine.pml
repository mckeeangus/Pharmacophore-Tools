# quarantine — 2 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 8PWN_TEP_A500.mol2, 8PWN_TEP_A500
load 9T9P_ZMA_B901.mol2, 9T9P_ZMA_B901
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
