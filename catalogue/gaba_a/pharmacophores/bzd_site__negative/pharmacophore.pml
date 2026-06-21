# gaba_a/bzd_site__negative — ensemble pharmacophore (5 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/bzd_site__negative/8DD3_R63_D701.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Acceptor_0, pos=[235.550, 219.952, 244.707], vdw=1.646
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom Acceptor_1, pos=[238.250, 211.962, 242.228], vdw=1.266
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Aromatic_2, pos=[236.760, 214.514, 244.216], vdw=1.088
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Hydrophobe_3, pos=[236.629, 215.729, 244.039], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_3
group ph4_Hydrophobe, Hydrophobe_3
pseudoatom Hydrophobe_4, pos=[236.675, 217.894, 243.170], vdw=1.000
color ph4_Hydrophobe, Hydrophobe_4
group ph4_Hydrophobe, Hydrophobe_4
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
