# net_slc6a2/central_s1__positive — ensemble pharmacophore (3 features)
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

pseudoatom Donor_1, pos=[130.541, 127.339, 133.247], vdw=2.755, label="Donor 1 (0.83)"
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[131.331, 132.479, 128.683], vdw=2.075, label="Donor 2 (0.50)"
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Aromatic_1, pos=[130.602, 130.920, 130.112], vdw=1.000, label="Aromatic 1 (0.67)"
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
