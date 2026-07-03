# net_slc6a2/central_s1__negative — ensemble pharmacophore (2 features)
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

pseudoatom Aromatic_1, pos=[130.475, 130.882, 131.599], vdw=2.000
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[130.475, 130.882, 131.599], label="Aromatic 1 (0.96)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom PosIonizable_1, pos=[130.001, 126.199, 134.125], vdw=2.000
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom PosIonizable_1_ctr, pos=[130.001, 126.199, 134.125], label="PosIonizable 1 (0.68)"
color ph4_PosIonizable, PosIonizable_1_ctr
group ph4_centers, PosIonizable_1_ctr
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
hide spheres, ph4_centers
show nb_spheres, ph4_centers
orient
