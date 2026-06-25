# ca2/active_site__negative — ensemble pharmacophore (5 features)
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

pseudoatom Acceptor_0, pos=[-5.272, 1.153, 17.993], vdw=1.000
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom Acceptor_1, pos=[-7.225, 1.098, 16.563], vdw=1.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Aromatic_2, pos=[-4.761, 3.525, 15.031], vdw=1.000
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom LumpedHydrophobe_3, pos=[-4.771, 3.512, 14.974], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_3
group ph4_LumpedHydrophobe, LumpedHydrophobe_3
pseudoatom Donor_4, pos=[-5.360, -0.377, 16.079], vdw=1.000
color ph4_Donor, Donor_4
group ph4_Donor, Donor_4
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
