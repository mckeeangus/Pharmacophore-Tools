# hiv1_protease/active_site__negative — ensemble pharmacophore (11 features)
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

pseudoatom Acceptor_0, pos=[-11.954, 14.855, 34.875], vdw=2.499
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom Acceptor_1, pos=[-8.576, 15.456, 25.814], vdw=1.669
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Donor_2, pos=[-10.919, 19.056, 27.878], vdw=1.219
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Acceptor_3, pos=[-9.271, 15.544, 30.658], vdw=1.418
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_4, pos=[-7.980, 18.019, 20.704], vdw=1.682
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom LumpedHydrophobe_5, pos=[-5.257, 18.247, 26.717], vdw=1.155
color ph4_LumpedHydrophobe, LumpedHydrophobe_5
group ph4_LumpedHydrophobe, LumpedHydrophobe_5
pseudoatom LumpedHydrophobe_6, pos=[-12.913, 13.698, 28.862], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_6
group ph4_LumpedHydrophobe, LumpedHydrophobe_6
pseudoatom Donor_7, pos=[-8.599, 17.270, 26.094], vdw=1.185
color ph4_Donor, Donor_7
group ph4_Donor, Donor_7
pseudoatom Donor_8, pos=[-10.465, 16.242, 29.685], vdw=1.222
color ph4_Donor, Donor_8
group ph4_Donor, Donor_8
pseudoatom LumpedHydrophobe_9, pos=[-8.824, 16.495, 22.534], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_9
group ph4_LumpedHydrophobe, LumpedHydrophobe_9
pseudoatom LumpedHydrophobe_10, pos=[-9.829, 15.970, 33.322], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_10
group ph4_LumpedHydrophobe, LumpedHydrophobe_10
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
