# separate_state — 3 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 7RS4_7I0_C601.mol2, 7RS4_7I0_C601
load 7TE7_I0V_A601.mol2, 7TE7_I0V_A601
load 6SBO_L5B_A4000.mol2, 6SBO_L5B_A4000
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
