# ache/gorge__negative — ensemble pharmacophore (7 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/gorge__negative/4BDT_HUW_A701.mol2, compounds
load ../../groups/gorge__negative/4EY5_HUP_A604.mol2, compounds
load ../../groups/gorge__negative/4EY6_GNT_A604.mol2, compounds
load ../../groups/gorge__negative/4M0E_1YL_B605.mol2, compounds
load ../../groups/gorge__negative/4M0F_1YK_B605.mol2, compounds
load ../../groups/gorge__negative/6O4W_E20_A604.mol2, compounds
load ../../groups/gorge__negative/6O4X_AA_B603.mol2, compounds
load ../../groups/gorge__negative/6O50_EBW_A601.mol2, compounds
load ../../groups/gorge__negative/7D9O_H0L_B601.mol2, compounds
load ../../groups/gorge__negative/7D9P_H0R_A601.mol2, compounds
load ../../groups/gorge__negative/7D9Q_H1R_B601.mol2, compounds
load ../../groups/gorge__negative/7RB6_NWA_A601.mol2, compounds
load ../../groups/gorge__negative/7XN1_THA_A601.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[90.914, 81.876, -6.156], vdw=2.014
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[86.015, 87.290, -4.993], vdw=1.126
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Aromatic_2, pos=[91.167, 80.550, -8.013], vdw=2.260
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_3, pos=[88.240, 89.067, -1.994], vdw=1.457
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Hydrophobe_4, pos=[90.671, 81.416, -7.814], vdw=2.399
color ph4_Hydrophobe, Hydrophobe_4
group ph4_Hydrophobe, Hydrophobe_4
pseudoatom Hydrophobe_5, pos=[88.144, 87.318, -3.284], vdw=2.507
color ph4_Hydrophobe, Hydrophobe_5
group ph4_Hydrophobe, Hydrophobe_5
pseudoatom PosIonizable_6, pos=[90.783, 81.273, -6.814], vdw=2.022
color ph4_PosIonizable, PosIonizable_6
group ph4_PosIonizable, PosIonizable_6
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
