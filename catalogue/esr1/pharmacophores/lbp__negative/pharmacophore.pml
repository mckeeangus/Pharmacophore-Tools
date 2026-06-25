# esr1/lbp__negative — ensemble pharmacophore (9 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load representative_ligand.sdf, ligand
hide everything, ligand
show sticks, ligand
color grey70, ligand and elem C

set_color ph4_Donor, [1.0, 0.4, 0.7]
set_color ph4_Acceptor, [0.0, 0.8, 0.0]
set_color ph4_LumpedHydrophobe, [0.0, 0.9, 0.9]
set_color ph4_Aromatic, [1.0, 0.85, 0.0]
set_color ph4_PosIonizable, [1.0, 0.0, 0.0]
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
pseudoatom LumpedHydrophobe_7, pos=[26.252, -9.704, 6.732], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_7
group ph4_LumpedHydrophobe, LumpedHydrophobe_7
pseudoatom LumpedHydrophobe_8, pos=[22.416, -11.603, 4.010], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_8
group ph4_LumpedHydrophobe, LumpedHydrophobe_8
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
