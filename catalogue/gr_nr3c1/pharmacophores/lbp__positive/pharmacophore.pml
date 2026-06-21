# gr_nr3c1/lbp__positive — ensemble pharmacophore (8 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/lbp__positive/1M2Z_DEX_A301.mol2, compounds
load ../../groups/lbp__positive/3BQD_DAY_A301.mol2, compounds
load ../../groups/lbp__positive/3E7C_866_A1.mol2, compounds
load ../../groups/lbp__positive/3K22_JZS_B1.mol2, compounds
load ../../groups/lbp__positive/3K23_JZN_B2.mol2, compounds
load ../../groups/lbp__positive/4CSJ_NN7_A1778.mol2, compounds
load ../../groups/lbp__positive/4LSJ_LSJ_A801.mol2, compounds
load ../../groups/lbp__positive/4P6W_MOF_A801.mol2, compounds
load ../../groups/lbp__positive/4P6X_HCY_C900.mol2, compounds
load ../../groups/lbp__positive/4UDD_CV7_A1782.mol2, compounds
load ../../groups/lbp__positive/5G3J_E7T_A1779.mol2, compounds
load ../../groups/lbp__positive/5G5W_R8C_A1778.mol2, compounds
load ../../groups/lbp__positive/5NFP_8W5_A804.mol2, compounds
load ../../groups/lbp__positive/5NFT_8W8_A804.mol2, compounds
load ../../groups/lbp__positive/6EL6_B9Q_A802.mol2, compounds
load ../../groups/lbp__positive/6EL7_B9T_A802.mol2, compounds
load ../../groups/lbp__positive/6EL9_B9W_A802.mol2, compounds
load ../../groups/lbp__positive/7PRV_GW6_A805.mol2, compounds
load ../../groups/lbp__positive/7PRX_82H_A801.mol2, compounds
load ../../groups/lbp__positive/8VKZ_A1ACE_A901.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Acceptor_0, pos=[28.739, 6.908, 14.827], vdw=3.000
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom Acceptor_1, pos=[34.067, 8.315, 6.623], vdw=3.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Hydrophobe_2, pos=[32.265, 7.314, 10.880], vdw=2.371
color ph4_Hydrophobe, Hydrophobe_2
group ph4_Hydrophobe, Hydrophobe_2
pseudoatom Hydrophobe_3, pos=[28.833, 8.021, 14.877], vdw=2.559
color ph4_Hydrophobe, Hydrophobe_3
group ph4_Hydrophobe, Hydrophobe_3
pseudoatom Donor_4, pos=[28.632, 5.909, 13.661], vdw=3.000
color ph4_Donor, Donor_4
group ph4_Donor, Donor_4
pseudoatom Aromatic_5, pos=[31.985, 7.683, 9.456], vdw=1.815
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom Aromatic_6, pos=[28.044, 9.760, 14.412], vdw=2.330
color ph4_Aromatic, Aromatic_6
group ph4_Aromatic, Aromatic_6
pseudoatom Aromatic_7, pos=[34.459, 9.264, 5.971], vdw=1.000
color ph4_Aromatic, Aromatic_7
group ph4_Aromatic, Aromatic_7
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
