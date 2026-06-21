# nachr_a4b2/orthosteric__neutral — ensemble pharmacophore (5 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__neutral/2WNC_TKT_C300.mol2, compounds
load ../../groups/orthosteric__neutral/2WZY_SQX_A301.mol2, compounds
load ../../groups/orthosteric__neutral/2X00_GYN_B301.mol2, compounds
load ../../groups/orthosteric__neutral/2XYS_SY9_E1206.mol2, compounds
load ../../groups/orthosteric__neutral/2XYT_TC9_F1206.mol2, compounds
load ../../groups/orthosteric__neutral/3SIO_MLK_D260.mol2, compounds
load ../../groups/orthosteric__neutral/8Q1M_ILR_A301.mol2, compounds
load ../../groups/orthosteric__neutral/8QTL_WSP_A301.mol2, compounds
load ../../groups/orthosteric__neutral/9SG3_PHN_A302.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[170.408, 119.399, 182.057], vdw=2.785
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[169.614, 120.201, 184.976], vdw=3.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[163.229, 124.030, 181.111], vdw=2.474
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Hydrophobe_3, pos=[166.121, 123.036, 184.389], vdw=1.353
color ph4_Hydrophobe, Hydrophobe_3
group ph4_Hydrophobe, Hydrophobe_3
pseudoatom Hydrophobe_4, pos=[168.186, 121.096, 184.020], vdw=1.457
color ph4_Hydrophobe, Hydrophobe_4
group ph4_Hydrophobe, Hydrophobe_4
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
