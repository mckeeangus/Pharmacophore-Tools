# cox2 — Stage 3 cells overlay (1 cells)
# Open from catalogue/cox2/:  pymol cox2_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/cox_channel__negative/5IKV_FLF_B601.mol2, cox_channel__negative__5IKV_FLF_B601
load groups/cox_channel__negative/5IKR_ID8_A601.mol2, cox_channel__negative__5IKR_ID8_A601
load groups/cox_channel__negative/5KIR_RCX_A601.mol2, cox_channel__negative__5KIR_RCX_A601
load groups/cox_channel__negative/5F1A_SAL_A601.mol2, cox_channel__negative__5F1A_SAL_A601
load groups/cox_channel__negative/5IKT_TLF_B601.mol2, cox_channel__negative__5IKT_TLF_B601
group cox_channel__negative, cox_channel__negative__*
color salmon, cox_channel__negative and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
