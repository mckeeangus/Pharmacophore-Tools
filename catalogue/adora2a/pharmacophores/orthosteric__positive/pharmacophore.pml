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

pseudoatom Aromatic_1, pos=[0.942, 95.882, 52.372], vdw=1.225, label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Acceptor_1, pos=[1.357, 97.457, 53.211], vdw=1.395, label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[3.269, 91.438, 53.901], vdw=1.453, label="Acceptor 2 (0.83)"
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Donor_1, pos=[-1.377, 98.054, 52.078], vdw=1.000, label="Donor 1 (1.00)"
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_3, pos=[2.622, 92.414, 50.925], vdw=1.000, label="Acceptor 3 (0.83)"
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Donor_2, pos=[1.679, 89.956, 49.936], vdw=1.000, label="Donor 2 (0.83)"
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Acceptor_4, pos=[-0.420, 95.066, 51.279], vdw=1.000, label="Acceptor 4 (0.83)"
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_5, pos=[0.266, 90.917, 50.969], vdw=1.000, label="Acceptor 5 (0.67)"
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Aromatic_2, pos=[1.178, 101.199, 56.411], vdw=2.055, label="Aromatic 2 (0.67)"
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
