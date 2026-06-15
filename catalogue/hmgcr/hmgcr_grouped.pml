# hmgcr — Stage 3 cells overlay (1 cells)
# Open from catalogue/hmgcr/:  pymol hmgcr_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/hmg_site__negative/1HW8_114_C4.mol2, hmg_site__negative__1HW8_114_C4
load groups/hmg_site__negative/1HWI_115_A2.mol2, hmg_site__negative__1HWI_115_A2
load groups/hmg_site__negative/1HWJ_116_C4.mol2, hmg_site__negative__1HWJ_116_C4
load groups/hmg_site__negative/1HWK_117_A2.mol2, hmg_site__negative__1HWK_117_A2
load groups/hmg_site__negative/3CCT_3HI_D3.mol2, hmg_site__negative__3CCT_3HI_D3
load groups/hmg_site__negative/3CCW_4HI_C4.mol2, hmg_site__negative__3CCW_4HI_C4
load groups/hmg_site__negative/3CCZ_5HI_B876.mol2, hmg_site__negative__3CCZ_5HI_B876
load groups/hmg_site__negative/3CD0_6HI_D3.mol2, hmg_site__negative__3CD0_6HI_D3
load groups/hmg_site__negative/3CD5_7HI_B1.mol2, hmg_site__negative__3CD5_7HI_B1
load groups/hmg_site__negative/2Q1L_882_A876.mol2, hmg_site__negative__2Q1L_882_A876
load groups/hmg_site__negative/3CD7_882_A1.mol2, hmg_site__negative__3CD7_882_A1
load groups/hmg_site__negative/3CDA_8HI_C4.mol2, hmg_site__negative__3CDA_8HI_C4
load groups/hmg_site__negative/3CDB_9HI_D3.mol2, hmg_site__negative__3CDB_9HI_D3
load groups/hmg_site__negative/1HWL_FBI_A2.mol2, hmg_site__negative__1HWL_FBI_A2
load groups/hmg_site__negative/2Q6C_HR1_A3002.mol2, hmg_site__negative__2Q6C_HR1_A3002
load groups/hmg_site__negative/2Q6B_HR2_A3001.mol2, hmg_site__negative__2Q6B_HR2_A3001
load groups/hmg_site__negative/3BGL_RID_A2.mol2, hmg_site__negative__3BGL_RID_A2
load groups/hmg_site__negative/2R4F_RIE_B876.mol2, hmg_site__negative__2R4F_RIE_B876
load groups/hmg_site__negative/1HW9_SIM_C1.mol2, hmg_site__negative__1HW9_SIM_C1
group hmg_site__negative, hmg_site__negative__*
color salmon, hmg_site__negative and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
