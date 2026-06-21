# nachr_a4b2/accessory__positive — ensemble pharmacophore (3 features)
# run from this file's directory:  pymol pharmacophore.pml
reinitialize
bg_color white
set valence, 1

load ../../groups/accessory__positive/4NZB_NSE_B301.mol2, compounds
hide everything, compounds
show lines, compounds
color grey70, compounds and elem C

set_color ph4_Donor, [0.0, 0.85, 0.0]
set_color ph4_Acceptor, [0.9, 0.0, 0.0]
set_color ph4_Hydrophobe, [1.0, 0.85, 0.0]
set_color ph4_Aromatic, [0.6, 0.3, 0.9]
set_color ph4_PosIonizable, [0.15, 0.45, 1.0]
set_color ph4_NegIonizable, [1.0, 0.45, 0.0]

pseudoatom Acceptor_0, pos=[167.983, 124.243, 185.138], vdw=1.139
color ph4_Acceptor, Acceptor_0
group ph4_Acceptor, Acceptor_0
pseudoatom Aromatic_1, pos=[166.562, 123.972, 184.482], vdw=1.956
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Hydrophobe_2, pos=[170.430, 122.564, 187.746], vdw=1.211
color ph4_Hydrophobe, Hydrophobe_2
group ph4_Hydrophobe, Hydrophobe_2
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
