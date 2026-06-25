# net_slc6a2/central_s1__negative — ensemble pharmacophore (5 features)
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

pseudoatom Donor_0, pos=[129.756, 126.559, 133.210], vdw=2.480
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom PosIonizable_1, pos=[130.001, 126.199, 134.125], vdw=1.163
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom Aromatic_2, pos=[130.475, 130.882, 131.599], vdw=2.571
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom LumpedHydrophobe_3, pos=[130.519, 131.009, 131.655], vdw=2.441
color ph4_LumpedHydrophobe, LumpedHydrophobe_3
group ph4_LumpedHydrophobe, LumpedHydrophobe_3
pseudoatom Acceptor_4, pos=[130.140, 129.479, 132.503], vdw=2.500
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
