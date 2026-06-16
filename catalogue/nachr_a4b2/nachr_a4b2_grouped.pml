# nachr_a4b2 — Stage 3 cells overlay (2 cells)
# Open from catalogue/nachr_a4b2/:  pymol nachr_a4b2_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/orthosteric__neutral/3SIO_MLK_A260.mol2, orthosteric__neutral__3SIO_MLK_A260
load groups/orthosteric__neutral/9SG3_PHN_A302.mol2, orthosteric__neutral__9SG3_PHN_A302
load groups/orthosteric__neutral/2XYS_SY9_C1206.mol2, orthosteric__neutral__2XYS_SY9_C1206
load groups/orthosteric__neutral/2XYT_TC9_F1206.mol2, orthosteric__neutral__2XYT_TC9_F1206
group orthosteric__neutral, orthosteric__neutral__*
color yellow, orthosteric__neutral and elem C
load groups/orthosteric__positive/8ST4_ACH_D704.mol2, orthosteric__positive__8ST4_ACH_D704
load groups/orthosteric__positive/5SYO_C5E_C301.mol2, orthosteric__positive__5SYO_C5E_C301
load groups/orthosteric__positive/1UV6_CCE_J1206.mol2, orthosteric__positive__1UV6_CCE_J1206
load groups/orthosteric__positive/5BP0_FN1_E301.mol2, orthosteric__positive__5BP0_FN1_E301
load groups/orthosteric__positive/1UW6_NCT_E1206.mol2, orthosteric__positive__1UW6_NCT_E1206
load groups/orthosteric__positive/5AIN_QMR_A1207.mol2, orthosteric__positive__5AIN_QMR_A1207
group orthosteric__positive, orthosteric__positive__*
color green, orthosteric__positive and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
