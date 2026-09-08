# adrb2/orthosteric__positive — ensemble pharmacophore (47 features)
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

pseudoatom Aromatic_1, pos=[-29.082, 10.359, 6.230], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[-29.082, 10.359, 6.230], label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom LumpedHydrophobe_1, pos=[-29.072, 10.355, 6.230], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[-29.072, 10.355, 6.230], label="LumpedHydrophobe 1 (1.00)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom Donor_1, pos=[-26.461, 10.789, 5.334], vdw=1.250
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[-26.461, 10.789, 5.334], label="Donor 1 (0.91)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Donor_2, pos=[-32.443, 10.820, 7.314], vdw=1.250
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_2_ctr, pos=[-32.443, 10.820, 7.314], label="Donor 2 (0.91)"
color ph4_Donor, Donor_2_ctr
group ph4_centers, Donor_2_ctr
pseudoatom Acceptor_1, pos=[-26.456, 10.813, 5.326], vdw=1.250
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[-26.456, 10.813, 5.326], label="Acceptor 1 (0.91)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Acceptor_2, pos=[-32.451, 10.819, 7.314], vdw=1.250
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[-32.451, 10.819, 7.314], label="Acceptor 2 (0.91)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom PosIonizable_1, pos=[-33.191, 8.634, 6.996], vdw=1.250
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom PosIonizable_1_ctr, pos=[-33.191, 8.634, 6.996], label="PosIonizable 1 (0.91)"
color ph4_PosIonizable, PosIonizable_1_ctr
group ph4_centers, PosIonizable_1_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
