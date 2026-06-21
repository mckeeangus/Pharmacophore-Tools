# adora2a/orthosteric__negative — ensemble pharmacophore (7 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__negative/10KT_A1C5S_A1202.mol2, compounds
load ../../groups/orthosteric__negative/3REY_XAC_A999.mol2, compounds
load ../../groups/orthosteric__negative/3UZA_T4G_A330.mol2, compounds
load ../../groups/orthosteric__negative/5IU7_6DY_A2401.mol2, compounds
load ../../groups/orthosteric__negative/5IU8_6DZ_A2401.mol2, compounds
load ../../groups/orthosteric__negative/5IUA_6DX_A2401.mol2, compounds
load ../../groups/orthosteric__negative/5IUB_6DV_A2401.mol2, compounds
load ../../groups/orthosteric__negative/5MZP_CFF_A2401.mol2, compounds
load ../../groups/orthosteric__negative/5N2R_8JN_A2401.mol2, compounds
load ../../groups/orthosteric__negative/5NM4_ZMA_A507.mol2, compounds
load ../../groups/orthosteric__negative/5OLZ_T4E_A1201.mol2, compounds
load ../../groups/orthosteric__negative/5UIG_8D1_A503.mol2, compounds
load ../../groups/orthosteric__negative/6ZDR_QGE_A1201.mol2, compounds
load ../../groups/orthosteric__negative/6ZDV_QGW_A1201.mol2, compounds
load ../../groups/orthosteric__negative/7IO5_TEP_A1202.mol2, compounds
load ../../groups/orthosteric__negative/7PX4_8E2_A2404.mol2, compounds
load ../../groups/orthosteric__negative/7PYR_8IM_A2404.mol2, compounds
load ../../groups/orthosteric__negative/8CU7_LJX_A1202.mol2, compounds
load ../../groups/orthosteric__negative/8DU3_TKO_A3001.mol2, compounds
load ../../groups/orthosteric__negative/8GNE_JQR_A1201.mol2, compounds
load ../../groups/orthosteric__negative/8JWY_VBF_A1201.mol2, compounds
load ../../groups/orthosteric__negative/8RW4_A1H3L_A1201.mol2, compounds
load ../../groups/orthosteric__negative/8RW7_A1H3J_A1201.mol2, compounds
load ../../groups/orthosteric__negative/8RWC_A1H3I_A1201.mol2, compounds
load ../../groups/orthosteric__negative/8RWD_A1H3H_A1201.mol2, compounds
load ../../groups/orthosteric__negative/8RWE_A1H3K_A1201.mol2, compounds
load ../../groups/orthosteric__negative/9H2X_A1IR1_A1226.mol2, compounds
load ../../groups/orthosteric__negative/9H37_A1IR0_A1226.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[-1.394, 97.991, 52.038], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[1.073, 95.882, 52.583], vdw=2.864
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[1.715, 103.447, 56.638], vdw=3.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Aromatic_3, pos=[0.772, 95.440, 52.350], vdw=2.467
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Aromatic_4, pos=[0.346, 102.766, 55.970], vdw=3.000
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Hydrophobe_5, pos=[1.082, 100.509, 54.914], vdw=3.000
color ph4_Hydrophobe, Hydrophobe_5
group ph4_Hydrophobe, Hydrophobe_5
pseudoatom Hydrophobe_6, pos=[1.270, 94.206, 52.190], vdw=2.543
color ph4_Hydrophobe, Hydrophobe_6
group ph4_Hydrophobe, Hydrophobe_6
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
