# net_slc6a2/central_s1__negative — ensemble pharmacophore (5 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/central_s1__negative/4M48_21B_A704.mol2, compounds
load ../../groups/central_s1__negative/4XNX_41X_A707.mol2, compounds
load ../../groups/central_s1__negative/4XP4_COC_A706.mol2, compounds
load ../../groups/central_s1__negative/4XPF_42F_A703.mol2, compounds
load ../../groups/central_s1__negative/4XPG_42L_A701.mol2, compounds
load ../../groups/central_s1__negative/6M38_29E_A601.mol2, compounds
load ../../groups/central_s1__negative/6M3Z_F0F_A701.mol2, compounds
load ../../groups/central_s1__negative/6M47_F1U_A608.mol2, compounds
load ../../groups/central_s1__negative/8HFI_DSM_A701.mol2, compounds
load ../../groups/central_s1__negative/8HFL_1XR_A701.mol2, compounds
load ../../groups/central_s1__negative/8I3V_68P_A701.mol2, compounds
load ../../groups/central_s1__negative/8WTX_Y60_A701.mol2, compounds
load ../../groups/central_s1__negative/8WTY_XEF_A701.mol2, compounds
load ../../groups/central_s1__negative/8XB2_YNT_A702.mol2, compounds
load ../../groups/central_s1__negative/8Y8Z_A1LX3_E701.mol2, compounds
load ../../groups/central_s1__negative/8Y90_A1LX6_A701.mol2, compounds
load ../../groups/central_s1__negative/8Y91_A1LX5_D703.mol2, compounds
load ../../groups/central_s1__negative/8Y93_TP0_A701.mol2, compounds
load ../../groups/central_s1__negative/8YR2_41U_B701.mol2, compounds
load ../../groups/central_s1__negative/8ZP1_A1D9Y_A702.mol2, compounds
load ../../groups/central_s1__negative/8ZP2_A1LX4_A701.mol2, compounds
load ../../groups/central_s1__negative/9JEL_A1EBN_A701.mol2, compounds
load ../../groups/central_s1__negative/9JF3_A1EBO_A701.mol2, compounds
load ../../groups/central_s1__negative/9KDH_A1D5S_B709.mol2, compounds
load ../../groups/central_s1__negative/9KE3_A1EFR_B707.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[129.756, 126.559, 133.210], vdw=2.480
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom PosIonizable_1, pos=[130.001, 126.199, 134.125], vdw=1.163
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom Aromatic_2, pos=[130.475, 130.882, 131.599], vdw=2.571
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Hydrophobe_3, pos=[130.348, 130.266, 132.145], vdw=2.592
color ph4_Hydrophobe, Hydrophobe_3
group ph4_Hydrophobe, Hydrophobe_3
pseudoatom Acceptor_4, pos=[130.140, 129.479, 132.503], vdw=2.500
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
