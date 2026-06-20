# unknown — 4 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 5OLV_9Y2_A1201.mol2, 5OLV_9Y2_A1201
load 7IN9_A1COM_A1234.mol2, 7IN9_A1COM_A1234
load 7INI_A1COV_A1234.mol2, 7INI_A1COV_A1234
load 7INL_A1COY_A1234.mol2, 7INL_A1COY_A1234
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
