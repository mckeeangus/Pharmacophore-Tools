# adrb2/orthosteric__neutral — ensemble pharmacophore (8 features)
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

pseudoatom Donor_0, pos=[-33.229, 9.668, 7.696], vdw=1.410
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[-30.053, 11.017, 6.980], vdw=2.677
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[-34.180, 2.911, 8.575], vdw=2.185
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom PosIonizable_3, pos=[-32.799, 8.034, 7.554], vdw=1.000
color ph4_PosIonizable, PosIonizable_3
group ph4_PosIonizable, PosIonizable_3
pseudoatom Aromatic_4, pos=[-32.097, 3.510, 9.046], vdw=3.000
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Aromatic_5, pos=[-28.118, 11.057, 6.017], vdw=1.256
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom LumpedHydrophobe_6, pos=[-30.310, 3.775, 9.306], vdw=3.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_6
group ph4_LumpedHydrophobe, LumpedHydrophobe_6
pseudoatom LumpedHydrophobe_7, pos=[-28.118, 11.057, 6.017], vdw=1.256
color ph4_LumpedHydrophobe, LumpedHydrophobe_7
group ph4_LumpedHydrophobe, LumpedHydrophobe_7
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
