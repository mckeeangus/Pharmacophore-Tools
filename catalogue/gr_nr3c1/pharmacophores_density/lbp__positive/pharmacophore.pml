# gr_nr3c1/lbp__positive — ensemble pharmacophore (47 features)
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

pseudoatom Acceptor_1, pos=[28.086, 6.763, 16.702], vdw=0.500
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[28.086, 6.763, 16.702], label="Acceptor 1 (0.95)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Donor_1, pos=[29.017, 5.295, 13.680], vdw=0.500
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[29.017, 5.295, 13.680], label="Donor 1 (0.95)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Acceptor_2, pos=[29.706, 6.772, 12.506], vdw=0.500
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[29.706, 6.772, 12.506], label="Acceptor 2 (0.95)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom Aromatic_1, pos=[31.930, 7.680, 9.505], vdw=0.500
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[31.930, 7.680, 9.505], label="Aromatic 1 (0.65)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Acceptor_3, pos=[31.613, 8.312, 7.334], vdw=0.500
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_3_ctr, pos=[31.613, 8.312, 7.334], label="Acceptor 3 (0.85)"
color ph4_Acceptor, Acceptor_3_ctr
group ph4_centers, Acceptor_3_ctr
pseudoatom Aromatic_2, pos=[27.780, 10.391, 14.542], vdw=0.500
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[27.780, 10.391, 14.542], label="Aromatic 2 (0.65)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom Aromatic_3, pos=[34.443, 9.164, 5.685], vdw=0.500
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Aromatic_3_ctr, pos=[34.443, 9.164, 5.685], label="Aromatic 3 (0.50)"
color ph4_Aromatic, Aromatic_3_ctr
group ph4_centers, Aromatic_3_ctr
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
