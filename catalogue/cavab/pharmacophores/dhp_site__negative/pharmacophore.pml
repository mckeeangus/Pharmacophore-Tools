# cavab/dhp_site__negative — ensemble pharmacophore (7 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/dhp_site__negative/5KLS_6UC_C1304.mol2, compounds
load ../../groups/dhp_site__negative/5KMF_6U9_A1301.mol2, compounds
load ../../groups/dhp_site__negative/6KE5_6UB_B1301.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[25.632, 162.997, 15.217], vdw=1.220
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[27.775, 164.940, 18.823], vdw=1.445
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[25.462, 167.265, 14.213], vdw=1.353
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom PosIonizable_3, pos=[27.775, 164.940, 18.823], vdw=1.445
color ph4_PosIonizable, PosIonizable_3
group ph4_PosIonizable, PosIonizable_3
pseudoatom Aromatic_4, pos=[25.395, 164.346, 10.410], vdw=1.000
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Hydrophobe_5, pos=[25.083, 164.172, 13.657], vdw=1.448
color ph4_Hydrophobe, Hydrophobe_5
group ph4_Hydrophobe, Hydrophobe_5
pseudoatom Hydrophobe_6, pos=[25.308, 164.418, 11.372], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_6
group ph4_Hydrophobe, Hydrophobe_6
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
