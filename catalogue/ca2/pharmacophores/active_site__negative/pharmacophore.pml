# ca2/active_site__negative — ensemble pharmacophore (4 features)
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
set_color ph4_ExcludedVolume, [0.55, 0.55, 0.55]

pseudoatom Acceptor_1, pos=[-5.272, 1.153, 17.993], vdw=1.000, label="Acceptor 1 (0.96)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Donor_1, pos=[-5.224, 0.049, 15.960], vdw=1.000, label="Donor 1 (0.80)"
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[-7.225, 1.098, 16.563], vdw=1.000, label="Acceptor 2 (0.95)"
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Aromatic_1, pos=[-4.761, 3.525, 15.031], vdw=1.000, label="Aromatic 1 (0.78)"
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
