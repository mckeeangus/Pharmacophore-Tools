# ache/gorge__negative — ensemble pharmacophore (7 features)
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
pseudoatom LumpedHydrophobe_4, pos=[91.010, 80.626, -7.947], vdw=2.373
color ph4_LumpedHydrophobe, LumpedHydrophobe_4
group ph4_LumpedHydrophobe, LumpedHydrophobe_4
pseudoatom LumpedHydrophobe_5, pos=[88.224, 89.384, -1.760], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_5
group ph4_LumpedHydrophobe, LumpedHydrophobe_5
pseudoatom PosIonizable_6, pos=[90.783, 81.273, -6.814], vdw=2.022
color ph4_PosIonizable, PosIonizable_6
group ph4_PosIonizable, PosIonizable_6
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
