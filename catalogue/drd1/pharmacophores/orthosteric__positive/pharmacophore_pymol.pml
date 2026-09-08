# drd1/orthosteric__positive — ensemble pharmacophore (47 features)
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

pseudoatom Aromatic_1, pos=[123.580, 120.575, 142.657], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[123.580, 120.575, 142.657], label="Aromatic 1 (0.88)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom LumpedHydrophobe_1, pos=[127.030, 122.824, 146.513], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[127.030, 122.824, 146.513], label="LumpedHydrophobe 1 (0.62)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom Aromatic_2, pos=[126.606, 122.613, 146.577], vdw=1.250
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[126.606, 122.613, 146.577], label="Aromatic 2 (0.62)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom LumpedHydrophobe_2, pos=[124.026, 119.919, 143.514], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_2
group ph4_LumpedHydrophobe, LumpedHydrophobe_2
pseudoatom LumpedHydrophobe_2_ctr, pos=[124.026, 119.919, 143.514], label="LumpedHydrophobe 2 (0.62)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_2_ctr
group ph4_centers, LumpedHydrophobe_2_ctr
pseudoatom Donor_1, pos=[122.230, 119.153, 144.871], vdw=1.250
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[122.230, 119.153, 144.871], label="Donor 1 (0.50)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Acceptor_1, pos=[122.247, 119.175, 144.868], vdw=1.250
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[122.247, 119.175, 144.868], label="Acceptor 1 (0.50)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom PosIonizable_1, pos=[127.584, 121.663, 142.396], vdw=1.250
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom PosIonizable_1_ctr, pos=[127.584, 121.663, 142.396], label="PosIonizable 1 (0.50)"
color ph4_PosIonizable, PosIonizable_1_ctr
group ph4_centers, PosIonizable_1_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
