# cavab/dhp_site__negative — ensemble pharmacophore (6 features)
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

pseudoatom Donor_0, pos=[25.632, 162.997, 15.217], vdw=1.220
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[27.775, 164.940, 18.823], vdw=1.445
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[25.462, 167.265, 14.213], vdw=1.353
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom PosIonizable_3, pos=[27.775, 164.940, 18.823], vdw=1.445
color ph4_PosIonizable, PosIonizable_3
group ph4_PosIonizable, PosIonizable_3
pseudoatom Aromatic_4, pos=[25.395, 164.346, 10.410], vdw=1.000
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom LumpedHydrophobe_5, pos=[25.509, 164.696, 10.056], vdw=1.814
color ph4_LumpedHydrophobe, LumpedHydrophobe_5
group ph4_LumpedHydrophobe, LumpedHydrophobe_5
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
