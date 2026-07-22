# hmgcr/hmg_site__negative — ensemble pharmacophore (49 features)
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

pseudoatom Donor_1, pos=[13.370, 4.427, 14.837], vdw=1.250
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[13.370, 4.427, 14.837], label="Donor 1 (1.00)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Donor_2, pos=[14.762, 6.492, 10.697], vdw=1.250
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_2_ctr, pos=[14.762, 6.492, 10.697], label="Donor 2 (1.00)"
color ph4_Donor, Donor_2_ctr
group ph4_centers, Donor_2_ctr
pseudoatom NegIonizable_1, pos=[14.774, 2.030, 15.802], vdw=1.250
color ph4_NegIonizable, NegIonizable_1
group ph4_NegIonizable, NegIonizable_1
pseudoatom NegIonizable_1_ctr, pos=[14.774, 2.030, 15.802], label="NegIonizable 1 (1.00)"
color ph4_NegIonizable, NegIonizable_1_ctr
group ph4_centers, NegIonizable_1_ctr
pseudoatom Aromatic_1, pos=[18.702, 9.308, 15.253], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[18.702, 9.308, 15.253], label="Aromatic 1 (0.89)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Acceptor_1, pos=[14.263, 8.052, 18.810], vdw=1.250
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[14.263, 8.052, 18.810], label="Acceptor 1 (0.83)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Aromatic_2, pos=[15.470, 8.142, 17.434], vdw=1.250
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[15.470, 8.142, 17.434], label="Aromatic 2 (0.83)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom LumpedHydrophobe_1, pos=[19.136, 8.935, 11.420], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[19.136, 8.935, 11.420], label="LumpedHydrophobe 1 (0.83)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom Donor_3, pos=[21.347, 11.266, 14.752], vdw=1.250
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Donor_3_ctr, pos=[21.347, 11.266, 14.752], label="Donor 3 (0.56)"
color ph4_Donor, Donor_3_ctr
group ph4_centers, Donor_3_ctr
pseudoatom Aromatic_3, pos=[24.417, 12.308, 13.694], vdw=1.250
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Aromatic_3_ctr, pos=[24.417, 12.308, 13.694], label="Aromatic 3 (0.56)"
color ph4_Aromatic, Aromatic_3_ctr
group ph4_centers, Aromatic_3_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
