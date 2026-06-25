# chrm2/orthosteric__negative — ensemble pharmacophore (8 features)
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

pseudoatom Donor_0, pos=[132.554, 146.180, 102.159], vdw=2.323
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[139.691, 145.652, 102.101], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[138.842, 144.637, 102.231], vdw=1.570
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[135.104, 145.822, 102.868], vdw=1.857
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom PosIonizable_4, pos=[132.396, 144.975, 102.435], vdw=1.000
color ph4_PosIonizable, PosIonizable_4
group ph4_PosIonizable, PosIonizable_4
pseudoatom Aromatic_5, pos=[137.853, 146.581, 105.624], vdw=1.000
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom Aromatic_6, pos=[138.979, 148.266, 101.347], vdw=1.000
color ph4_Aromatic, Aromatic_6
group ph4_Aromatic, Aromatic_6
pseudoatom LumpedHydrophobe_7, pos=[137.853, 146.581, 105.624], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_7
group ph4_LumpedHydrophobe, LumpedHydrophobe_7
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
