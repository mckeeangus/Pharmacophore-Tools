# gaba_a/orthosteric__positive — ensemble pharmacophore (5 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__positive/7A5V_HSM_A5408.mol2, compounds
load ../../groups/orthosteric__positive/7QNC_EI7_B503.mol2, compounds
load ../../groups/orthosteric__positive/9EQG_ABU_E3205.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Donor_0, pos=[187.423, 221.793, 241.900], vdw=2.772
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[185.516, 220.400, 241.529], vdw=2.138
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom PosIonizable_2, pos=[188.186, 223.029, 242.056], vdw=2.446
color ph4_PosIonizable, PosIonizable_2
group ph4_PosIonizable, PosIonizable_2
pseudoatom Aromatic_3, pos=[186.728, 220.685, 241.310], vdw=1.015
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Hydrophobe_4, pos=[187.556, 221.762, 241.560], vdw=2.248
color ph4_Hydrophobe, Hydrophobe_4
group ph4_Hydrophobe, Hydrophobe_4
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
