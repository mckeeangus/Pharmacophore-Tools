# drd1/orthosteric__positive — ensemble pharmacophore (9 features)
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

pseudoatom Donor_0, pos=[122.206, 119.069, 144.027], vdw=1.731
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[127.754, 121.952, 142.268], vdw=1.218
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[123.585, 119.972, 143.917], vdw=2.497
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[130.032, 124.463, 148.307], vdw=2.934
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom PosIonizable_4, pos=[127.550, 121.809, 142.231], vdw=1.563
color ph4_PosIonizable, PosIonizable_4
group ph4_PosIonizable, PosIonizable_4
pseudoatom Aromatic_5, pos=[123.914, 120.217, 142.830], vdw=1.013
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom Aromatic_6, pos=[126.913, 122.339, 146.326], vdw=1.000
color ph4_Aromatic, Aromatic_6
group ph4_Aromatic, Aromatic_6
pseudoatom LumpedHydrophobe_7, pos=[127.403, 122.576, 146.454], vdw=1.387
color ph4_LumpedHydrophobe, LumpedHydrophobe_7
group ph4_LumpedHydrophobe, LumpedHydrophobe_7
pseudoatom LumpedHydrophobe_8, pos=[123.799, 120.178, 143.270], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_8
group ph4_LumpedHydrophobe, LumpedHydrophobe_8
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
