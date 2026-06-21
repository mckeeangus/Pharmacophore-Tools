# net_slc6a2/central_s1__positive — ensemble pharmacophore (7 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/central_s1__positive/4XP1_LDP_A708.mol2, compounds
load ../../groups/central_s1__positive/4XP6_B40_A601.mol2, compounds
load ../../groups/central_s1__positive/4XP9_1WE_C706.mol2, compounds
load ../../groups/central_s1__positive/8WTV_E5E_A704.mol2, compounds
load ../../groups/central_s1__positive/8XB3_YMN_A701.mol2, compounds
load ../../groups/central_s1__positive/8ZOY_LNR_A701.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[130.541, 127.339, 133.247], vdw=2.142
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[131.331, 132.479, 128.683], vdw=1.680
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[131.032, 133.096, 128.336], vdw=1.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom PosIonizable_3, pos=[130.926, 127.132, 134.495], vdw=1.485
color ph4_PosIonizable, PosIonizable_3
group ph4_PosIonizable, PosIonizable_3
pseudoatom Aromatic_4, pos=[130.602, 130.920, 130.112], vdw=1.000
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Hydrophobe_5, pos=[130.412, 130.629, 130.434], vdw=1.352
color ph4_Hydrophobe, Hydrophobe_5
group ph4_Hydrophobe, Hydrophobe_5
pseudoatom Hydrophobe_6, pos=[130.783, 128.652, 133.009], vdw=1.078
color ph4_Hydrophobe, Hydrophobe_6
group ph4_Hydrophobe, Hydrophobe_6
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
