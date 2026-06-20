# quarantine — 2 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 5EK0_5P2_A1808.mol2, 5EK0_5P2_A1808
load 8I5G_T70_A2005.mol2, 8I5G_T70_A2005
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
