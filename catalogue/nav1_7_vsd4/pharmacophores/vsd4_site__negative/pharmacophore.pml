# nav1_7_vsd4/vsd4_site__negative — ensemble pharmacophore (10 features)
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

pseudoatom Donor_0, pos=[86.966, 136.645, 140.149], vdw=1.818
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[90.984, 132.432, 132.950], vdw=1.374
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[93.433, 134.595, 136.779], vdw=1.090
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Aromatic_3, pos=[91.315, 131.284, 133.783], vdw=1.100
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Donor_4, pos=[91.926, 134.437, 134.633], vdw=1.000
color ph4_Donor, Donor_4
group ph4_Donor, Donor_4
pseudoatom Acceptor_5, pos=[92.818, 136.613, 135.127], vdw=1.000
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Aromatic_6, pos=[90.128, 135.700, 137.770], vdw=1.000
color ph4_Aromatic, Aromatic_6
group ph4_Aromatic, Aromatic_6
pseudoatom Acceptor_7, pos=[89.660, 136.608, 135.288], vdw=1.000
color ph4_Acceptor, Acceptor_7
group ph4_Acceptor, Acceptor_7
pseudoatom Acceptor_8, pos=[90.923, 127.695, 134.119], vdw=1.000
color ph4_Acceptor, Acceptor_8
group ph4_Acceptor, Acceptor_8
pseudoatom LumpedHydrophobe_9, pos=[90.502, 124.464, 133.206], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_9
group ph4_LumpedHydrophobe, LumpedHydrophobe_9
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
