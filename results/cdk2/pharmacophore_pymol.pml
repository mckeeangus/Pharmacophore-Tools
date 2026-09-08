# cdk2 — ensemble pharmacophore (3 features)
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

pseudoatom Acceptor_1, pos=[-1.690, -3.908, -1.599], vdw=1.250
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[-1.690, -3.908, -1.599], label="Acceptor 1 (0.63)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Aromatic_1, pos=[-1.525, -2.649, -0.769], vdw=1.250
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[-1.525, -2.649, -0.769], label="Aromatic 1 (0.55)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Donor_1, pos=[2.434, 3.534, 0.523], vdw=1.250
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[2.434, 3.534, 0.523], label="Donor 1 (0.53)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
set surface_quality, 2
flag ignore, ph4_*, clear
show mesh, ph4_*
hide mesh, ph4_centers
show nb_spheres, ph4_centers
orient
