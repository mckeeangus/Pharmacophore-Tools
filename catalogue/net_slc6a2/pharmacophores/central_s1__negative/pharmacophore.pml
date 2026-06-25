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

pseudoatom LumpedHydrophobe_0, pos=[130.519, 131.009, 131.655], vdw=2.441
color ph4_LumpedHydrophobe, LumpedHydrophobe_0
group ph4_LumpedHydrophobe, LumpedHydrophobe_0
pseudoatom Donor_1, pos=[129.756, 126.559, 133.210], vdw=2.480
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
