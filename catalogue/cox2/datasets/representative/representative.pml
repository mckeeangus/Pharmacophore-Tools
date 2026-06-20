# representative — 6 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 5IKV_FLF_B601.mol2, 5IKV_FLF_B601
load 5IKR_ID8_A601.mol2, 5IKR_ID8_A601
load 5IKQ_JMS_B602.mol2, 5IKQ_JMS_B602
load 5KIR_RCX_A601.mol2, 5KIR_RCX_A601
load 5F1A_SAL_A601.mol2, 5F1A_SAL_A601
load 5IKT_TLF_B601.mol2, 5IKT_TLF_B601
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
