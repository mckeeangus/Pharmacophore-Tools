# hiv1_protease/active_site__negative — ensemble pharmacophore (49 features)
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

pseudoatom Acceptor_1, pos=[-10.665, 19.107, 27.506], vdw=1.250
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[-10.665, 19.107, 27.506], label="Acceptor 1 (0.84)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Donor_1, pos=[-11.060, 18.626, 28.248], vdw=1.250
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[-11.060, 18.626, 28.248], label="Donor 1 (0.81)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Acceptor_2, pos=[-8.588, 15.169, 26.433], vdw=1.250
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[-8.588, 15.169, 26.433], label="Acceptor 2 (0.69)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom LumpedHydrophobe_1, pos=[-13.066, 13.120, 28.743], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[-13.066, 13.120, 28.743], label="LumpedHydrophobe 1 (0.66)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom Aromatic_1, pos=[-13.072, 13.068, 29.170], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[-13.072, 13.068, 29.170], label="Aromatic 1 (0.62)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom LumpedHydrophobe_2, pos=[-5.097, 18.058, 26.681], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_2
group ph4_LumpedHydrophobe, LumpedHydrophobe_2
pseudoatom LumpedHydrophobe_2_ctr, pos=[-5.097, 18.058, 26.681], label="LumpedHydrophobe 2 (0.62)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_2_ctr
group ph4_centers, LumpedHydrophobe_2_ctr
pseudoatom LumpedHydrophobe_3, pos=[-9.043, 16.109, 22.682], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_3
group ph4_LumpedHydrophobe, LumpedHydrophobe_3
pseudoatom LumpedHydrophobe_3_ctr, pos=[-9.043, 16.109, 22.682], label="LumpedHydrophobe 3 (0.62)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_3_ctr
group ph4_centers, LumpedHydrophobe_3_ctr
pseudoatom Aromatic_2, pos=[-5.013, 18.068, 26.217], vdw=1.250
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[-5.013, 18.068, 26.217], label="Aromatic 2 (0.53)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom LumpedHydrophobe_4, pos=[-10.044, 16.016, 33.617], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_4
group ph4_LumpedHydrophobe, LumpedHydrophobe_4
pseudoatom LumpedHydrophobe_4_ctr, pos=[-10.044, 16.016, 33.617], label="LumpedHydrophobe 4 (0.50)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_4_ctr
group ph4_centers, LumpedHydrophobe_4_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
