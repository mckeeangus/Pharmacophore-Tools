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
set_color ph4_ExcludedVolume, [0.55, 0.55, 0.55]

pseudoatom Acceptor_1, pos=[1.588, 97.505, 53.309], vdw=1.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[1.588, 97.505, 53.309], label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Aromatic_1, pos=[0.942, 95.882, 52.372], vdw=1.000
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[0.942, 95.882, 52.372], label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Donor_1, pos=[-1.377, 98.054, 52.078], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[-1.377, 98.054, 52.078], label="Donor 1 (1.00)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Donor_2, pos=[4.060, 92.513, 53.928], vdw=1.000
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_2_ctr, pos=[4.060, 92.513, 53.928], label="Donor 2 (0.83)"
color ph4_Donor, Donor_2_ctr
group ph4_centers, Donor_2_ctr
pseudoatom Donor_3, pos=[2.477, 90.362, 53.874], vdw=1.000
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Donor_3_ctr, pos=[2.477, 90.362, 53.874], label="Donor 3 (0.83)"
color ph4_Donor, Donor_3_ctr
group ph4_centers, Donor_3_ctr
pseudoatom Acceptor_2, pos=[2.848, 92.568, 51.143], vdw=1.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[2.848, 92.568, 51.143], label="Acceptor 2 (0.83)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom Acceptor_3, pos=[-0.420, 95.066, 51.279], vdw=1.000
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_3_ctr, pos=[-0.420, 95.066, 51.279], label="Acceptor 3 (0.83)"
color ph4_Acceptor, Acceptor_3_ctr
group ph4_centers, Acceptor_3_ctr
pseudoatom Acceptor_4, pos=[0.510, 91.062, 50.743], vdw=1.000
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_4_ctr, pos=[0.510, 91.062, 50.743], label="Acceptor 4 (0.83)"
color ph4_Acceptor, Acceptor_4_ctr
group ph4_centers, Acceptor_4_ctr
pseudoatom Donor_4, pos=[1.669, 90.045, 49.924], vdw=1.000
color ph4_Donor, Donor_4
group ph4_Donor, Donor_4
pseudoatom Donor_4_ctr, pos=[1.669, 90.045, 49.924], label="Donor 4 (0.67)"
color ph4_Donor, Donor_4_ctr
group ph4_centers, Donor_4_ctr
pseudoatom Aromatic_2, pos=[1.178, 101.199, 56.411], vdw=1.000
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[1.178, 101.199, 56.411], label="Aromatic 2 (0.67)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
hide spheres, ph4_centers
show nb_spheres, ph4_centers
orient
