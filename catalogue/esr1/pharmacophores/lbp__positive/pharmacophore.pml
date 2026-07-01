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

pseudoatom Donor_1, pos=[21.229, -11.142, 2.618], vdw=1.811, label="Donor 1 (1.00)"
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom LumpedHydrophobe_1, pos=[22.511, -11.502, 4.561], vdw=1.000, label="LumpedHydrophobe 1 (1.00)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom Donor_2, pos=[26.647, -12.030, 10.316], vdw=2.316, label="Donor 2 (0.81)"
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom LumpedHydrophobe_2, pos=[25.269, -11.750, 8.474], vdw=1.362, label="LumpedHydrophobe 2 (0.62)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_2
group ph4_LumpedHydrophobe, LumpedHydrophobe_2
pseudoatom Acceptor_1, pos=[23.217, -13.094, 7.487], vdw=1.000, label="Acceptor 1 (0.56)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
