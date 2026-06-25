# hiv1_protease/active_site__negative — ensemble pharmacophore (9 features)
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
pseudoatom Acceptor_1, pos=[-8.576, 15.456, 25.814], vdw=1.669
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[-9.271, 15.544, 30.658], vdw=1.418
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[-11.699, 15.890, 34.988], vdw=1.671
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_4, pos=[-7.996, 17.968, 20.765], vdw=1.639
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom LumpedHydrophobe_5, pos=[-5.257, 18.247, 26.717], vdw=1.155
color ph4_LumpedHydrophobe, LumpedHydrophobe_5
group ph4_LumpedHydrophobe, LumpedHydrophobe_5
pseudoatom LumpedHydrophobe_6, pos=[-12.913, 13.698, 28.862], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_6
group ph4_LumpedHydrophobe, LumpedHydrophobe_6
pseudoatom LumpedHydrophobe_7, pos=[-8.824, 16.495, 22.534], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_7
group ph4_LumpedHydrophobe, LumpedHydrophobe_7
pseudoatom LumpedHydrophobe_8, pos=[-9.829, 15.970, 33.322], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_8
group ph4_LumpedHydrophobe, LumpedHydrophobe_8
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
