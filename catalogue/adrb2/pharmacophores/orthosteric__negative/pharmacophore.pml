# adrb2/orthosteric__negative — ensemble pharmacophore (7 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__negative/2RH1_CAU_A408.mol2, compounds
load ../../groups/orthosteric__negative/3NY9_JSZ_A1203.mol2, compounds
load ../../groups/orthosteric__negative/6PS3_CVD_A1201.mol2, compounds
load ../../groups/orthosteric__negative/6PS4_JRZ_A1201.mol2, compounds
load ../../groups/orthosteric__negative/6PS5_SNP_A1201.mol2, compounds
load ../../groups/orthosteric__negative/6PS6_TIM_A1201.mol2, compounds
load ../../groups/orthosteric__negative/9RKF_A1JHU_A520.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[-33.351, 10.866, 8.168], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[-33.547, 8.148, 7.571], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[-30.016, 10.572, 7.208], vdw=1.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[-33.351, 10.866, 8.168], vdw=1.000
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom PosIonizable_4, pos=[-33.550, 8.294, 7.442], vdw=1.000
color ph4_PosIonizable, PosIonizable_4
group ph4_PosIonizable, PosIonizable_4
pseudoatom Aromatic_5, pos=[-27.301, 9.857, 6.392], vdw=2.085
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom Hydrophobe_6, pos=[-27.404, 10.344, 6.197], vdw=1.397
color ph4_Hydrophobe, Hydrophobe_6
group ph4_Hydrophobe, Hydrophobe_6
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
