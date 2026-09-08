# hiv1_protease — ensemble pharmacophore (8 features)
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

pseudoatom Aromatic_1, pos=[3.306, -1.901, 0.118], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[3.306, -1.901, 0.118], label="Aromatic 1 (0.88)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom LumpedHydrophobe_1, pos=[3.309, -1.909, 0.108], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[3.309, -1.909, 0.108], label="LumpedHydrophobe 1 (0.86)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom Acceptor_1, pos=[-3.166, -1.963, 2.509], vdw=1.250
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[-3.166, -1.963, 2.509], label="Acceptor 1 (0.72)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Acceptor_2, pos=[-1.157, -0.971, -1.467], vdw=1.250
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[-1.157, -0.971, -1.467], label="Acceptor 2 (0.72)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom Aromatic_2, pos=[-0.607, 2.059, 1.133], vdw=1.250
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[-0.607, 2.059, 1.133], label="Aromatic 2 (0.68)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom LumpedHydrophobe_2, pos=[-0.616, 2.056, 1.139], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_2
group ph4_LumpedHydrophobe, LumpedHydrophobe_2
pseudoatom LumpedHydrophobe_2_ctr, pos=[-0.616, 2.056, 1.139], label="LumpedHydrophobe 2 (0.66)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_2_ctr
group ph4_centers, LumpedHydrophobe_2_ctr
pseudoatom LumpedHydrophobe_3, pos=[-4.635, -0.912, -0.837], vdw=1.250
color ph4_LumpedHydrophobe, LumpedHydrophobe_3
group ph4_LumpedHydrophobe, LumpedHydrophobe_3
pseudoatom LumpedHydrophobe_3_ctr, pos=[-4.635, -0.912, -0.837], label="LumpedHydrophobe 3 (0.66)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_3_ctr
group ph4_centers, LumpedHydrophobe_3_ctr
pseudoatom Aromatic_3, pos=[-4.637, -0.918, -0.843], vdw=1.250
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Aromatic_3_ctr, pos=[-4.637, -0.918, -0.843], label="Aromatic 3 (0.60)"
color ph4_Aromatic, Aromatic_3_ctr
group ph4_centers, Aromatic_3_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
