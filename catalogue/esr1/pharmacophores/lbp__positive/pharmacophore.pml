# esr1/lbp__positive — ensemble pharmacophore (8 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/lbp__positive/2B1V_458_B202.mol2, compounds
load ../../groups/lbp__positive/2B1Z_17M_B202.mol2, compounds
load ../../groups/lbp__positive/2QAB_EI1_B1.mol2, compounds
load ../../groups/lbp__positive/2QSE_1HP_B1.mol2, compounds
load ../../groups/lbp__positive/2QZO_KN1_B1.mol2, compounds
load ../../groups/lbp__positive/4MG8_27J_A601.mol2, compounds
load ../../groups/lbp__positive/4MGA_27L_B601.mol2, compounds
load ../../groups/lbp__positive/4MGB_XDH_B601.mol2, compounds
load ../../groups/lbp__positive/4TV1_36M_A601.mol2, compounds
load ../../groups/lbp__positive/5TN4_7FZ_A601.mol2, compounds
load ../../groups/lbp__positive/5TN5_7G0_B601.mol2, compounds
load ../../groups/lbp__positive/7NEL_EST_A601.mol2, compounds
load ../../groups/lbp__positive/7NFB_GEN_A601.mol2, compounds
load ../../groups/lbp__positive/7RKE_5VP_B601.mol2, compounds
load ../../groups/lbp__positive/9W11_ZHB_A701.mol2, compounds
load ../../groups/lbp__positive/9W12_A1ET8_A701.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[21.229, -11.142, 2.618], vdw=1.811
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[26.647, -12.030, 10.316], vdw=2.316
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[20.903, -11.053, 2.110], vdw=1.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[27.340, -11.540, 10.834], vdw=1.000
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_4, pos=[23.217, -13.094, 7.487], vdw=1.000
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Aromatic_5, pos=[22.495, -11.463, 4.443], vdw=1.000
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom Hydrophobe_6, pos=[22.961, -11.667, 5.285], vdw=1.443
color ph4_Hydrophobe, Hydrophobe_6
group ph4_Hydrophobe, Hydrophobe_6
pseudoatom Hydrophobe_7, pos=[25.092, -11.919, 8.595], vdw=1.757
color ph4_Hydrophobe, Hydrophobe_7
group ph4_Hydrophobe, Hydrophobe_7
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
