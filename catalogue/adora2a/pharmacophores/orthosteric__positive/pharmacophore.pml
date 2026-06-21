# adora2a/orthosteric__positive — ensemble pharmacophore (9 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__positive/2YDV_NEC_A400.mol2, compounds
load ../../groups/orthosteric__positive/4UHR_NGI_A1320.mol2, compounds
load ../../groups/orthosteric__positive/5WF5_UKA_A1201.mol2, compounds
load ../../groups/orthosteric__positive/7ARO_RVZ_A1201.mol2, compounds
load ../../groups/orthosteric__positive/8RLN_A1H1S_A1211.mol2, compounds
load ../../groups/orthosteric__positive/8WDT_WCH_A1000.mol2, compounds
load ../../groups/orthosteric__positive/9EE8_ADN_A400.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[-1.377, 98.054, 52.078], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[2.477, 90.362, 53.874], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[1.679, 89.956, 49.936], vdw=1.000
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_3, pos=[4.060, 92.513, 53.928], vdw=1.000
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Acceptor_4, pos=[1.796, 93.998, 52.555], vdw=3.000
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_5, pos=[0.652, 105.641, 56.233], vdw=3.000
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom PosIonizable_6, pos=[0.635, 95.067, 51.805], vdw=1.000
color ph4_PosIonizable, PosIonizable_6
group ph4_PosIonizable, PosIonizable_6
pseudoatom Aromatic_7, pos=[0.942, 95.882, 52.372], vdw=1.404
color ph4_Aromatic, Aromatic_7
group ph4_Aromatic, Aromatic_7
pseudoatom Aromatic_8, pos=[1.178, 101.199, 56.411], vdw=2.227
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
