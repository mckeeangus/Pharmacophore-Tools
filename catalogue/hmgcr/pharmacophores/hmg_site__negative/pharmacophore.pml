# hmgcr/hmg_site__negative — ensemble pharmacophore (21 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/hmg_site__negative/1HW8_114_A2.mol2, compounds
load ../../groups/hmg_site__negative/1HW9_SIM_C2.mol2, compounds
load ../../groups/hmg_site__negative/1HWI_115_A2.mol2, compounds
load ../../groups/hmg_site__negative/1HWJ_116_A2.mol2, compounds
load ../../groups/hmg_site__negative/1HWK_117_A2.mol2, compounds
load ../../groups/hmg_site__negative/1HWL_FBI_A2.mol2, compounds
load ../../groups/hmg_site__negative/2Q1L_882_A877.mol2, compounds
load ../../groups/hmg_site__negative/2Q6B_HR2_A3001.mol2, compounds
load ../../groups/hmg_site__negative/2Q6C_HR1_A3002.mol2, compounds
load ../../groups/hmg_site__negative/2R4F_RIE_B876.mol2, compounds
load ../../groups/hmg_site__negative/3BGL_RID_A2.mol2, compounds
load ../../groups/hmg_site__negative/3CCT_3HI_D3.mol2, compounds
load ../../groups/hmg_site__negative/3CCW_4HI_C4.mol2, compounds
load ../../groups/hmg_site__negative/3CCZ_5HI_B876.mol2, compounds
load ../../groups/hmg_site__negative/3CD0_6HI_D3.mol2, compounds
load ../../groups/hmg_site__negative/3CD5_7HI_B1.mol2, compounds
load ../../groups/hmg_site__negative/3CDA_8HI_B1.mol2, compounds
load ../../groups/hmg_site__negative/3CDB_9HI_D3.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[13.527, 4.701, 14.441], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[14.839, 6.577, 11.023], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[21.606, 11.423, 14.702], vdw=1.265
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_3, pos=[14.018, 1.801, 16.113], vdw=1.000
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Donor_4, pos=[16.184, 2.602, 16.215], vdw=1.000
color ph4_Donor, Donor_4
group ph4_Donor, Donor_4
pseudoatom Acceptor_5, pos=[15.101, 2.221, 16.156], vdw=1.123
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Acceptor_6, pos=[13.527, 4.701, 14.441], vdw=1.000
color ph4_Acceptor, Acceptor_6
group ph4_Acceptor, Acceptor_6
pseudoatom Acceptor_7, pos=[14.839, 6.577, 11.023], vdw=1.000
color ph4_Acceptor, Acceptor_7
group ph4_Acceptor, Acceptor_7
pseudoatom Acceptor_8, pos=[21.574, 9.516, 13.916], vdw=1.363
color ph4_Acceptor, Acceptor_8
group ph4_Acceptor, Acceptor_8
pseudoatom Acceptor_9, pos=[13.795, 7.670, 19.145], vdw=1.000
color ph4_Acceptor, Acceptor_9
group ph4_Acceptor, Acceptor_9
pseudoatom Acceptor_10, pos=[18.280, 9.988, 16.762], vdw=2.584
color ph4_Acceptor, Acceptor_10
group ph4_Acceptor, Acceptor_10
pseudoatom NegIonizable_11, pos=[15.156, 2.301, 15.975], vdw=1.000
color ph4_NegIonizable, NegIonizable_11
group ph4_NegIonizable, NegIonizable_11
pseudoatom Hydrophobe_12, pos=[16.353, 7.454, 13.079], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_12
group ph4_Hydrophobe, Hydrophobe_12
pseudoatom Hydrophobe_13, pos=[15.004, 4.777, 12.566], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_13
group ph4_Hydrophobe, Hydrophobe_13
pseudoatom Hydrophobe_14, pos=[14.979, 2.824, 14.126], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_14
group ph4_Hydrophobe, Hydrophobe_14
pseudoatom Hydrophobe_15, pos=[16.898, 8.696, 16.304], vdw=1.014
color ph4_Hydrophobe, Hydrophobe_15
group ph4_Hydrophobe, Hydrophobe_15
pseudoatom Hydrophobe_16, pos=[18.992, 9.220, 12.558], vdw=1.204
color ph4_Hydrophobe, Hydrophobe_16
group ph4_Hydrophobe, Hydrophobe_16
pseudoatom Hydrophobe_17, pos=[19.143, 9.599, 15.822], vdw=1.067
color ph4_Hydrophobe, Hydrophobe_17
group ph4_Hydrophobe, Hydrophobe_17
pseudoatom Aromatic_18, pos=[18.612, 9.310, 14.566], vdw=1.000
color ph4_Aromatic, Aromatic_18
group ph4_Aromatic, Aromatic_18
pseudoatom Aromatic_19, pos=[15.650, 8.319, 17.263], vdw=1.000
color ph4_Aromatic, Aromatic_19
group ph4_Aromatic, Aromatic_19
pseudoatom Aromatic_20, pos=[24.373, 12.416, 13.584], vdw=1.348
color ph4_Aromatic, Aromatic_20
group ph4_Aromatic, Aromatic_20
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
