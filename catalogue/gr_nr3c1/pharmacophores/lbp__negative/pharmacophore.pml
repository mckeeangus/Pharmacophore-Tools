# gr_nr3c1/lbp__negative — ensemble pharmacophore (6 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/lbp__negative/4MDD_29M_B801.mol2, compounds
load ../../groups/lbp__negative/5UC3_486_B801.mol2, compounds
load ../../groups/lbp__negative/6DXK_HJ4_A801.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[28.806, 7.140, 16.806], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[32.710, 8.607, 8.576], vdw=2.294
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[27.163, 6.055, 16.417], vdw=2.210
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Aromatic_3, pos=[30.436, 3.441, 12.177], vdw=1.000
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Hydrophobe_4, pos=[31.006, 6.945, 12.619], vdw=2.209
color ph4_Hydrophobe, Hydrophobe_4
group ph4_Hydrophobe, Hydrophobe_4
pseudoatom Hydrophobe_5, pos=[28.102, 10.010, 15.238], vdw=1.094
color ph4_Hydrophobe, Hydrophobe_5
group ph4_Hydrophobe, Hydrophobe_5
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
