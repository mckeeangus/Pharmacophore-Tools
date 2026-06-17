# separate_state — 2 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 4QKX_35V_A1403.mol2, 4QKX_35V_A1403
load 3PDS_ERC_A1201.mol2, 3PDS_ERC_A1201
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
