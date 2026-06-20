# chrm2 — Stage 3 cells overlay (2 cells)
# Open from catalogue/chrm2/:  pymol chrm2_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/orthosteric__negative/5ZKC_3C0_A501.mol2, orthosteric__negative__5ZKC_3C0_A501
load groups/orthosteric__negative/5ZKB_82F_A1201.mol2, orthosteric__negative__5ZKB_82F_A1201
load groups/orthosteric__negative/5ZK3_QNB_A501.mol2, orthosteric__negative__5ZK3_QNB_A501
group orthosteric__negative, orthosteric__negative__*
color salmon, orthosteric__negative and elem C
load groups/orthosteric__positive/7T94_ACH_A501.mol2, orthosteric__positive__7T94_ACH_A501
load groups/orthosteric__positive/4MQS_IXO_A501.mol2, orthosteric__positive__4MQS_IXO_A501
group orthosteric__positive, orthosteric__positive__*
color green, orthosteric__positive and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
