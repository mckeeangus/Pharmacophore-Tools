# nav1_7_vsd4/vsd4_site__negative — ensemble pharmacophore (10 features)
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

pseudoatom Acceptor_1, pos=[90.984, 132.432, 132.950], vdw=2.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[90.984, 132.432, 132.950], label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Acceptor_2, pos=[93.433, 134.595, 136.779], vdw=2.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[93.433, 134.595, 136.779], label="Acceptor 2 (1.00)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom Donor_1, pos=[88.061, 135.946, 139.658], vdw=2.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[88.061, 135.946, 139.658], label="Donor 1 (1.00)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Acceptor_3, pos=[92.818, 136.613, 135.127], vdw=2.000
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_3_ctr, pos=[92.818, 136.613, 135.127], label="Acceptor 3 (1.00)"
color ph4_Acceptor, Acceptor_3_ctr
group ph4_centers, Acceptor_3_ctr
pseudoatom Aromatic_1, pos=[90.128, 135.700, 137.770], vdw=2.000
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[90.128, 135.700, 137.770], label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Donor_2, pos=[91.898, 134.778, 134.190], vdw=2.000
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_2_ctr, pos=[91.898, 134.778, 134.190], label="Donor 2 (0.67)"
color ph4_Donor, Donor_2_ctr
group ph4_centers, Donor_2_ctr
pseudoatom Acceptor_4, pos=[89.660, 136.608, 135.288], vdw=2.000
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_4_ctr, pos=[89.660, 136.608, 135.288], label="Acceptor 4 (0.67)"
color ph4_Acceptor, Acceptor_4_ctr
group ph4_centers, Acceptor_4_ctr
pseudoatom Acceptor_5, pos=[90.923, 127.695, 134.119], vdw=2.000
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Acceptor_5_ctr, pos=[90.923, 127.695, 134.119], label="Acceptor 5 (0.67)"
color ph4_Acceptor, Acceptor_5_ctr
group ph4_centers, Acceptor_5_ctr
pseudoatom PosIonizable_1, pos=[86.726, 137.674, 141.231], vdw=2.000
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom PosIonizable_1_ctr, pos=[86.726, 137.674, 141.231], label="PosIonizable 1 (0.67)"
color ph4_PosIonizable, PosIonizable_1_ctr
group ph4_centers, PosIonizable_1_ctr
pseudoatom LumpedHydrophobe_1, pos=[90.502, 124.464, 133.206], vdw=2.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[90.502, 124.464, 133.206], label="LumpedHydrophobe 1 (0.67)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
hide spheres, ph4_centers
show nb_spheres, ph4_centers
orient
