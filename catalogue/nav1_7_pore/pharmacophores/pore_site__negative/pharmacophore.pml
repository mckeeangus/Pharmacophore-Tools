# nav1_7_pore/pore_site__negative — ensemble pharmacophore (5 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/pore_site__negative/7W9K_9Z9_A2006.mol2, compounds
load ../../groups/pore_site__negative/8I5B_OJ0_A2021.mol2, compounds
load ../../groups/pore_site__negative/8S9B_LQO_A2003.mol2, compounds
load ../../groups/pore_site__negative/8S9C_N6W_A2003.mol2, compounds
load ../../groups/pore_site__negative/8THH_IYJ_A2004.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Acceptor_0, pos=[122.639, 123.538, 104.519], vdw=2.413
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom Hydrophobe_1, pos=[122.379, 125.386, 107.383], vdw=1.917
color ph4_Hydrophobe, Hydrophobe_1
group ph4_Hydrophobe, Hydrophobe_1
pseudoatom Hydrophobe_2, pos=[121.970, 123.687, 101.454], vdw=1.999
color ph4_Hydrophobe, Hydrophobe_2
group ph4_Hydrophobe, Hydrophobe_2
pseudoatom Donor_3, pos=[121.598, 124.599, 104.075], vdw=1.798
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Aromatic_4, pos=[123.173, 124.813, 107.114], vdw=1.000
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
