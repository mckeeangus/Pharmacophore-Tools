# nav1_7_pore/pore_site__negative — ensemble pharmacophore (4 features)
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

pseudoatom Acceptor_0, pos=[122.639, 123.538, 104.519], vdw=2.413
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom LumpedHydrophobe_1, pos=[122.774, 125.184, 108.019], vdw=1.099
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom Donor_2, pos=[121.598, 124.599, 104.075], vdw=1.798
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Aromatic_3, pos=[123.173, 124.813, 107.114], vdw=1.000
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
