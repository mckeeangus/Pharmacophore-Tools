# adrb2/orthosteric__positive — ensemble pharmacophore (5 features)
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

pseudoatom Donor_1, pos=[-32.305, 10.727, 7.511], vdw=1.000, label="Donor 1 (1.00)"
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[-26.456, 8.964, 6.147], vdw=1.000, label="Donor 2 (1.00)"
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_3, pos=[-26.538, 11.707, 5.394], vdw=1.000, label="Donor 3 (1.00)"
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Aromatic_1, pos=[-28.730, 10.707, 6.457], vdw=1.000, label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Donor_4, pos=[-32.971, 8.110, 7.359], vdw=1.000, label="Donor 4 (0.91)"
color ph4_Donor, Donor_4
group ph4_Donor, Donor_4
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
