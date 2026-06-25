# adrb2/orthosteric__positive — ensemble pharmacophore (10 features)
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

pseudoatom Donor_0, pos=[-32.305, 10.727, 7.511], vdw=1.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[-26.456, 8.964, 6.147], vdw=1.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[-26.538, 11.707, 5.394], vdw=1.000
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_3, pos=[-32.971, 8.110, 7.359], vdw=1.000
color ph4_Donor, Donor_3
group ph4_Donor, Donor_3
pseudoatom Acceptor_4, pos=[-32.237, 10.765, 7.451], vdw=1.000
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_5, pos=[-26.372, 11.519, 5.402], vdw=1.000
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Acceptor_6, pos=[-26.438, 8.901, 6.143], vdw=1.000
color ph4_Acceptor, Acceptor_6
group ph4_Acceptor, Acceptor_6
pseudoatom PosIonizable_7, pos=[-32.971, 8.110, 7.359], vdw=1.000
color ph4_PosIonizable, PosIonizable_7
group ph4_PosIonizable, PosIonizable_7
pseudoatom Aromatic_8, pos=[-28.730, 10.707, 6.457], vdw=1.000
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
pseudoatom LumpedHydrophobe_9, pos=[-28.730, 10.707, 6.457], vdw=1.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_9
group ph4_LumpedHydrophobe, LumpedHydrophobe_9
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
