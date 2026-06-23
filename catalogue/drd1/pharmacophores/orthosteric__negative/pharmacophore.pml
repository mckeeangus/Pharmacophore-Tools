# drd1/orthosteric__negative — ensemble pharmacophore (6 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__negative/9LLG_A1EKL_R602.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[128.476, 122.014, 144.659], vdw=1.388
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom PosIonizable_1, pos=[128.476, 122.014, 144.659], vdw=1.388
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom Aromatic_2, pos=[123.205, 119.026, 140.813], vdw=2.533
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Hydrophobe_3, pos=[125.496, 120.777, 141.225], vdw=1.097
color ph4_Hydrophobe, Hydrophobe_3
group ph4_Hydrophobe, Hydrophobe_3
pseudoatom Hydrophobe_4, pos=[123.041, 119.603, 142.895], vdw=1.314
color ph4_Hydrophobe, Hydrophobe_4
group ph4_Hydrophobe, Hydrophobe_4
pseudoatom Hydrophobe_5, pos=[123.416, 119.128, 139.405], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_5
group ph4_Hydrophobe, Hydrophobe_5
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
