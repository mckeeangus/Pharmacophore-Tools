# chrm2/orthosteric__positive — ensemble pharmacophore (3 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/orthosteric__positive/4MQS_IXO_A501.mol2, compounds
load ../../groups/orthosteric__positive/7T94_ACH_A501.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Acceptor_0, pos=[136.798, 146.012, 104.766], vdw=1.255
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom PosIonizable_1, pos=[132.860, 144.782, 102.184], vdw=1.000
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom Hydrophobe_2, pos=[134.581, 146.004, 104.344], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_2
group ph4_Hydrophobe, Hydrophobe_2
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
