# cox2/seed_align — ensemble pharmacophore (6 features)
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

pseudoatom Donor_1, pos=[170.053, 222.322, 215.871], vdw=1.250
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[170.053, 222.322, 215.871], label="Donor 1 (0.88)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Aromatic_1, pos=[164.383, 219.402, 218.430], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[164.383, 219.402, 218.430], label="Aromatic 1 (0.82)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Aromatic_2, pos=[167.390, 223.254, 218.403], vdw=1.250
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[167.390, 223.254, 218.403], label="Aromatic 2 (0.82)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom LumpedHydrophobe_1, pos=[164.369, 219.402, 218.837], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[164.369, 219.402, 218.837], label="LumpedHydrophobe 1 (0.80)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom NegIonizable_1, pos=[168.968, 221.777, 216.037], vdw=1.250
color ph4_NegIonizable, NegIonizable_1
group ph4_NegIonizable, NegIonizable_1
pseudoatom NegIonizable_1_ctr, pos=[168.968, 221.777, 216.037], label="NegIonizable 1 (0.76)"
color ph4_NegIonizable, NegIonizable_1_ctr
group ph4_centers, NegIonizable_1_ctr
pseudoatom LumpedHydrophobe_2, pos=[167.390, 223.304, 218.792], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_2
group ph4_LumpedHydrophobe, LumpedHydrophobe_2
pseudoatom LumpedHydrophobe_2_ctr, pos=[167.390, 223.304, 218.792], label="LumpedHydrophobe 2 (0.62)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_2_ctr
group ph4_centers, LumpedHydrophobe_2_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
