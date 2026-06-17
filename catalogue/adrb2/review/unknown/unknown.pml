# unknown — 3 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 9I52_A1IZU_R501.mol2, 9I52_A1IZU_R501
load 9I54_A1IZV_R501.mol2, 9I54_A1IZV_R501
load 9U9V_B40_R401.mol2, 9U9V_B40_R401
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
