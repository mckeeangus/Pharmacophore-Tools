# hmgcr/hmg_site__negative — ensemble pharmacophore (54 features)
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

pseudoatom Donor_1, pos=[13.375, 4.475, 14.742], vdw=1.250
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[13.375, 4.475, 14.742], label="Donor 1 (1.00)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Donor_2, pos=[14.444, 6.459, 10.772], vdw=1.250
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_2_ctr, pos=[14.444, 6.459, 10.772], label="Donor 2 (1.00)"
color ph4_Donor, Donor_2_ctr
group ph4_centers, Donor_2_ctr
pseudoatom Acceptor_1, pos=[13.375, 4.478, 14.747], vdw=1.250
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[13.375, 4.478, 14.747], label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Acceptor_2, pos=[14.453, 6.459, 10.772], vdw=1.250
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[14.453, 6.459, 10.772], label="Acceptor 2 (1.00)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom NegIonizable_1, pos=[14.774, 2.030, 15.802], vdw=1.250
color ph4_NegIonizable, NegIonizable_1
group ph4_NegIonizable, NegIonizable_1
pseudoatom NegIonizable_1_ctr, pos=[14.774, 2.030, 15.802], label="NegIonizable 1 (1.00)"
color ph4_NegIonizable, NegIonizable_1_ctr
group ph4_centers, NegIonizable_1_ctr
pseudoatom Aromatic_1, pos=[18.316, 8.789, 14.929], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[18.316, 8.789, 14.929], label="Aromatic 1 (0.89)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Acceptor_3, pos=[13.445, 7.497, 18.780], vdw=1.250
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_3_ctr, pos=[13.445, 7.497, 18.780], label="Acceptor 3 (0.83)"
color ph4_Acceptor, Acceptor_3_ctr
group ph4_centers, Acceptor_3_ctr
pseudoatom Aromatic_2, pos=[15.405, 7.843, 16.941], vdw=1.250
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[15.405, 7.843, 16.941], label="Aromatic 2 (0.83)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom LumpedHydrophobe_1, pos=[19.294, 8.769, 11.183], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[19.294, 8.769, 11.183], label="LumpedHydrophobe 1 (0.83)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom LumpedHydrophobe_2, pos=[15.367, 7.834, 17.160], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_2
group ph4_LumpedHydrophobe, LumpedHydrophobe_2
pseudoatom LumpedHydrophobe_2_ctr, pos=[15.367, 7.834, 17.160], label="LumpedHydrophobe 2 (0.83)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_2_ctr
group ph4_centers, LumpedHydrophobe_2_ctr
pseudoatom Acceptor_4, pos=[21.367, 9.449, 13.769], vdw=1.250
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_4_ctr, pos=[21.367, 9.449, 13.769], label="Acceptor 4 (0.72)"
color ph4_Acceptor, Acceptor_4_ctr
group ph4_centers, Acceptor_4_ctr
pseudoatom Donor_3, pos=[21.361, 11.402, 14.745], vdw=1.250
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Donor_3_ctr, pos=[21.361, 11.402, 14.745], label="Donor 3 (0.56)"
color ph4_Donor, Donor_3_ctr
group ph4_centers, Donor_3_ctr
pseudoatom Aromatic_3, pos=[24.326, 11.836, 13.862], vdw=1.250
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Aromatic_3_ctr, pos=[24.326, 11.836, 13.862], label="Aromatic 3 (0.56)"
color ph4_Aromatic, Aromatic_3_ctr
group ph4_centers, Aromatic_3_ctr
pseudoatom LumpedHydrophobe_3, pos=[24.318, 11.830, 14.088], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_3
group ph4_LumpedHydrophobe, LumpedHydrophobe_3
pseudoatom LumpedHydrophobe_3_ctr, pos=[24.318, 11.830, 14.088], label="LumpedHydrophobe 3 (0.56)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_3_ctr
group ph4_centers, LumpedHydrophobe_3_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
