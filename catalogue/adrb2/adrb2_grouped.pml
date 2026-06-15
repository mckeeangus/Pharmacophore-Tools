# adrb2 — Stage 3 cells overlay (4 cells)
# Open from catalogue/adrb2/:  pymol adrb2_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/orthosteric__negative/2RH1_CAU_A408.mol2, orthosteric__negative__2RH1_CAU_A408
load groups/orthosteric__negative/5D5A_CAU_A1202.mol2, orthosteric__negative__5D5A_CAU_A1202
load groups/orthosteric__negative/5D6L_CAU_A1208.mol2, orthosteric__negative__5D6L_CAU_A1208
load groups/orthosteric__negative/5X7D_CAU_A1206.mol2, orthosteric__negative__5X7D_CAU_A1206
load groups/orthosteric__negative/6PS0_CAU_A1201.mol2, orthosteric__negative__6PS0_CAU_A1201
group orthosteric__negative, orthosteric__negative__*
color salmon, orthosteric__negative and elem C
load groups/orthosteric__positive/7DHI_68H_R401.mol2, orthosteric__positive__7DHI_68H_R401
load groups/orthosteric__positive/8JJL_DZQ_A501.mol2, orthosteric__positive__8JJL_DZQ_A501
load groups/orthosteric__positive/9LW5_LDP_R401.mol2, orthosteric__positive__9LW5_LDP_R401
group orthosteric__positive, orthosteric__positive__*
color green, orthosteric__positive and elem C
load groups/secondary_1__negative/5JQH_CAU_B1401.mol2, secondary_1__negative__5JQH_CAU_B1401
group secondary_1__negative, secondary_1__negative__*
color salmon, secondary_1__negative and elem C
load groups/secondary_1__positive/4LDO_ALE_A1402.mol2, secondary_1__positive__4LDO_ALE_A1402
load groups/secondary_1__positive/6MXT_K5Y_A1401.mol2, secondary_1__positive__6MXT_K5Y_A1401
group secondary_1__positive, secondary_1__positive__*
color green, secondary_1__positive and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
