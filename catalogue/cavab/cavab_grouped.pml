# cavab — Stage 3 cells overlay (1 cells)
# Open from catalogue/cavab/:  pymol cavab_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/dhp_site__negative/5KMF_6U9_A1301.mol2, dhp_site__negative__5KMF_6U9_A1301
load groups/dhp_site__negative/5KMD_6UB_C1304.mol2, dhp_site__negative__5KMD_6UB_C1304
load groups/dhp_site__negative/6KE5_6UB_B1301.mol2, dhp_site__negative__6KE5_6UB_B1301
load groups/dhp_site__negative/5KLG_6UC_D1305.mol2, dhp_site__negative__5KLG_6UC_D1305
load groups/dhp_site__negative/5KLS_6UC_C1304.mol2, dhp_site__negative__5KLS_6UC_C1304
group dhp_site__negative, dhp_site__negative__*
color salmon, dhp_site__negative and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
