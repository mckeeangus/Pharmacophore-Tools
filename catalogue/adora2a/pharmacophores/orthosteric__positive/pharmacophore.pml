# adora2a/orthosteric__positive — ensemble pharmacophore (10 features)
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

pseudoatom Donor_0, pos=[-1.377, 98.054, 52.078], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[2.477, 90.362, 53.874], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[1.679, 89.956, 49.936], vdw=1.000
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_3, pos=[4.060, 92.513, 53.928], vdw=1.000
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Acceptor_4, pos=[1.796, 93.998, 52.555], vdw=3.000
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_5, pos=[0.652, 105.641, 56.233], vdw=3.000
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom PosIonizable_6, pos=[0.635, 95.067, 51.805], vdw=1.000
color ph4_PosIonizable, PosIonizable_6
group ph4_PosIonizable, PosIonizable_6
pseudoatom Aromatic_7, pos=[0.942, 95.882, 52.372], vdw=1.404
color ph4_Aromatic, Aromatic_7
group ph4_Aromatic, Aromatic_7
pseudoatom Aromatic_8, pos=[1.178, 101.199, 56.411], vdw=2.227
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
pseudoatom LumpedHydrophobe_9, pos=[-0.202, 101.766, 55.317], vdw=3.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_9
group ph4_LumpedHydrophobe, LumpedHydrophobe_9
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
