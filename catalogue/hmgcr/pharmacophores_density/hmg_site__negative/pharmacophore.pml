# hmgcr/hmg_site__negative — ensemble pharmacophore (46 features)
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

pseudoatom Acceptor_1, pos=[20.912, 9.730, 14.540], vdw=2.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[20.912, 9.730, 14.540], label="Acceptor 1 (0.94)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Donor_1, pos=[13.370, 4.427, 14.837], vdw=2.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[13.370, 4.427, 14.837], label="Donor 1 (1.00)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Donor_2, pos=[14.762, 6.492, 10.697], vdw=2.000
color ph4_Donor, Donor_2
group ph4_Donor, Donor_2
pseudoatom Donor_2_ctr, pos=[14.762, 6.492, 10.697], label="Donor 2 (1.00)"
color ph4_Donor, Donor_2_ctr
group ph4_centers, Donor_2_ctr
pseudoatom Acceptor_2, pos=[14.263, 8.052, 18.810], vdw=2.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[14.263, 8.052, 18.810], label="Acceptor 2 (0.94)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom LumpedHydrophobe_1, pos=[19.136, 8.935, 11.420], vdw=2.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_1_ctr, pos=[19.136, 8.935, 11.420], label="LumpedHydrophobe 1 (0.83)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1_ctr
group ph4_centers, LumpedHydrophobe_1_ctr
pseudoatom Aromatic_1, pos=[24.417, 12.308, 13.694], vdw=2.000
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[24.417, 12.308, 13.694], label="Aromatic 1 (0.61)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom ExcludedVolume_6, pos=[23.807, 8.402, 12.090], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_7, pos=[11.246, 6.229, 18.505], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_8, pos=[16.523, 0.737, 18.123], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_9, pos=[13.871, 2.089, 18.793], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_10, pos=[11.550, 4.086, 12.515], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_11, pos=[15.815, 7.237, 21.702], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_12, pos=[11.055, 9.328, 18.727], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_13, pos=[24.795, 13.951, 8.714], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_14, pos=[20.313, 13.686, 10.742], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_15, pos=[16.636, 5.176, 9.115], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_16, pos=[12.660, 5.203, 8.924], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_17, pos=[23.553, 9.338, 11.050], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_18, pos=[15.193, 8.703, 8.916], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_19, pos=[20.934, 11.416, 23.758], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_20, pos=[20.227, 15.402, 11.351], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_21, pos=[16.695, 0.267, 13.155], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_22, pos=[23.119, 8.504, 17.944], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_23, pos=[12.007, 6.800, 16.422], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_24, pos=[17.733, 12.999, 9.447], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_25, pos=[11.841, 5.232, 17.162], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_26, pos=[14.492, -0.946, 14.433], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_27, pos=[29.205, 10.015, 11.754], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_28, pos=[11.173, 10.504, 19.519], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_29, pos=[10.961, 5.319, 19.620], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_30, pos=[22.439, 8.280, 21.121], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_31, pos=[17.889, 0.155, 17.961], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_32, pos=[29.325, 10.423, 14.274], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_33, pos=[13.655, 7.771, 22.842], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_34, pos=[19.846, 6.026, 15.372], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_35, pos=[25.111, 11.251, 9.213], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_36, pos=[21.041, 11.554, 8.706], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_37, pos=[10.563, 2.868, 13.303], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_38, pos=[26.643, 8.970, 16.305], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_39, pos=[15.071, 7.182, 23.004], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_40, pos=[14.331, 3.240, 19.515], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_41, pos=[24.853, 9.836, 10.437], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
pseudoatom ExcludedVolume_42, pos=[15.156, -1.524, 17.120], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_42
group ph4_ExcludedVolume, ExcludedVolume_42
pseudoatom ExcludedVolume_43, pos=[22.518, 6.898, 20.151], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_43
group ph4_ExcludedVolume, ExcludedVolume_43
pseudoatom ExcludedVolume_44, pos=[28.172, 9.663, 14.725], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_44
group ph4_ExcludedVolume, ExcludedVolume_44
pseudoatom ExcludedVolume_45, pos=[20.601, 4.407, 10.288], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_45
group ph4_ExcludedVolume, ExcludedVolume_45
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
hide spheres, ph4_centers
show nb_spheres, ph4_centers
orient
