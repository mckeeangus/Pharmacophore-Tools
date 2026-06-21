# adrb2/orthosteric__positive — ensemble pharmacophore (11 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__positive/4LDE_P0G_A1401.mol2, compounds
load ../../groups/orthosteric__positive/4LDL_XQC_A1401.mol2, compounds
load ../../groups/orthosteric__positive/4LDO_ALE_A1402.mol2, compounds
load ../../groups/orthosteric__positive/6MXT_K5Y_A1401.mol2, compounds
load ../../groups/orthosteric__positive/7DHI_68H_R401.mol2, compounds
load ../../groups/orthosteric__positive/7XK9_GJ6_A1401.mol2, compounds
load ../../groups/orthosteric__positive/8GG0_G1I_R501.mol2, compounds
load ../../groups/orthosteric__positive/8JJ8_H98_F501.mol2, compounds
load ../../groups/orthosteric__positive/8JJL_DZQ_A501.mol2, compounds
load ../../groups/orthosteric__positive/9BUY_A1ASM_R504.mol2, compounds
load ../../groups/orthosteric__positive/9LW5_LDP_R401.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[-32.305, 10.727, 7.511], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[-26.456, 8.964, 6.147], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[-26.538, 11.707, 5.394], vdw=1.000
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_3, pos=[-32.971, 8.110, 7.359], vdw=1.000
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Acceptor_4, pos=[-32.237, 10.765, 7.451], vdw=1.000
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_5, pos=[-26.372, 11.519, 5.402], vdw=1.000
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Acceptor_6, pos=[-26.438, 8.901, 6.143], vdw=1.000
color ph4_Acceptor, Acceptor_6
group ph4_Acceptor, Acceptor_6
pseudoatom PosIonizable_7, pos=[-32.971, 8.110, 7.359], vdw=1.000
color ph4_PosIonizable, PosIonizable_7
group ph4_PosIonizable, PosIonizable_7
pseudoatom Aromatic_8, pos=[-28.730, 10.707, 6.457], vdw=1.000
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
pseudoatom Hydrophobe_9, pos=[-29.570, 10.026, 6.957], vdw=1.330
color ph4_Hydrophobe, Hydrophobe_9
group ph4_Hydrophobe, Hydrophobe_9
pseudoatom Hydrophobe_10, pos=[-34.848, 5.376, 7.807], vdw=1.494
color ph4_Hydrophobe, Hydrophobe_10
group ph4_Hydrophobe, Hydrophobe_10
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
