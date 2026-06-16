# quarantine — 3 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 8ZWG_A1D9A_A601.mol2, 8ZWG_A1D9A_A601
load 9CHU_E5E_A501.mol2, 9CHU_E5E_A501
load 8UHB_WV8_A401.mol2, 8UHB_WV8_A401
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
