# gr_nr3c1 — Stage 3 cells overlay (2 cells)
# Open from catalogue/gr_nr3c1/:  pymol gr_nr3c1_grouped.pml
reinitialize
bg_color white
set valence, 1

load groups/lbp__negative/4MDD_29M_A801.mol2, lbp__negative__4MDD_29M_A801
load groups/lbp__negative/5UC3_486_A801.mol2, lbp__negative__5UC3_486_A801
load groups/lbp__negative/6DXK_HJ4_A801.mol2, lbp__negative__6DXK_HJ4_A801
group lbp__negative, lbp__negative__*
color salmon, lbp__negative and elem C
load groups/lbp__positive/7PRX_82H_A801.mol2, lbp__positive__7PRX_82H_A801
load groups/lbp__positive/3E7C_866_A1.mol2, lbp__positive__3E7C_866_A1
load groups/lbp__positive/5NFP_8W5_A804.mol2, lbp__positive__5NFP_8W5_A804
load groups/lbp__positive/5NFT_8W8_A804.mol2, lbp__positive__5NFT_8W8_A804
load groups/lbp__positive/8VKZ_A1ACE_A901.mol2, lbp__positive__8VKZ_A1ACE_A901
load groups/lbp__positive/6EL6_B9Q_A802.mol2, lbp__positive__6EL6_B9Q_A802
load groups/lbp__positive/6EL7_B9T_A802.mol2, lbp__positive__6EL7_B9T_A802
load groups/lbp__positive/6EL9_B9W_A802.mol2, lbp__positive__6EL9_B9W_A802
load groups/lbp__positive/4UDD_CV7_A1782.mol2, lbp__positive__4UDD_CV7_A1782
load groups/lbp__positive/3BQD_DAY_A301.mol2, lbp__positive__3BQD_DAY_A301
load groups/lbp__positive/1M2Z_DEX_A301.mol2, lbp__positive__1M2Z_DEX_A301
load groups/lbp__positive/5G3J_E7T_A1779.mol2, lbp__positive__5G3J_E7T_A1779
load groups/lbp__positive/7PRV_GW6_A805.mol2, lbp__positive__7PRV_GW6_A805
load groups/lbp__positive/4P6X_HCY_G900.mol2, lbp__positive__4P6X_HCY_G900
load groups/lbp__positive/3K23_JZN_B2.mol2, lbp__positive__3K23_JZN_B2
load groups/lbp__positive/3K22_JZS_B1.mol2, lbp__positive__3K22_JZS_B1
load groups/lbp__positive/4LSJ_LSJ_A801.mol2, lbp__positive__4LSJ_LSJ_A801
load groups/lbp__positive/4P6W_MOF_A801.mol2, lbp__positive__4P6W_MOF_A801
load groups/lbp__positive/4CSJ_NN7_A1778.mol2, lbp__positive__4CSJ_NN7_A1778
load groups/lbp__positive/5G5W_R8C_A1778.mol2, lbp__positive__5G5W_R8C_A1778
group lbp__positive, lbp__positive__*
color green, lbp__positive and elem C
show sticks
hide everything, hydro
set stick_radius, 0.15
orient
