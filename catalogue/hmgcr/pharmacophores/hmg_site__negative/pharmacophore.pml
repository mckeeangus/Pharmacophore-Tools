# hmgcr/hmg_site__negative — ensemble pharmacophore (12 features)
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

pseudoatom Acceptor_0, pos=[15.101, 2.221, 16.156], vdw=1.123
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom Acceptor_1, pos=[21.574, 9.516, 13.916], vdw=1.363
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Donor_2, pos=[13.527, 4.701, 14.441], vdw=1.000
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_3, pos=[14.839, 6.577, 11.023], vdw=1.000
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Aromatic_4, pos=[18.612, 9.310, 14.566], vdw=1.000
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Acceptor_5, pos=[13.795, 7.670, 19.145], vdw=1.000
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Aromatic_6, pos=[15.650, 8.319, 17.263], vdw=1.000
color ph4_Aromatic, Aromatic_6
group ph4_Aromatic, Aromatic_6
pseudoatom LumpedHydrophobe_7, pos=[19.109, 9.038, 11.465], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_7
group ph4_LumpedHydrophobe, LumpedHydrophobe_7
pseudoatom Aromatic_8, pos=[24.373, 12.416, 13.584], vdw=1.348
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
pseudoatom Donor_9, pos=[21.606, 11.423, 14.702], vdw=1.265
color ph4_Donor, Donor_9
group ph4_Donor, Donor_9
pseudoatom Donor_10, pos=[14.018, 1.801, 16.113], vdw=1.000
color ph4_Donor, Donor_10
group ph4_Donor, Donor_10
pseudoatom Donor_11, pos=[16.184, 2.602, 16.215], vdw=1.000
color ph4_Donor, Donor_11
group ph4_Donor, Donor_11
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
