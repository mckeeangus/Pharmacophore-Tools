# cavab/dhp_site__negative — ensemble pharmacophore (4 features)
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

pseudoatom Acceptor_1, pos=[25.462, 167.265, 14.213], vdw=1.680, label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom LumpedHydrophobe_1, pos=[25.509, 164.696, 10.056], vdw=1.894, label="LumpedHydrophobe 1 (1.00)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom Donor_1, pos=[25.632, 162.997, 15.217], vdw=1.404, label="Donor 1 (1.00)"
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[27.775, 164.940, 18.823], vdw=1.445, label="Donor 2 (0.67)"
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
