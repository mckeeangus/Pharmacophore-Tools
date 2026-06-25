# nachr_a4b2/orthosteric__positive — ensemble pharmacophore (4 features)
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

pseudoatom Donor_0, pos=[166.878, 123.394, 186.228], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[171.480, 124.134, 188.452], vdw=1.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom PosIonizable_2, pos=[166.886, 123.379, 186.181], vdw=1.000
color ph4_PosIonizable, PosIonizable_2
group ph4_PosIonizable, PosIonizable_2
pseudoatom Aromatic_3, pos=[170.850, 122.801, 188.266], vdw=1.000
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
