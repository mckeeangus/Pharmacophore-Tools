# unknown — 3 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 4COF_BEN_E500.mol2, 4COF_BEN_E500
load 9HAA_BUA_B601.mol2, 9HAA_BUA_B601
load 9DRX_IYJ_D402.mol2, 9DRX_IYJ_D402
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
