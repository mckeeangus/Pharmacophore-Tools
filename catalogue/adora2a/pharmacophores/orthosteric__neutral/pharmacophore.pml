# adora2a/orthosteric__neutral — ensemble pharmacophore (7 features)
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

pseudoatom Donor_0, pos=[-2.377, 99.329, 52.024], vdw=2.239
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[3.934, 94.721, 53.562], vdw=1.679
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[0.693, 97.874, 52.954], vdw=1.210
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[-0.913, 95.680, 51.441], vdw=1.000
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Aromatic_4, pos=[0.680, 94.802, 52.108], vdw=2.212
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Aromatic_5, pos=[3.191, 99.138, 56.062], vdw=2.968
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom LumpedHydrophobe_6, pos=[-0.020, 92.865, 51.182], vdw=1.138
color ph4_LumpedHydrophobe, LumpedHydrophobe_6
group ph4_LumpedHydrophobe, LumpedHydrophobe_6
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
