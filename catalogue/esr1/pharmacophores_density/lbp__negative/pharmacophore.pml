# esr1/lbp__negative — ensemble pharmacophore (48 features)
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

pseudoatom Acceptor_1, pos=[24.069, -13.082, 11.359], vdw=0.500
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[24.069, -13.082, 11.359], label="Acceptor 1 (0.64)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Aromatic_1, pos=[26.230, -9.567, 6.986], vdw=0.500
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[26.230, -9.567, 6.986], label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Aromatic_2, pos=[22.342, -11.633, 3.839], vdw=0.500
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[22.342, -11.633, 3.839], label="Aromatic 2 (1.00)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom Acceptor_2, pos=[27.315, -7.344, 7.054], vdw=0.500
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[27.315, -7.344, 7.054], label="Acceptor 2 (0.83)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom Donor_1, pos=[20.565, -10.977, 1.734], vdw=0.500
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[20.565, -10.977, 1.734], label="Donor 1 (0.76)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Aromatic_3, pos=[25.333, -13.964, 10.239], vdw=0.500
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Aromatic_3_ctr, pos=[25.333, -13.964, 10.239], label="Aromatic 3 (0.74)"
color ph4_Aromatic, Aromatic_3_ctr
group ph4_centers, Aromatic_3_ctr
pseudoatom Acceptor_3, pos=[25.586, -14.237, 7.216], vdw=0.500
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_3_ctr, pos=[25.586, -14.237, 7.216], label="Acceptor 3 (0.74)"
color ph4_Acceptor, Acceptor_3_ctr
group ph4_centers, Acceptor_3_ctr
pseudoatom PosIonizable_1, pos=[28.236, -3.955, 5.908], vdw=0.500
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom PosIonizable_1_ctr, pos=[28.236, -3.955, 5.908], label="PosIonizable 1 (0.64)"
color ph4_PosIonizable, PosIonizable_1_ctr
group ph4_centers, PosIonizable_1_ctr
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
