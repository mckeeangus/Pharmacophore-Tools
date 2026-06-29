# hmgcr/hmg_site__negative — ensemble pharmacophore (56 features)
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

pseudoatom Donor_0, pos=[14.293, 3.388, 15.375], vdw=3.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[14.780, 6.718, 10.703], vdw=2.565
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_2, pos=[21.334, 10.936, 14.783], vdw=2.774
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Acceptor_3, pos=[14.923, 2.605, 15.640], vdw=2.913
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Acceptor_4, pos=[14.530, 6.586, 11.210], vdw=2.793
color ph4_Acceptor, Acceptor_4
group ph4_Acceptor, Acceptor_4
pseudoatom Acceptor_5, pos=[20.915, 9.784, 14.585], vdw=3.000
color ph4_Acceptor, Acceptor_5
group ph4_Acceptor, Acceptor_5
pseudoatom Acceptor_6, pos=[14.048, 7.867, 18.471], vdw=3.000
color ph4_Acceptor, Acceptor_6
group ph4_Acceptor, Acceptor_6
pseudoatom NegIonizable_7, pos=[14.774, 2.030, 15.802], vdw=2.582
color ph4_NegIonizable, NegIonizable_7
group ph4_NegIonizable, NegIonizable_7
pseudoatom Aromatic_8, pos=[18.702, 9.308, 15.253], vdw=2.983
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
pseudoatom Aromatic_9, pos=[15.470, 8.142, 17.434], vdw=2.683
color ph4_Aromatic, Aromatic_9
group ph4_Aromatic, Aromatic_9
pseudoatom Aromatic_10, pos=[24.417, 12.308, 13.694], vdw=3.000
color ph4_Aromatic, Aromatic_10
group ph4_Aromatic, Aromatic_10
pseudoatom LumpedHydrophobe_11, pos=[19.116, 8.887, 11.298], vdw=2.650
color ph4_LumpedHydrophobe, LumpedHydrophobe_11
group ph4_LumpedHydrophobe, LumpedHydrophobe_11
pseudoatom LumpedHydrophobe_12, pos=[15.251, 8.033, 17.092], vdw=2.526
color ph4_LumpedHydrophobe, LumpedHydrophobe_12
group ph4_LumpedHydrophobe, LumpedHydrophobe_12
pseudoatom LumpedHydrophobe_13, pos=[24.609, 12.357, 13.762], vdw=3.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_13
group ph4_LumpedHydrophobe, LumpedHydrophobe_13
pseudoatom LumpedHydrophobe_14, pos=[19.359, 10.084, 17.749], vdw=2.819
color ph4_LumpedHydrophobe, LumpedHydrophobe_14
group ph4_LumpedHydrophobe, LumpedHydrophobe_14
pseudoatom PosIonizable_15, pos=[18.604, 9.148, 14.312], vdw=2.582
color ph4_PosIonizable, PosIonizable_15
group ph4_PosIonizable, PosIonizable_15
pseudoatom ExcludedVolume_16, pos=[23.807, 8.402, 12.090], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_17, pos=[11.246, 6.229, 18.505], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_18, pos=[16.523, 0.737, 18.123], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_19, pos=[13.871, 2.089, 18.793], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_20, pos=[11.550, 4.086, 12.515], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_21, pos=[15.815, 7.237, 21.702], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_22, pos=[11.055, 9.328, 18.727], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_23, pos=[24.795, 13.951, 8.714], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_24, pos=[20.313, 13.686, 10.742], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_25, pos=[16.636, 5.176, 9.115], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_26, pos=[12.660, 5.203, 8.924], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_27, pos=[23.553, 9.338, 11.050], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_28, pos=[15.193, 8.703, 8.916], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_29, pos=[20.934, 11.416, 23.758], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_30, pos=[20.227, 15.402, 11.351], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_31, pos=[16.695, 0.267, 13.155], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_32, pos=[23.119, 8.504, 17.944], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_33, pos=[12.007, 6.800, 16.422], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_34, pos=[17.733, 12.999, 9.447], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_35, pos=[11.841, 5.232, 17.162], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_36, pos=[14.492, -0.946, 14.433], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_37, pos=[29.205, 10.015, 11.754], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_38, pos=[11.173, 10.504, 19.519], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_39, pos=[10.961, 5.319, 19.620], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_40, pos=[22.439, 8.280, 21.121], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_41, pos=[17.889, 0.155, 17.961], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
pseudoatom ExcludedVolume_42, pos=[29.325, 10.423, 14.274], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_42
group ph4_ExcludedVolume, ExcludedVolume_42
pseudoatom ExcludedVolume_43, pos=[13.655, 7.771, 22.842], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_43
group ph4_ExcludedVolume, ExcludedVolume_43
pseudoatom ExcludedVolume_44, pos=[19.846, 6.026, 15.372], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_44
group ph4_ExcludedVolume, ExcludedVolume_44
pseudoatom ExcludedVolume_45, pos=[25.111, 11.251, 9.213], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_45
group ph4_ExcludedVolume, ExcludedVolume_45
pseudoatom ExcludedVolume_46, pos=[21.041, 11.554, 8.706], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_46
group ph4_ExcludedVolume, ExcludedVolume_46
pseudoatom ExcludedVolume_47, pos=[10.563, 2.868, 13.303], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_47
group ph4_ExcludedVolume, ExcludedVolume_47
pseudoatom ExcludedVolume_48, pos=[26.643, 8.970, 16.305], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_48
group ph4_ExcludedVolume, ExcludedVolume_48
pseudoatom ExcludedVolume_49, pos=[15.071, 7.182, 23.004], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_49
group ph4_ExcludedVolume, ExcludedVolume_49
pseudoatom ExcludedVolume_50, pos=[14.331, 3.240, 19.515], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_50
group ph4_ExcludedVolume, ExcludedVolume_50
pseudoatom ExcludedVolume_51, pos=[24.853, 9.836, 10.437], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_51
group ph4_ExcludedVolume, ExcludedVolume_51
pseudoatom ExcludedVolume_52, pos=[15.156, -1.524, 17.120], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_52
group ph4_ExcludedVolume, ExcludedVolume_52
pseudoatom ExcludedVolume_53, pos=[22.518, 6.898, 20.151], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_53
group ph4_ExcludedVolume, ExcludedVolume_53
pseudoatom ExcludedVolume_54, pos=[28.172, 9.663, 14.725], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_54
group ph4_ExcludedVolume, ExcludedVolume_54
pseudoatom ExcludedVolume_55, pos=[20.601, 4.407, 10.288], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_55
group ph4_ExcludedVolume, ExcludedVolume_55
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
