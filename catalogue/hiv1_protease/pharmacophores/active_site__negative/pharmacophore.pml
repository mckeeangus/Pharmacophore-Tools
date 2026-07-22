# hiv1_protease/active_site__negative — ensemble pharmacophore (10 features)
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

pseudoatom Donor_1, pos=[-10.338, 17.921, 28.052], vdw=0.500
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[-10.338, 17.921, 28.052], label="Donor 1 (0.88)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Acceptor_1, pos=[-11.954, 14.855, 34.875], vdw=0.500
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[-11.954, 14.855, 34.875], label="Acceptor 1 (0.72)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Acceptor_2, pos=[-8.576, 15.456, 25.814], vdw=0.500
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[-8.576, 15.456, 25.814], label="Acceptor 2 (0.94)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom Acceptor_3, pos=[-10.863, 19.033, 27.920], vdw=0.500
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_3_ctr, pos=[-10.863, 19.033, 27.920], label="Acceptor 3 (0.88)"
color ph4_Acceptor, Acceptor_3_ctr
group ph4_centers, Acceptor_3_ctr
pseudoatom Acceptor_4, pos=[-9.271, 15.544, 30.658], vdw=0.500
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_4_ctr, pos=[-9.271, 15.544, 30.658], label="Acceptor 4 (0.66)"
color ph4_Acceptor, Acceptor_4_ctr
group ph4_centers, Acceptor_4_ctr
pseudoatom Acceptor_5, pos=[-7.976, 17.989, 20.655], vdw=0.500
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Acceptor_5_ctr, pos=[-7.976, 17.989, 20.655], label="Acceptor 5 (0.72)"
color ph4_Acceptor, Acceptor_5_ctr
group ph4_centers, Acceptor_5_ctr
pseudoatom Aromatic_1, pos=[-4.877, 18.168, 26.406], vdw=0.500
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[-4.877, 18.168, 26.406], label="Aromatic 1 (0.66)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Aromatic_2, pos=[-12.929, 13.433, 29.071], vdw=0.500
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[-12.929, 13.433, 29.071], label="Aromatic 2 (0.66)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
pseudoatom Aromatic_3, pos=[-8.630, 16.553, 22.488], vdw=0.500
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Aromatic_3_ctr, pos=[-8.630, 16.553, 22.488], label="Aromatic 3 (0.53)"
color ph4_Aromatic, Aromatic_3_ctr
group ph4_centers, Aromatic_3_ctr
pseudoatom Aromatic_4, pos=[-9.965, 15.850, 33.482], vdw=0.500
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Aromatic_4_ctr, pos=[-9.965, 15.850, 33.482], label="Aromatic 4 (0.53)"
color ph4_Aromatic, Aromatic_4_ctr
group ph4_centers, Aromatic_4_ctr
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
