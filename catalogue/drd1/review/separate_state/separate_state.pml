# separate_state — 2 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 7F1O_GDP_A402.mol2, 7F1O_GDP_A402
load 7F23_GTP_A401.mol2, 7F23_GTP_A401
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
