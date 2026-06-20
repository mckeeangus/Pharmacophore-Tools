# nav1_7_pore — Stage 3 cells overlay (1 cells)
# Open from catalogue/nav1_7_pore/:  pymol nav1_7_pore_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/pore_site__negative/7W9K_9Z9_A2006.mol2, pore_site__negative__7W9K_9Z9_A2006
load groups/pore_site__negative/8THH_IYJ_A2004.mol2, pore_site__negative__8THH_IYJ_A2004
load groups/pore_site__negative/8S9B_LQO_A2003.mol2, pore_site__negative__8S9B_LQO_A2003
load groups/pore_site__negative/8S9C_N6W_A2003.mol2, pore_site__negative__8S9C_N6W_A2003
load groups/pore_site__negative/8I5B_OJ0_A2021.mol2, pore_site__negative__8I5B_OJ0_A2021
group pore_site__negative, pore_site__negative__*
color salmon, pore_site__negative and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
