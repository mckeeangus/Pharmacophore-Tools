# gaba_a/bzd_site__neutral — ensemble pharmacophore (3 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/bzd_site__neutral/7QNE_EIE_D502.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Acceptor_0, pos=[235.299, 219.143, 244.166], vdw=1.718
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom PosIonizable_1, pos=[236.402, 213.359, 243.742], vdw=3.000
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom Aromatic_2, pos=[236.065, 215.085, 243.676], vdw=1.991
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
