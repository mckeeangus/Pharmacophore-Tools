# gr_nr3c1/lbp__positive — ensemble pharmacophore (7 features)
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

pseudoatom Acceptor_0, pos=[28.739, 6.908, 14.827], vdw=3.000
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom Acceptor_1, pos=[34.067, 8.315, 6.623], vdw=3.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Donor_2, pos=[28.632, 5.909, 13.661], vdw=3.000
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Aromatic_3, pos=[31.985, 7.683, 9.456], vdw=1.815
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Aromatic_4, pos=[28.044, 9.760, 14.412], vdw=2.330
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Aromatic_5, pos=[34.459, 9.264, 5.971], vdw=1.000
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom LumpedHydrophobe_6, pos=[32.412, 7.782, 10.738], vdw=1.414
color ph4_LumpedHydrophobe, LumpedHydrophobe_6
group ph4_LumpedHydrophobe, LumpedHydrophobe_6
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
