# cox2/cox_channel__negative — ensemble pharmacophore (44 features)
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

pseudoatom Aromatic_1, pos=[25.561, 4.644, 35.211], vdw=0.500
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[25.561, 4.644, 35.211], label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Donor_1, pos=[25.681, 3.897, 32.886], vdw=0.500
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[25.681, 3.897, 32.886], label="Donor 1 (0.80)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom NegIonizable_1, pos=[27.089, 4.282, 32.855], vdw=0.500
color ph4_NegIonizable, NegIonizable_1
group ph4_NegIonizable, NegIonizable_1
pseudoatom NegIonizable_1_ctr, pos=[27.089, 4.282, 32.855], label="NegIonizable 1 (0.80)"
color ph4_NegIonizable, NegIonizable_1_ctr
group ph4_centers, NegIonizable_1_ctr
pseudoatom Aromatic_2, pos=[22.972, 1.257, 32.447], vdw=0.500
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[22.972, 1.257, 32.447], label="Aromatic 2 (0.80)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
