# gaba_a/bzd_site__positive — ensemble pharmacophore (4 features)
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

pseudoatom Aromatic_1, pos=[236.806, 214.104, 243.425], vdw=1.160, label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom LumpedHydrophobe_1, pos=[237.741, 215.201, 238.627], vdw=1.603, label="LumpedHydrophobe 1 (1.00)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom Acceptor_1, pos=[240.062, 218.267, 240.197], vdw=1.054, label="Acceptor 1 (0.67)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Aromatic_2, pos=[239.373, 216.656, 239.297], vdw=1.000, label="Aromatic 2 (0.67)"
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
