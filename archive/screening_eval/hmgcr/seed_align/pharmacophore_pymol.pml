# hmgcr/seed_align — ensemble pharmacophore (8 features)
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

pseudoatom Acceptor_1, pos=[19.513, -25.080, 13.149], vdw=1.250
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[19.513, -25.080, 13.149], label="Acceptor 1 (0.76)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Aromatic_1, pos=[17.533, -25.190, 15.600], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[17.533, -25.190, 15.600], label="Aromatic 1 (0.82)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Donor_1, pos=[14.291, -25.679, 15.719], vdw=1.250
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[14.291, -25.679, 15.719], label="Donor 1 (0.80)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Aromatic_2, pos=[20.542, -22.256, 16.600], vdw=1.250
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[20.542, -22.256, 16.600], label="Aromatic 2 (0.76)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom LumpedHydrophobe_1, pos=[17.511, -24.730, 16.191], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[17.511, -24.730, 16.191], label="LumpedHydrophobe 1 (0.76)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom Acceptor_2, pos=[14.494, -26.987, 14.174], vdw=1.250
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[14.494, -26.987, 14.174], label="Acceptor 2 (0.72)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom NegIonizable_1, pos=[21.067, -19.184, 17.191], vdw=1.250
color ph4_NegIonizable, NegIonizable_1
group ph4_NegIonizable, NegIonizable_1
pseudoatom NegIonizable_1_ctr, pos=[21.067, -19.184, 17.191], label="NegIonizable 1 (0.68)"
color ph4_NegIonizable, NegIonizable_1_ctr
group ph4_centers, NegIonizable_1_ctr
pseudoatom Donor_2, pos=[18.279, -25.710, 11.785], vdw=1.250
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_2_ctr, pos=[18.279, -25.710, 11.785], label="Donor 2 (0.66)"
color ph4_Donor, Donor_2_ctr
group ph4_centers, Donor_2_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
