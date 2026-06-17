# unknown — 4 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 7WLW_1WR_A704.mol2, 7WLW_1WR_A704
load 4XPH_42J_A602.mol2, 4XPH_42J_A602
load 7WGT_9BC_A701.mol2, 7WGT_9BC_A701
load 9EUO_A1H8F_A701.mol2, 9EUO_A1H8F_A701
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
