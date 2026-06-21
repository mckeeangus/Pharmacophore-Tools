# cox2/cox_channel__negative — ensemble pharmacophore (8 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/cox_channel__negative/5F1A_SAL_A601.mol2, compounds
load ../../groups/cox_channel__negative/5IKR_ID8_A601.mol2, compounds
load ../../groups/cox_channel__negative/5IKT_TLF_B601.mol2, compounds
load ../../groups/cox_channel__negative/5IKV_FLF_B601.mol2, compounds
load ../../groups/cox_channel__negative/5KIR_RCX_A601.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[27.911, 4.591, 32.772], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[24.754, 3.590, 32.885], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[26.684, 4.278, 32.470], vdw=2.442
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom NegIonizable_3, pos=[28.031, 4.738, 32.943], vdw=1.000
color ph4_NegIonizable, NegIonizable_3
group ph4_NegIonizable, NegIonizable_3
pseudoatom Aromatic_4, pos=[25.683, 4.575, 35.186], vdw=1.000
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Aromatic_5, pos=[22.877, 2.248, 31.852], vdw=1.000
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom Hydrophobe_6, pos=[25.618, 4.665, 35.292], vdw=1.404
color ph4_Hydrophobe, Hydrophobe_6
group ph4_Hydrophobe, Hydrophobe_6
pseudoatom Hydrophobe_7, pos=[22.777, 2.108, 31.825], vdw=1.988
color ph4_Hydrophobe, Hydrophobe_7
group ph4_Hydrophobe, Hydrophobe_7
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
