# cox2/cox_channel__negative — ensemble pharmacophore (8 features)
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

pseudoatom Donor_0, pos=[27.911, 4.591, 32.772], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[24.754, 3.590, 32.885], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[26.684, 4.278, 32.470], vdw=2.442
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom NegIonizable_3, pos=[28.031, 4.738, 32.943], vdw=1.000
color ph4_NegIonizable, NegIonizable_3
group ph4_NegIonizable, NegIonizable_3
pseudoatom Aromatic_4, pos=[25.683, 4.575, 35.186], vdw=1.000
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Aromatic_5, pos=[22.877, 2.248, 31.852], vdw=1.000
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom LumpedHydrophobe_6, pos=[25.683, 4.575, 35.186], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_6
group ph4_LumpedHydrophobe, LumpedHydrophobe_6
pseudoatom LumpedHydrophobe_7, pos=[22.877, 2.248, 31.852], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_7
group ph4_LumpedHydrophobe, LumpedHydrophobe_7
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
