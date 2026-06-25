# nachr_a4b2/orthosteric__neutral — ensemble pharmacophore (3 features)
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

pseudoatom Donor_0, pos=[170.408, 119.399, 182.057], vdw=2.785
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[169.614, 120.201, 184.976], vdw=3.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[163.229, 124.030, 181.111], vdw=2.474
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
