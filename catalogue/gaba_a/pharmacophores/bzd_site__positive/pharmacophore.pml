# gaba_a/bzd_site__positive — ensemble pharmacophore (7 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/bzd_site__positive/6HUO_08H_D501.mol2, compounds
load ../../groups/bzd_site__positive/6X3X_DZP_D404.mol2, compounds
load ../../groups/bzd_site__positive/8VQY_A1ADG_E401.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Acceptor_0, pos=[240.062, 218.267, 240.197], vdw=1.000
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom Aromatic_1, pos=[236.806, 214.104, 243.425], vdw=1.006
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_2, pos=[237.050, 214.807, 238.522], vdw=1.000
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_3, pos=[239.373, 216.656, 239.297], vdw=1.000
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Hydrophobe_4, pos=[236.888, 214.767, 242.685], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_4
group ph4_Hydrophobe, Hydrophobe_4
pseudoatom Hydrophobe_5, pos=[237.434, 215.177, 239.515], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_5
group ph4_Hydrophobe, Hydrophobe_5
pseudoatom Hydrophobe_6, pos=[236.053, 213.904, 238.109], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_6
group ph4_Hydrophobe, Hydrophobe_6
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
