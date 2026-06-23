# drd1/orthosteric__positive — ensemble pharmacophore (9 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__positive/7CKX_G3O_R501.mol2, compounds
load ../../groups/orthosteric__positive/7CKY_G3U_R502.mol2, compounds
load ../../groups/orthosteric__positive/7CRH_GBU_R501.mol2, compounds
load ../../groups/orthosteric__positive/7JOZ_VFP_R1201.mol2, compounds
load ../../groups/orthosteric__positive/7JVP_SK9_R501.mol2, compounds
load ../../groups/orthosteric__positive/7JVQ_OR9_R501.mol2, compounds
load ../../groups/orthosteric__positive/7LJC_SK0_R501.mol2, compounds
load ../../groups/orthosteric__positive/7X2C_G3C_F503.mol2, compounds
load ../../groups/orthosteric__positive/7X2D_86W_F502.mol2, compounds
load ../../groups/orthosteric__positive/8IRR_R5F_R501.mol2, compounds
load ../../groups/orthosteric__positive/8JXR_7LD_A401.mol2, compounds
load ../../groups/orthosteric__positive/8JXS_V6X_A401.mol2, compounds
load ../../groups/orthosteric__positive/9I52_A1IZU_R501.mol2, compounds
load ../../groups/orthosteric__positive/9I54_A1IZV_R501.mol2, compounds
load ../../groups/orthosteric__positive/9LLJ_LDP_R701.mol2, compounds
load ../../groups/orthosteric__positive/9LWC_ALE_R501.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[122.206, 119.069, 144.027], vdw=1.731
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[127.754, 121.952, 142.268], vdw=1.218
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[123.585, 119.972, 143.917], vdw=2.497
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[130.032, 124.463, 148.307], vdw=2.934
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom PosIonizable_4, pos=[127.550, 121.809, 142.231], vdw=1.563
color ph4_PosIonizable, PosIonizable_4
group ph4_PosIonizable, PosIonizable_4
pseudoatom Aromatic_5, pos=[123.914, 120.217, 142.830], vdw=1.013
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom Aromatic_6, pos=[126.913, 122.339, 146.326], vdw=1.000
color ph4_Aromatic, Aromatic_6
group ph4_Aromatic, Aromatic_6
pseudoatom Hydrophobe_7, pos=[124.996, 120.758, 143.130], vdw=1.936
color ph4_Hydrophobe, Hydrophobe_7
group ph4_Hydrophobe, Hydrophobe_7
pseudoatom Hydrophobe_8, pos=[128.446, 122.751, 146.484], vdw=1.910
color ph4_Hydrophobe, Hydrophobe_8
group ph4_Hydrophobe, Hydrophobe_8
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
