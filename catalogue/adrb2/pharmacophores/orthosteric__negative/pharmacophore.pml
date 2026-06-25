# adrb2/orthosteric__negative — ensemble pharmacophore (6 features)
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

pseudoatom Aromatic_0, pos=[-27.301, 9.857, 6.392], vdw=2.085
color ph4_Aromatic, Aromatic_0
group ph4_Aromatic, Aromatic_0
pseudoatom Donor_1, pos=[-33.351, 10.866, 8.168], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[-33.547, 8.148, 7.571], vdw=1.000
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Acceptor_3, pos=[-30.016, 10.572, 7.208], vdw=1.000
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom LumpedHydrophobe_4, pos=[-34.420, 6.262, 7.619], vdw=1.797
color ph4_LumpedHydrophobe, LumpedHydrophobe_4
group ph4_LumpedHydrophobe, LumpedHydrophobe_4
pseudoatom LumpedHydrophobe_5, pos=[-26.861, 7.736, 7.221], vdw=1.551
color ph4_LumpedHydrophobe, LumpedHydrophobe_5
group ph4_LumpedHydrophobe, LumpedHydrophobe_5
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
