# adora2a/orthosteric__neutral — ensemble pharmacophore (7 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__neutral/5OLH_9XT_A1201.mol2, compounds
load ../../groups/orthosteric__neutral/5OLO_9XW_A1201.mol2, compounds
load ../../groups/orthosteric__neutral/6GT3_F9Q_A2401.mol2, compounds
load ../../groups/orthosteric__neutral/8CIC_U30_A1202.mol2, compounds
load ../../groups/orthosteric__neutral/8RW0_JQ9_A1201.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[-2.377, 99.329, 52.024], vdw=2.239
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[3.934, 94.721, 53.562], vdw=1.679
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[0.693, 97.874, 52.954], vdw=1.210
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[-0.913, 95.680, 51.441], vdw=1.000
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Aromatic_4, pos=[0.680, 94.802, 52.108], vdw=2.212
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Aromatic_5, pos=[3.191, 99.138, 56.062], vdw=2.968
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom Hydrophobe_6, pos=[0.665, 93.510, 51.553], vdw=1.968
color ph4_Hydrophobe, Hydrophobe_6
group ph4_Hydrophobe, Hydrophobe_6
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
