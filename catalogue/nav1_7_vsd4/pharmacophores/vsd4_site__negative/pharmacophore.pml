# nav1_7_vsd4/vsd4_site__negative — ensemble pharmacophore (13 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/vsd4_site__negative/8F0P_X7L_A1610.mol2, compounds
load ../../groups/vsd4_site__negative/8F0R_X7W_A1606.mol2, compounds
load ../../groups/vsd4_site__negative/8F0S_X80_A1605.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[86.966, 136.645, 140.149], vdw=1.818
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[91.926, 134.437, 134.633], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[90.984, 132.432, 132.950], vdw=1.374
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[93.433, 134.595, 136.779], vdw=1.090
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_4, pos=[92.818, 136.613, 135.127], vdw=1.000
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_5, pos=[89.660, 136.608, 135.288], vdw=1.000
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Acceptor_6, pos=[90.923, 127.695, 134.119], vdw=1.000
color ph4_Acceptor, Acceptor_6
group ph4_Acceptor, Acceptor_6
pseudoatom PosIonizable_7, pos=[86.726, 137.674, 141.231], vdw=1.000
color ph4_PosIonizable, PosIonizable_7
group ph4_PosIonizable, PosIonizable_7
pseudoatom Aromatic_8, pos=[91.315, 131.284, 133.783], vdw=1.100
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
pseudoatom Aromatic_9, pos=[90.128, 135.700, 137.770], vdw=1.000
color ph4_Aromatic, Aromatic_9
group ph4_Aromatic, Aromatic_9
pseudoatom Hydrophobe_10, pos=[90.840, 135.403, 137.373], vdw=1.154
color ph4_Hydrophobe, Hydrophobe_10
group ph4_Hydrophobe, Hydrophobe_10
pseudoatom Hydrophobe_11, pos=[91.279, 130.915, 134.781], vdw=1.180
color ph4_Hydrophobe, Hydrophobe_11
group ph4_Hydrophobe, Hydrophobe_11
pseudoatom Hydrophobe_12, pos=[90.874, 125.624, 133.081], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_12
group ph4_Hydrophobe, Hydrophobe_12
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
