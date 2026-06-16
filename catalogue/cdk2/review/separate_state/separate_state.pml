# separate_state — 1 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 4EOJ_ATP_A301.mol2, 4EOJ_ATP_A301
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
