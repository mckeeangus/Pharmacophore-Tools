# esr1/lbp__negative — ensemble pharmacophore (8 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/lbp__negative/1XP1_AIH_A600.mol2, compounds
load ../../groups/lbp__negative/1XP6_AIU_A600.mol2, compounds
load ../../groups/lbp__negative/1XP9_AIJ_A600.mol2, compounds
load ../../groups/lbp__negative/1XPC_AIT_A600.mol2, compounds
load ../../groups/lbp__negative/2IOG_IOG_A600.mol2, compounds
load ../../groups/lbp__negative/4ZNS_OFB_B601.mol2, compounds
load ../../groups/lbp__negative/4ZNV_4Q7_B601.mol2, compounds
load ../../groups/lbp__negative/5KCD_OB2_A601.mol2, compounds
load ../../groups/lbp__negative/5KCE_OB3_A602.mol2, compounds
load ../../groups/lbp__negative/5KCT_OB6_B601.mol2, compounds
load ../../groups/lbp__negative/5KCT_OB7_A601.mol2, compounds
load ../../groups/lbp__negative/5U2D_OBH_A601.mol2, compounds
load ../../groups/lbp__negative/5W9C_OHT_D601.mol2, compounds
load ../../groups/lbp__negative/5W9D_9XY_A601.mol2, compounds
load ../../groups/lbp__negative/6PSJ_29S_B601.mol2, compounds
load ../../groups/lbp__negative/6VJD_C3D_C601.mol2, compounds
load ../../groups/lbp__negative/6VPF_53Q_B601.mol2, compounds
load ../../groups/lbp__negative/7NDO_RAL_B601.mol2, compounds
load ../../groups/lbp__negative/7RRX_7AI_B601.mol2, compounds
load ../../groups/lbp__negative/7RRY_L84_C601.mol2, compounds
load ../../groups/lbp__negative/7RRZ_77I_C601.mol2, compounds
load ../../groups/lbp__negative/7RS0_7I9_C601.mol2, compounds
load ../../groups/lbp__negative/7RS1_7Q5_C601.mol2, compounds
load ../../groups/lbp__negative/7RS2_7I5_C601.mol2, compounds
load ../../groups/lbp__negative/7RS3_7OR_B604.mol2, compounds
load ../../groups/lbp__negative/7RS7_73I_A601.mol2, compounds
load ../../groups/lbp__negative/7RS8_7EI_C601.mol2, compounds
load ../../groups/lbp__negative/7RS9_7OI_C601.mol2, compounds
load ../../groups/lbp__negative/7UJ7_NYU_C901.mol2, compounds
load ../../groups/lbp__negative/7UJF_R3V_C601.mol2, compounds
load ../../groups/lbp__negative/7UJO_QYM_C601.mol2, compounds
load ../../groups/lbp__negative/7UJY_RL4_C601.mol2, compounds
load ../../groups/lbp__negative/8DU8_TS7_B601.mol2, compounds
load ../../groups/lbp__negative/8DUB_TTU_B601.mol2, compounds
load ../../groups/lbp__negative/8DUC_TU9_A601.mol2, compounds
load ../../groups/lbp__negative/8DUD_TV3_A601.mol2, compounds
load ../../groups/lbp__negative/8DUK_TW6_C601.mol2, compounds
load ../../groups/lbp__negative/8DV5_TX9_A601.mol2, compounds
load ../../groups/lbp__negative/8DV7_TXK_B601.mol2, compounds
load ../../groups/lbp__negative/8DV8_TZ3_A601.mol2, compounds
load ../../groups/lbp__negative/8W03_OBT_C600.mol2, compounds
load ../../groups/lbp__negative/9BU1_A1ASN_B601.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[20.809, -10.921, 1.943], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[28.297, -4.011, 5.973], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[24.564, -13.510, 9.986], vdw=2.585
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[27.485, -7.309, 7.121], vdw=1.347
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_4, pos=[21.245, -11.126, 2.274], vdw=1.676
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Aromatic_5, pos=[22.437, -11.630, 4.100], vdw=1.000
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom Aromatic_6, pos=[26.252, -9.704, 6.732], vdw=1.000
color ph4_Aromatic, Aromatic_6
group ph4_Aromatic, Aromatic_6
pseudoatom Hydrophobe_7, pos=[24.228, -12.081, 6.952], vdw=2.515
color ph4_Hydrophobe, Hydrophobe_7
group ph4_Hydrophobe, Hydrophobe_7
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
