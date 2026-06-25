# cdk2/atp_site__negative — ensemble pharmacophore (6 features)
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

pseudoatom Donor_0, pos=[7.309, -24.620, -24.826], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Acceptor_1, pos=[7.310, -22.059, -22.608], vdw=3.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[3.138, -27.178, -26.345], vdw=2.833
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Aromatic_3, pos=[8.110, -22.239, -22.982], vdw=1.389
color ph4_Aromatic, Aromatic_3
group ph4_Aromatic, Aromatic_3
pseudoatom Aromatic_4, pos=[4.767, -25.854, -26.218], vdw=1.610
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom LumpedHydrophobe_5, pos=[6.160, -20.849, -21.553], vdw=2.622
color ph4_LumpedHydrophobe, LumpedHydrophobe_5
group ph4_LumpedHydrophobe, LumpedHydrophobe_5
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
