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
set_color ph4_ExcludedVolume, [0.55, 0.55, 0.55]

pseudoatom Donor_1, pos=[86.966, 136.645, 140.149], vdw=1.818, label="Donor 1 (1.00)"
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_1, pos=[90.984, 132.432, 132.950], vdw=1.374, label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[93.433, 134.595, 136.779], vdw=1.090, label="Acceptor 2 (1.00)"
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Aromatic_1, pos=[91.315, 131.284, 133.783], vdw=1.100, label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Acceptor_3, pos=[92.818, 136.613, 135.127], vdw=1.000, label="Acceptor 3 (1.00)"
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Aromatic_2, pos=[90.128, 135.700, 137.770], vdw=1.000, label="Aromatic 2 (1.00)"
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Donor_2, pos=[91.898, 134.778, 134.190], vdw=1.000, label="Donor 2 (0.67)"
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Acceptor_4, pos=[89.660, 136.608, 135.288], vdw=1.000, label="Acceptor 4 (0.67)"
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_5, pos=[90.923, 127.695, 134.119], vdw=1.000, label="Acceptor 5 (0.67)"
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom LumpedHydrophobe_1, pos=[90.502, 124.464, 133.206], vdw=1.000, label="LumpedHydrophobe 1 (0.67)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
