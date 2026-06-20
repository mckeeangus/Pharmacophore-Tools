# nav1_7_vsd4 — Stage 3 cells overlay (1 cells)
# Open from catalogue/nav1_7_vsd4/:  pymol nav1_7_vsd4_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/vsd4_site__negative/8F0P_X7L_A1610.mol2, vsd4_site__negative__8F0P_X7L_A1610
load groups/vsd4_site__negative/8F0R_X7W_A1606.mol2, vsd4_site__negative__8F0R_X7W_A1606
load groups/vsd4_site__negative/8F0S_X80_A1605.mol2, vsd4_site__negative__8F0S_X80_A1605
group vsd4_site__negative, vsd4_site__negative__*
color salmon, vsd4_site__negative and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
