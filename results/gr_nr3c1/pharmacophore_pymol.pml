# gr_nr3c1 — ensemble pharmacophore (8 features)
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

pseudoatom Donor_1, pos=[1.515, 1.461, 1.366], vdw=1.250
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[1.515, 1.461, 1.366], label="Donor 1 (0.82)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Acceptor_1, pos=[0.597, -1.045, 2.153], vdw=1.250
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[0.597, -1.045, 2.153], label="Acceptor 1 (0.82)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Aromatic_1, pos=[-2.195, 1.459, 0.238], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[-2.195, 1.459, 0.238], label="Aromatic 1 (0.82)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom LumpedHydrophobe_1, pos=[-2.192, 1.450, 0.182], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[-2.192, 1.450, 0.182], label="LumpedHydrophobe 1 (0.72)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom LumpedHydrophobe_2, pos=[3.871, 0.431, 1.178], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_2
group ph4_LumpedHydrophobe, LumpedHydrophobe_2
pseudoatom LumpedHydrophobe_2_ctr, pos=[3.871, 0.431, 1.178], label="LumpedHydrophobe 2 (0.64)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_2_ctr
group ph4_centers, LumpedHydrophobe_2_ctr
pseudoatom Aromatic_2, pos=[3.848, 0.435, 1.254], vdw=1.250
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[3.848, 0.435, 1.254], label="Aromatic 2 (0.60)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom Acceptor_2, pos=[5.609, -2.151, 1.179], vdw=1.250
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[5.609, -2.151, 1.179], label="Acceptor 2 (0.54)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom LumpedHydrophobe_3, pos=[-6.159, 0.391, -0.866], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_3
group ph4_LumpedHydrophobe, LumpedHydrophobe_3
pseudoatom LumpedHydrophobe_3_ctr, pos=[-6.159, 0.391, -0.866], label="LumpedHydrophobe 3 (0.50)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_3_ctr
group ph4_centers, LumpedHydrophobe_3_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
