# esr1 — Stage 3 cells overlay (2 cells)
# Open from catalogue/esr1/:  pymol esr1_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/lbp__negative/6PSJ_29S_B601.mol2, lbp__negative__6PSJ_29S_B601
load groups/lbp__negative/6VPF_53Q_A601.mol2, lbp__negative__6VPF_53Q_A601
load groups/lbp__negative/5W9D_9XY_B601.mol2, lbp__negative__5W9D_9XY_B601
load groups/lbp__negative/5W9C_OHT_C601.mol2, lbp__negative__5W9C_OHT_C601
load groups/lbp__negative/2QXS_RAL_A600.mol2, lbp__negative__2QXS_RAL_A600
load groups/lbp__negative/7KBS_RAL_B601.mol2, lbp__negative__7KBS_RAL_B601
load groups/lbp__negative/7NDO_RAL_A601.mol2, lbp__negative__7NDO_RAL_A601
load groups/lbp__negative/7UJC_RAL_B601.mol2, lbp__negative__7UJC_RAL_B601
group lbp__negative, lbp__negative__*
color salmon, lbp__negative and elem C
load groups/lbp__positive/2B1Z_17M_B202.mol2, lbp__positive__2B1Z_17M_B202
load groups/lbp__positive/4MG8_27J_A601.mol2, lbp__positive__4MG8_27J_A601
load groups/lbp__positive/2YJA_EST_B1550.mol2, lbp__positive__2YJA_EST_B1550
load groups/lbp__positive/3UUD_EST_A600.mol2, lbp__positive__3UUD_EST_A600
load groups/lbp__positive/5DXE_EST_A1000.mol2, lbp__positive__5DXE_EST_A1000
load groups/lbp__positive/5DXG_EST_A1000.mol2, lbp__positive__5DXG_EST_A1000
load groups/lbp__positive/5WGD_EST_A601.mol2, lbp__positive__5WGD_EST_A601
load groups/lbp__positive/6CBZ_EST_A601.mol2, lbp__positive__6CBZ_EST_A601
load groups/lbp__positive/7NEL_EST_A601.mol2, lbp__positive__7NEL_EST_A601
load groups/lbp__positive/2QA8_GEN_A600.mol2, lbp__positive__2QA8_GEN_A600
load groups/lbp__positive/7NFB_GEN_A601.mol2, lbp__positive__7NFB_GEN_A601
group lbp__positive, lbp__positive__*
color green, lbp__positive and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
