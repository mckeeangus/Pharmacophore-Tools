# ache — Stage 3 cells overlay (1 cells)
# Open from catalogue/ache/:  pymol ache_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/gorge__negative/4M0F_1YK_B605.mol2, gorge__negative__4M0F_1YK_B605
load groups/gorge__negative/4M0E_1YL_B605.mol2, gorge__negative__4M0E_1YL_B605
load groups/gorge__negative/6O4X_AA_B603.mol2, gorge__negative__6O4X_AA_B603
load groups/gorge__negative/6O4W_E20_A604.mol2, gorge__negative__6O4W_E20_A604
load groups/gorge__negative/6O50_EBW_A601.mol2, gorge__negative__6O50_EBW_A601
load groups/gorge__negative/4EY6_GNT_A604.mol2, gorge__negative__4EY6_GNT_A604
load groups/gorge__negative/7D9O_H0L_B601.mol2, gorge__negative__7D9O_H0L_B601
load groups/gorge__negative/7D9P_H0R_B601.mol2, gorge__negative__7D9P_H0R_B601
load groups/gorge__negative/7D9Q_H1R_A601.mol2, gorge__negative__7D9Q_H1R_A601
load groups/gorge__negative/4EY5_HUP_A604.mol2, gorge__negative__4EY5_HUP_A604
load groups/gorge__negative/4BDT_HUW_A701.mol2, gorge__negative__4BDT_HUW_A701
load groups/gorge__negative/7RB6_NWA_B601.mol2, gorge__negative__7RB6_NWA_B601
load groups/gorge__negative/7XN1_THA_A601.mol2, gorge__negative__7XN1_THA_A601
group gorge__negative, gorge__negative__*
color salmon, gorge__negative and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
