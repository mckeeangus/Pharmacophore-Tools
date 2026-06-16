# esr1 — Stage 3 cells overlay (2 cells)
# Open from catalogue/esr1/:  pymol esr1_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/lbp__negative/6PSJ_29S_B601.mol2, lbp__negative__6PSJ_29S_B601
load groups/lbp__negative/6VPF_53Q_A601.mol2, lbp__negative__6VPF_53Q_A601
load groups/lbp__negative/5W9D_9XY_B601.mol2, lbp__negative__5W9D_9XY_B601
load groups/lbp__negative/1XP1_AIH_A600.mol2, lbp__negative__1XP1_AIH_A600
load groups/lbp__negative/1XP9_AIJ_A600.mol2, lbp__negative__1XP9_AIJ_A600
load groups/lbp__negative/1XPC_AIT_A600.mol2, lbp__negative__1XPC_AIT_A600
load groups/lbp__negative/1XP6_AIU_A600.mol2, lbp__negative__1XP6_AIU_A600
load groups/lbp__negative/5W9C_OHT_C601.mol2, lbp__negative__5W9C_OHT_C601
load groups/lbp__negative/7NDO_RAL_A601.mol2, lbp__negative__7NDO_RAL_A601
group lbp__negative, lbp__negative__*
color salmon, lbp__negative and elem C
load groups/lbp__positive/2B1Z_17M_B202.mol2, lbp__positive__2B1Z_17M_B202
load groups/lbp__positive/4MG8_27J_A601.mol2, lbp__positive__4MG8_27J_A601
load groups/lbp__positive/7NEL_EST_A601.mol2, lbp__positive__7NEL_EST_A601
load groups/lbp__positive/7NFB_GEN_A601.mol2, lbp__positive__7NFB_GEN_A601
group lbp__positive, lbp__positive__*
color green, lbp__positive and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
