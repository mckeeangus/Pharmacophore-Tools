# gr_nr3c1/lbp__negative — ensemble pharmacophore (42 features)
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

pseudoatom Aromatic_1, pos=[30.073, 4.514, 12.728], vdw=0.500
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[30.073, 4.514, 12.728], label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom Donor_1, pos=[28.133, 6.992, 15.927], vdw=0.500
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[28.133, 6.992, 15.927], label="Donor 1 (1.00)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom ExcludedVolume_2, pos=[31.064, -1.334, 15.339], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_2
group ph4_ExcludedVolume, ExcludedVolume_2
pseudoatom ExcludedVolume_2_ctr, pos=[31.064, -1.334, 15.339], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_2_ctr
group ph4_centers, ExcludedVolume_2_ctr
pseudoatom ExcludedVolume_3, pos=[22.478, 3.780, 15.698], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_3
group ph4_ExcludedVolume, ExcludedVolume_3
pseudoatom ExcludedVolume_3_ctr, pos=[22.478, 3.780, 15.698], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_3_ctr
group ph4_centers, ExcludedVolume_3_ctr
pseudoatom ExcludedVolume_4, pos=[23.308, 8.031, 17.672], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_4
group ph4_ExcludedVolume, ExcludedVolume_4
pseudoatom ExcludedVolume_4_ctr, pos=[23.308, 8.031, 17.672], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_4_ctr
group ph4_centers, ExcludedVolume_4_ctr
pseudoatom ExcludedVolume_5, pos=[33.742, 2.058, 12.491], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_5
group ph4_ExcludedVolume, ExcludedVolume_5
pseudoatom ExcludedVolume_5_ctr, pos=[33.742, 2.058, 12.491], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_5_ctr
group ph4_centers, ExcludedVolume_5_ctr
pseudoatom ExcludedVolume_6, pos=[26.553, 9.633, 17.715], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_6_ctr, pos=[26.553, 9.633, 17.715], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_6_ctr
group ph4_centers, ExcludedVolume_6_ctr
pseudoatom ExcludedVolume_7, pos=[24.023, 9.035, 16.390], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_7_ctr, pos=[24.023, 9.035, 16.390], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_7_ctr
group ph4_centers, ExcludedVolume_7_ctr
pseudoatom ExcludedVolume_8, pos=[33.295, 1.829, 13.805], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_8_ctr, pos=[33.295, 1.829, 13.805], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_8_ctr
group ph4_centers, ExcludedVolume_8_ctr
pseudoatom ExcludedVolume_9, pos=[31.540, -1.504, 16.760], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_9_ctr, pos=[31.540, -1.504, 16.760], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_9_ctr
group ph4_centers, ExcludedVolume_9_ctr
pseudoatom ExcludedVolume_10, pos=[26.735, 10.852, 18.948], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_10_ctr, pos=[26.735, 10.852, 18.948], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_10_ctr
group ph4_centers, ExcludedVolume_10_ctr
pseudoatom ExcludedVolume_11, pos=[36.962, 8.683, 9.500], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_11_ctr, pos=[36.962, 8.683, 9.500], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_11_ctr
group ph4_centers, ExcludedVolume_11_ctr
pseudoatom ExcludedVolume_12, pos=[26.675, 3.392, 13.005], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_12_ctr, pos=[26.675, 3.392, 13.005], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_12_ctr
group ph4_centers, ExcludedVolume_12_ctr
pseudoatom ExcludedVolume_13, pos=[23.083, 7.529, 14.294], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_13_ctr, pos=[23.083, 7.529, 14.294], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_13_ctr
group ph4_centers, ExcludedVolume_13_ctr
pseudoatom ExcludedVolume_14, pos=[33.799, 11.130, 5.482], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_14_ctr, pos=[33.799, 11.130, 5.482], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_14_ctr
group ph4_centers, ExcludedVolume_14_ctr
pseudoatom ExcludedVolume_15, pos=[25.006, 3.442, 13.486], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_15_ctr, pos=[25.006, 3.442, 13.486], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_15_ctr
group ph4_centers, ExcludedVolume_15_ctr
pseudoatom ExcludedVolume_16, pos=[33.795, 6.409, 6.306], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_16_ctr, pos=[33.795, 6.409, 6.306], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_16_ctr
group ph4_centers, ExcludedVolume_16_ctr
pseudoatom ExcludedVolume_17, pos=[31.040, 11.671, 15.388], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_17_ctr, pos=[31.040, 11.671, 15.388], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_17_ctr
group ph4_centers, ExcludedVolume_17_ctr
pseudoatom ExcludedVolume_18, pos=[26.795, 3.438, 10.343], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_18_ctr, pos=[26.795, 3.438, 10.343], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_18_ctr
group ph4_centers, ExcludedVolume_18_ctr
pseudoatom ExcludedVolume_19, pos=[33.166, 7.095, 4.840], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_19_ctr, pos=[33.166, 7.095, 4.840], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_19_ctr
group ph4_centers, ExcludedVolume_19_ctr
pseudoatom ExcludedVolume_20, pos=[37.454, 9.103, 11.443], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_20_ctr, pos=[37.454, 9.103, 11.443], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_20_ctr
group ph4_centers, ExcludedVolume_20_ctr
pseudoatom ExcludedVolume_21, pos=[28.014, 5.414, 8.874], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_21_ctr, pos=[28.014, 5.414, 8.874], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_21_ctr
group ph4_centers, ExcludedVolume_21_ctr
pseudoatom ExcludedVolume_22, pos=[25.662, 1.095, 16.369], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_22_ctr, pos=[25.662, 1.095, 16.369], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_22_ctr
group ph4_centers, ExcludedVolume_22_ctr
pseudoatom ExcludedVolume_23, pos=[30.831, -3.075, 11.102], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_23_ctr, pos=[30.831, -3.075, 11.102], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_23_ctr
group ph4_centers, ExcludedVolume_23_ctr
pseudoatom ExcludedVolume_24, pos=[24.325, 5.927, 11.687], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_24_ctr, pos=[24.325, 5.927, 11.687], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_24_ctr
group ph4_centers, ExcludedVolume_24_ctr
pseudoatom ExcludedVolume_25, pos=[26.392, -0.442, 14.644], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_25_ctr, pos=[26.392, -0.442, 14.644], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_25_ctr
group ph4_centers, ExcludedVolume_25_ctr
pseudoatom ExcludedVolume_26, pos=[23.286, 7.103, 12.447], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_26_ctr, pos=[23.286, 7.103, 12.447], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_26_ctr
group ph4_centers, ExcludedVolume_26_ctr
pseudoatom ExcludedVolume_27, pos=[35.062, 5.788, 15.033], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_27_ctr, pos=[35.062, 5.788, 15.033], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_27_ctr
group ph4_centers, ExcludedVolume_27_ctr
pseudoatom ExcludedVolume_28, pos=[29.191, 12.856, 19.243], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_28_ctr, pos=[29.191, 12.856, 19.243], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_28_ctr
group ph4_centers, ExcludedVolume_28_ctr
pseudoatom ExcludedVolume_29, pos=[27.238, -1.073, 9.438], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_29_ctr, pos=[27.238, -1.073, 9.438], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_29_ctr
group ph4_centers, ExcludedVolume_29_ctr
pseudoatom ExcludedVolume_30, pos=[26.755, 15.076, 17.652], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_30_ctr, pos=[26.755, 15.076, 17.652], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_30_ctr
group ph4_centers, ExcludedVolume_30_ctr
pseudoatom ExcludedVolume_31, pos=[29.479, 14.359, 17.376], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_31_ctr, pos=[29.479, 14.359, 17.376], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_31_ctr
group ph4_centers, ExcludedVolume_31_ctr
pseudoatom ExcludedVolume_32, pos=[25.948, 2.697, 11.387], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_32_ctr, pos=[25.948, 2.697, 11.387], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_32_ctr
group ph4_centers, ExcludedVolume_32_ctr
pseudoatom ExcludedVolume_33, pos=[27.876, 15.066, 14.739], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_33_ctr, pos=[27.876, 15.066, 14.739], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_33_ctr
group ph4_centers, ExcludedVolume_33_ctr
pseudoatom ExcludedVolume_34, pos=[24.948, 10.749, 18.821], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_34_ctr, pos=[24.948, 10.749, 18.821], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_34_ctr
group ph4_centers, ExcludedVolume_34_ctr
pseudoatom ExcludedVolume_35, pos=[21.299, 3.407, 16.584], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_35_ctr, pos=[21.299, 3.407, 16.584], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_35_ctr
group ph4_centers, ExcludedVolume_35_ctr
pseudoatom ExcludedVolume_36, pos=[22.835, 8.799, 15.085], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_36_ctr, pos=[22.835, 8.799, 15.085], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_36_ctr
group ph4_centers, ExcludedVolume_36_ctr
pseudoatom ExcludedVolume_37, pos=[28.778, 1.753, 19.616], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_37_ctr, pos=[28.778, 1.753, 19.616], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_37_ctr
group ph4_centers, ExcludedVolume_37_ctr
pseudoatom ExcludedVolume_38, pos=[33.457, 12.441, 10.766], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_38_ctr, pos=[33.457, 12.441, 10.766], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_38_ctr
group ph4_centers, ExcludedVolume_38_ctr
pseudoatom ExcludedVolume_39, pos=[33.807, 10.587, 17.627], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_39_ctr, pos=[33.807, 10.587, 17.627], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_39_ctr
group ph4_centers, ExcludedVolume_39_ctr
pseudoatom ExcludedVolume_40, pos=[27.936, 1.955, 8.847], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_40_ctr, pos=[27.936, 1.955, 8.847], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_40_ctr
group ph4_centers, ExcludedVolume_40_ctr
pseudoatom ExcludedVolume_41, pos=[30.940, -3.655, 13.420], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
pseudoatom ExcludedVolume_41_ctr, pos=[30.940, -3.655, 13.420], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_41_ctr
group ph4_centers, ExcludedVolume_41_ctr
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
hide spheres, ph4_centers
show nb_spheres, ph4_centers
orient
