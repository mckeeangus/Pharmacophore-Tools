# cox2/cox_channel__negative — ensemble pharmacophore (3 features)
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

pseudoatom Acceptor_0, pos=[26.512, 4.334, 32.277], vdw=2.576
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom Aromatic_1, pos=[25.683, 4.575, 35.186], vdw=1.000
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_2, pos=[22.877, 2.248, 31.852], vdw=1.000
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
