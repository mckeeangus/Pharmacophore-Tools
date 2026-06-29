# esr1/lbp__positive — ensemble pharmacophore (5 features)
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

pseudoatom LumpedHydrophobe_0, pos=[22.511, -11.502, 4.561], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_0
group ph4_LumpedHydrophobe, LumpedHydrophobe_0
pseudoatom Donor_1, pos=[21.449, -10.950, 2.140], vdw=1.504
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[22.667, -13.203, 7.636], vdw=1.869
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Donor_3, pos=[26.728, -11.870, 10.265], vdw=2.286
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom LumpedHydrophobe_4, pos=[25.269, -11.750, 8.474], vdw=1.362
color ph4_LumpedHydrophobe, LumpedHydrophobe_4
group ph4_LumpedHydrophobe, LumpedHydrophobe_4
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
