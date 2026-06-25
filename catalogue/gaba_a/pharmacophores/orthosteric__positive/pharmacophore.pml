# gaba_a/orthosteric__positive — ensemble pharmacophore (4 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load representative_ligand.sdf, ligand
hide everything, ligand
show sticks, ligand
color grey70, ligand and elem C

set_color ph4_Donor, [1.0, 0.4, 0.7]
set_color ph4_Acceptor, [0.0, 0.8, 0.0]
set_color ph4_LumpedHydrophobe, [0.0, 0.9, 0.9]
set_color ph4_Aromatic, [1.0, 0.85, 0.0]
set_color ph4_PosIonizable, [1.0, 0.0, 0.0]
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
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
