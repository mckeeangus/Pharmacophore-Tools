# hiv1_protease/active_site__negative — ensemble pharmacophore (16 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/active_site__negative/1BVE_DMP_B100.mol2, compounds
load ../../groups/active_site__negative/1BWB_146_B641.mol2, compounds
load ../../groups/active_site__negative/1DMP_DMQ_B450.mol2, compounds
load ../../groups/active_site__negative/1HIV_1ZK_A100.mol2, compounds
load ../../groups/active_site__negative/1HVH_Q82_B265.mol2, compounds
load ../../groups/active_site__negative/1HVR_XK2_A263.mol2, compounds
load ../../groups/active_site__negative/1HWR_216_B216.mol2, compounds
load ../../groups/active_site__negative/1ODX_0E8_A201.mol2, compounds
load ../../groups/active_site__negative/1ODY_LP1_A201.mol2, compounds
load ../../groups/active_site__negative/1QBR_XV6_A638.mol2, compounds
load ../../groups/active_site__negative/1QBU_846_B300.mol2, compounds
load ../../groups/active_site__negative/2FDE_385_A101.mol2, compounds
load ../../groups/active_site__negative/2WHH_GLU_A2302.mol2, compounds
load ../../groups/active_site__negative/2WHH_PPN_A2301.mol2, compounds
load ../../groups/active_site__negative/4Q1Y_017_A106.mol2, compounds
load ../../groups/active_site__negative/4Q5M_ROC_A1101.mol2, compounds
load ../../groups/active_site__negative/4U7Q_3EM_B101.mol2, compounds
load ../../groups/active_site__negative/4U7V_3EN_B101.mol2, compounds
load ../../groups/active_site__negative/5DGU_5B7_A201.mol2, compounds
load ../../groups/active_site__negative/5DGW_5B5_A201.mol2, compounds
load ../../groups/active_site__negative/5KAO_G43_A500.mol2, compounds
load ../../groups/active_site__negative/6DIF_TPV_B201.mol2, compounds
load ../../groups/active_site__negative/6DJ1_AB1_B201.mol2, compounds
load ../../groups/active_site__negative/6DJ5_G52_B201.mol2, compounds
load ../../groups/active_site__negative/6DJ7_G10_B201.mol2, compounds
load ../../groups/active_site__negative/6DV0_GA8_B201.mol2, compounds
load ../../groups/active_site__negative/6DV4_GA5_B201.mol2, compounds
load ../../groups/active_site__negative/6E7J_HWY_A201.mol2, compounds
load ../../groups/active_site__negative/6E9A_J0S_B201.mol2, compounds
load ../../groups/active_site__negative/7DOZ_1UN_A1102.mol2, compounds
load ../../groups/active_site__negative/8ESX_X7B_B203.mol2, compounds
load ../../groups/active_site__negative/8F0F_X7H_B201.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[-10.271, 17.797, 28.033], vdw=2.219
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[-6.995, 17.314, 21.672], vdw=2.447
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[-11.319, 14.529, 34.904], vdw=2.259
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Acceptor_3, pos=[-8.576, 15.456, 25.814], vdw=1.669
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_4, pos=[-10.865, 19.010, 27.934], vdw=1.291
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_5, pos=[-7.996, 17.968, 20.765], vdw=1.639
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Acceptor_6, pos=[-11.699, 15.890, 34.988], vdw=1.671
color ph4_Acceptor, Acceptor_6
group ph4_Acceptor, Acceptor_6
pseudoatom Acceptor_7, pos=[-9.271, 15.544, 30.658], vdw=1.418
color ph4_Acceptor, Acceptor_7
group ph4_Acceptor, Acceptor_7
pseudoatom Aromatic_8, pos=[-4.877, 18.168, 26.406], vdw=1.000
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
pseudoatom Aromatic_9, pos=[-12.929, 13.433, 29.071], vdw=1.000
color ph4_Aromatic, Aromatic_9
group ph4_Aromatic, Aromatic_9
pseudoatom Aromatic_10, pos=[-8.630, 16.553, 22.488], vdw=1.000
color ph4_Aromatic, Aromatic_10
group ph4_Aromatic, Aromatic_10
pseudoatom Aromatic_11, pos=[-9.965, 15.850, 33.482], vdw=1.022
color ph4_Aromatic, Aromatic_11
group ph4_Aromatic, Aromatic_11
pseudoatom Hydrophobe_12, pos=[-6.367, 18.361, 27.032], vdw=1.967
color ph4_Hydrophobe, Hydrophobe_12
group ph4_Hydrophobe, Hydrophobe_12
pseudoatom Hydrophobe_13, pos=[-12.334, 15.231, 28.382], vdw=1.229
color ph4_Hydrophobe, Hydrophobe_13
group ph4_Hydrophobe, Hydrophobe_13
pseudoatom Hydrophobe_14, pos=[-8.572, 16.399, 23.099], vdw=1.293
color ph4_Hydrophobe, Hydrophobe_14
group ph4_Hydrophobe, Hydrophobe_14
pseudoatom Hydrophobe_15, pos=[-10.061, 15.535, 32.928], vdw=1.520
color ph4_Hydrophobe, Hydrophobe_15
group ph4_Hydrophobe, Hydrophobe_15
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
