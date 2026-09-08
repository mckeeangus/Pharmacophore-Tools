# esr1/lbp__negative — ensemble pharmacophore (49 features)
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

pseudoatom Aromatic_1, pos=[22.700, -11.572, 3.702], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[22.700, -11.572, 3.702], label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom LumpedHydrophobe_1, pos=[22.697, -11.574, 3.705], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[22.697, -11.574, 3.705], label="LumpedHydrophobe 1 (1.00)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom Aromatic_2, pos=[25.829, -9.601, 6.632], vdw=1.250
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[25.829, -9.601, 6.632], label="Aromatic 2 (0.95)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom LumpedHydrophobe_2, pos=[25.828, -9.605, 6.634], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_2
group ph4_LumpedHydrophobe, LumpedHydrophobe_2
pseudoatom LumpedHydrophobe_2_ctr, pos=[25.828, -9.605, 6.634], label="LumpedHydrophobe 2 (0.95)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_2_ctr
group ph4_centers, LumpedHydrophobe_2_ctr
pseudoatom Donor_1, pos=[20.459, -10.994, 1.698], vdw=1.250
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[20.459, -10.994, 1.698], label="Donor 1 (0.76)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Acceptor_1, pos=[20.470, -11.248, 1.696], vdw=1.250
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[20.470, -11.248, 1.696], label="Acceptor 1 (0.76)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Acceptor_2, pos=[27.401, -7.290, 6.747], vdw=1.250
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[27.401, -7.290, 6.747], label="Acceptor 2 (0.76)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom PosIonizable_1, pos=[28.171, -3.950, 5.843], vdw=1.250
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom PosIonizable_1_ctr, pos=[28.171, -3.950, 5.843], label="PosIonizable 1 (0.57)"
color ph4_PosIonizable, PosIonizable_1_ctr
group ph4_centers, PosIonizable_1_ctr
pseudoatom Acceptor_3, pos=[25.403, -14.237, 7.691], vdw=1.250
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_3_ctr, pos=[25.403, -14.237, 7.691], label="Acceptor 3 (0.52)"
color ph4_Acceptor, Acceptor_3_ctr
group ph4_centers, Acceptor_3_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
