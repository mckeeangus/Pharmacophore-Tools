# hmgcr/hmg_site__negative — ensemble pharmacophore (9 features)
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

pseudoatom Acceptor_1, pos=[21.574, 9.516, 13.916], vdw=1.363, label="Acceptor 1 (0.83)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Donor_1, pos=[14.839, 6.577, 11.023], vdw=1.000, label="Donor 1 (1.00)"
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[13.527, 4.701, 14.441], vdw=1.000, label="Donor 2 (1.00)"
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Acceptor_2, pos=[15.100, 2.240, 16.147], vdw=1.068, label="Acceptor 2 (1.00)"
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Aromatic_1, pos=[18.612, 9.310, 14.566], vdw=1.000, label="Aromatic 1 (0.89)"
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Acceptor_3, pos=[13.795, 7.670, 19.145], vdw=1.000, label="Acceptor 3 (0.83)"
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Aromatic_2, pos=[15.650, 8.319, 17.263], vdw=1.000, label="Aromatic 2 (0.83)"
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom LumpedHydrophobe_1, pos=[19.109, 9.038, 11.465], vdw=1.000, label="LumpedHydrophobe 1 (0.83)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom Aromatic_3, pos=[24.373, 12.416, 13.584], vdw=1.348, label="Aromatic 3 (0.61)"
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
