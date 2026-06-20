# representative — 5 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 7W9K_9Z9_A2006.mol2, 7W9K_9Z9_A2006
load 8THH_IYJ_A2004.mol2, 8THH_IYJ_A2004
load 8S9B_LQO_A2003.mol2, 8S9B_LQO_A2003
load 8S9C_N6W_A2003.mol2, 8S9C_N6W_A2003
load 8I5B_OJ0_A2021.mol2, 8I5B_OJ0_A2021
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
