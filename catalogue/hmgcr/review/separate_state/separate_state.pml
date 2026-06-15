# separate_state — 3 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 1DQ9_HMG_D104.mol2, 1DQ9_HMG_D104
load 1DQ8_MAH_A200.mol2, 1DQ8_MAH_A200
load 1DQA_MAH_B202.mol2, 1DQA_MAH_B202
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
