# nachr_a4b2/orthosteric__positive — ensemble pharmacophore (5 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__positive/1UV6_CCE_J1206.mol2, compounds
load ../../groups/orthosteric__positive/2WNL_AN4_G300.mol2, compounds
load ../../groups/orthosteric__positive/3U8J_09O_A211.mol2, compounds
load ../../groups/orthosteric__positive/3U8K_09P_F211.mol2, compounds
load ../../groups/orthosteric__positive/3U8L_09Q_J211.mol2, compounds
load ../../groups/orthosteric__positive/3U8M_09R_L211.mol2, compounds
load ../../groups/orthosteric__positive/3U8N_09S_Q211.mol2, compounds
load ../../groups/orthosteric__positive/3WTJ_TH4_B301.mol2, compounds
load ../../groups/orthosteric__positive/3WTN_N2Y_H301.mol2, compounds
load ../../groups/orthosteric__positive/3ZDG_XRX_I301.mol2, compounds
load ../../groups/orthosteric__positive/3ZDH_XRS_A301.mol2, compounds
load ../../groups/orthosteric__positive/4FRR_0VC_F301.mol2, compounds
load ../../groups/orthosteric__positive/4ZJS_4P0_D301.mol2, compounds
load ../../groups/orthosteric__positive/5AIN_QMR_A1207.mol2, compounds
load ../../groups/orthosteric__positive/5BP0_FN1_D302.mol2, compounds
load ../../groups/orthosteric__positive/5O87_NCT_A601.mol2, compounds
load ../../groups/orthosteric__positive/5SYO_C5E_E301.mol2, compounds
load ../../groups/orthosteric__positive/6SGV_LDQ_G601.mol2, compounds
load ../../groups/orthosteric__positive/8ST4_ACH_A704.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[166.878, 123.394, 186.228], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[171.480, 124.134, 188.452], vdw=1.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom PosIonizable_2, pos=[166.886, 123.379, 186.181], vdw=1.000
color ph4_PosIonizable, PosIonizable_2
group ph4_PosIonizable, PosIonizable_2
pseudoatom Aromatic_3, pos=[170.850, 122.801, 188.266], vdw=1.000
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Hydrophobe_4, pos=[168.962, 122.971, 185.660], vdw=1.535
color ph4_Hydrophobe, Hydrophobe_4
group ph4_Hydrophobe, Hydrophobe_4
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
