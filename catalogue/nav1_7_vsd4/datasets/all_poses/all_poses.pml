# all_poses — 5 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 5EK0_5P2_A1808.mol2, 5EK0_5P2_A1808
load 8I5G_T70_A2005.mol2, 8I5G_T70_A2005
load 8F0P_X7L_A1610.mol2, 8F0P_X7L_A1610
load 8F0R_X7W_A1606.mol2, 8F0R_X7W_A1606
load 8F0S_X80_A1605.mol2, 8F0S_X80_A1605
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
