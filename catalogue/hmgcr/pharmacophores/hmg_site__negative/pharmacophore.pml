# hmgcr/hmg_site__negative — ensemble pharmacophore (18 features)
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

pseudoatom Donor_0, pos=[13.527, 4.701, 14.441], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[14.839, 6.577, 11.023], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[21.606, 11.423, 14.702], vdw=1.265
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_3, pos=[14.018, 1.801, 16.113], vdw=1.000
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Donor_4, pos=[16.184, 2.602, 16.215], vdw=1.000
color ph4_Donor, Donor_4
group ph4_Donor, Donor_4
pseudoatom Acceptor_5, pos=[15.101, 2.221, 16.156], vdw=1.123
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Acceptor_6, pos=[21.574, 9.516, 13.916], vdw=1.363
color ph4_Acceptor, Acceptor_6
group ph4_Acceptor, Acceptor_6
pseudoatom Acceptor_7, pos=[13.527, 4.701, 14.441], vdw=1.000
color ph4_Acceptor, Acceptor_7
group ph4_Acceptor, Acceptor_7
pseudoatom Acceptor_8, pos=[14.839, 6.577, 11.023], vdw=1.000
color ph4_Acceptor, Acceptor_8
group ph4_Acceptor, Acceptor_8
pseudoatom Acceptor_9, pos=[13.795, 7.670, 19.145], vdw=1.000
color ph4_Acceptor, Acceptor_9
group ph4_Acceptor, Acceptor_9
pseudoatom Acceptor_10, pos=[18.280, 9.988, 16.762], vdw=2.584
color ph4_Acceptor, Acceptor_10
group ph4_Acceptor, Acceptor_10
pseudoatom NegIonizable_11, pos=[15.156, 2.301, 15.975], vdw=1.000
color ph4_NegIonizable, NegIonizable_11
group ph4_NegIonizable, NegIonizable_11
pseudoatom Aromatic_12, pos=[18.612, 9.310, 14.566], vdw=1.000
color ph4_Aromatic, Aromatic_12
group ph4_Aromatic, Aromatic_12
pseudoatom Aromatic_13, pos=[15.650, 8.319, 17.263], vdw=1.000
color ph4_Aromatic, Aromatic_13
group ph4_Aromatic, Aromatic_13
pseudoatom Aromatic_14, pos=[24.373, 12.416, 13.584], vdw=1.348
color ph4_Aromatic, Aromatic_14
group ph4_Aromatic, Aromatic_14
pseudoatom LumpedHydrophobe_15, pos=[19.109, 9.038, 11.465], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_15
group ph4_LumpedHydrophobe, LumpedHydrophobe_15
pseudoatom LumpedHydrophobe_16, pos=[15.650, 8.319, 17.263], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_16
group ph4_LumpedHydrophobe, LumpedHydrophobe_16
pseudoatom LumpedHydrophobe_17, pos=[24.373, 12.416, 13.584], vdw=1.348
color ph4_LumpedHydrophobe, LumpedHydrophobe_17
group ph4_LumpedHydrophobe, LumpedHydrophobe_17
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
