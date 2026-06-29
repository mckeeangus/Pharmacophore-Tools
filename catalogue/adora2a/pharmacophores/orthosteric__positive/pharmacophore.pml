# adora2a/orthosteric__positive — ensemble pharmacophore (9 features)
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

pseudoatom Aromatic_0, pos=[0.942, 95.882, 52.372], vdw=1.404
color ph4_Aromatic, Aromatic_0
group ph4_Aromatic, Aromatic_0
pseudoatom Acceptor_1, pos=[1.357, 97.457, 53.211], vdw=1.260
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[3.269, 91.438, 53.901], vdw=1.386
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[2.622, 92.414, 50.925], vdw=1.000
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Donor_4, pos=[1.679, 89.956, 49.936], vdw=1.000
color ph4_Donor, Donor_4
group ph4_Donor, Donor_4
pseudoatom Acceptor_5, pos=[-0.420, 95.066, 51.279], vdw=1.000
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Donor_6, pos=[-1.523, 97.877, 51.894], vdw=1.000
color ph4_Donor, Donor_6
group ph4_Donor, Donor_6
pseudoatom Acceptor_7, pos=[0.266, 90.917, 50.969], vdw=1.000
color ph4_Acceptor, Acceptor_7
group ph4_Acceptor, Acceptor_7
pseudoatom Aromatic_8, pos=[1.178, 101.199, 56.411], vdw=2.227
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
