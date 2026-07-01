# gaba_a/orthosteric__positive — ensemble pharmacophore (2 features)
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

pseudoatom Donor_1, pos=[187.423, 221.793, 241.900], vdw=2.772, label="Donor 1 (0.67)"
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_1, pos=[204.700, 203.827, 242.516], vdw=3.000, label="Acceptor 1 (0.67)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
