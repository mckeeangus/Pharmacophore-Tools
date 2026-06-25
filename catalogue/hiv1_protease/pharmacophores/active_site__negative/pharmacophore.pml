# hiv1_protease/active_site__negative — ensemble pharmacophore (16 features)
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

pseudoatom Donor_0, pos=[-10.271, 17.797, 28.033], vdw=2.219
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[-6.995, 17.314, 21.672], vdw=2.447
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[-11.319, 14.529, 34.904], vdw=2.259
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Acceptor_3, pos=[-8.576, 15.456, 25.814], vdw=1.669
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_4, pos=[-10.865, 19.010, 27.934], vdw=1.291
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_5, pos=[-9.271, 15.544, 30.658], vdw=1.418
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Acceptor_6, pos=[-11.699, 15.890, 34.988], vdw=1.671
color ph4_Acceptor, Acceptor_6
group ph4_Acceptor, Acceptor_6
pseudoatom Acceptor_7, pos=[-7.996, 17.968, 20.765], vdw=1.639
color ph4_Acceptor, Acceptor_7
group ph4_Acceptor, Acceptor_7
pseudoatom Aromatic_8, pos=[-4.877, 18.168, 26.406], vdw=1.000
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
pseudoatom Aromatic_9, pos=[-12.929, 13.433, 29.071], vdw=1.000
color ph4_Aromatic, Aromatic_9
group ph4_Aromatic, Aromatic_9
pseudoatom Aromatic_10, pos=[-8.630, 16.553, 22.488], vdw=1.000
color ph4_Aromatic, Aromatic_10
group ph4_Aromatic, Aromatic_10
pseudoatom Aromatic_11, pos=[-9.965, 15.850, 33.482], vdw=1.022
color ph4_Aromatic, Aromatic_11
group ph4_Aromatic, Aromatic_11
pseudoatom LumpedHydrophobe_12, pos=[-5.257, 18.247, 26.717], vdw=1.155
color ph4_LumpedHydrophobe, LumpedHydrophobe_12
group ph4_LumpedHydrophobe, LumpedHydrophobe_12
pseudoatom LumpedHydrophobe_13, pos=[-12.913, 13.698, 28.862], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_13
group ph4_LumpedHydrophobe, LumpedHydrophobe_13
pseudoatom LumpedHydrophobe_14, pos=[-8.824, 16.495, 22.534], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_14
group ph4_LumpedHydrophobe, LumpedHydrophobe_14
pseudoatom LumpedHydrophobe_15, pos=[-9.829, 15.970, 33.322], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_15
group ph4_LumpedHydrophobe, LumpedHydrophobe_15
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
