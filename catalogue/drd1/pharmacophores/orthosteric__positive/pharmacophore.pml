# drd1/orthosteric__positive — ensemble pharmacophore (4 features)
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
set_color ph4_ExcludedVolume, [0.55, 0.55, 0.55]

pseudoatom Acceptor_1, pos=[123.585, 119.972, 143.917], vdw=2.497, label="Acceptor 1 (0.94)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[130.032, 124.463, 148.307], vdw=2.934, label="Acceptor 2 (0.50)"
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom LumpedHydrophobe_1, pos=[127.403, 122.576, 146.454], vdw=1.387, label="LumpedHydrophobe 1 (0.75)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom PosIonizable_1, pos=[127.550, 121.809, 142.231], vdw=1.563, label="PosIonizable 1 (0.69)"
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
