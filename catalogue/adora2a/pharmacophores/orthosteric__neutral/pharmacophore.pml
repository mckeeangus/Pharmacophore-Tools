# adora2a/orthosteric__neutral — ensemble pharmacophore (5 features)
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

pseudoatom Aromatic_1, pos=[0.680, 94.802, 52.108], vdw=2.000
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[0.680, 94.802, 52.108], label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Acceptor_1, pos=[3.934, 94.721, 53.562], vdw=2.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[3.934, 94.721, 53.562], label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Acceptor_2, pos=[0.693, 97.874, 52.954], vdw=2.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[0.693, 97.874, 52.954], label="Acceptor 2 (1.00)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom Donor_1, pos=[-2.367, 99.088, 51.984], vdw=2.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[-2.367, 99.088, 51.984], label="Donor 1 (0.80)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Aromatic_2, pos=[3.191, 99.138, 56.062], vdw=2.000
color ph4_Aromatic, Aromatic_2
group ph4_Aromatic, Aromatic_2
pseudoatom Aromatic_2_ctr, pos=[3.191, 99.138, 56.062], label="Aromatic 2 (0.60)"
color ph4_Aromatic, Aromatic_2_ctr
group ph4_centers, Aromatic_2_ctr
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
hide spheres, ph4_centers
show nb_spheres, ph4_centers
orient
