# gaba_a — Stage 3 cells overlay (4 cells)
# Open from catalogue/gaba_a/:  pymol gaba_a_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/bzd_site__negative/8DD3_R63_D701.mol2, bzd_site__negative__8DD3_R63_D701
group bzd_site__negative, bzd_site__negative__*
color salmon, bzd_site__negative and elem C
load groups/bzd_site__neutral/7QNE_EIE_D502.mol2, bzd_site__neutral__7QNE_EIE_D502
group bzd_site__neutral, bzd_site__neutral__*
color yellow, bzd_site__neutral and elem C
load groups/bzd_site__positive/6HUO_08H_D501.mol2, bzd_site__positive__6HUO_08H_D501
load groups/bzd_site__positive/8VQY_A1ADG_E401.mol2, bzd_site__positive__8VQY_A1ADG_E401
load groups/bzd_site__positive/6X3X_DZP_D404.mol2, bzd_site__positive__6X3X_DZP_D404
group bzd_site__positive, bzd_site__positive__*
color green, bzd_site__positive and elem C
load groups/orthosteric__positive/9EQG_ABU_E3205.mol2, orthosteric__positive__9EQG_ABU_E3205
load groups/orthosteric__positive/7QNC_EI7_B503.mol2, orthosteric__positive__7QNC_EI7_B503
load groups/orthosteric__positive/7A5V_HSM_A5408.mol2, orthosteric__positive__7A5V_HSM_A5408
group orthosteric__positive, orthosteric__positive__*
color green, orthosteric__positive and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
