# cavab/dhp_site__negative — ensemble pharmacophore (43 features)
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

pseudoatom Donor_1, pos=[25.787, 163.008, 14.950], vdw=0.500
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[25.787, 163.008, 14.950], label="Donor 1 (1.00)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom Aromatic_1, pos=[25.014, 164.146, 10.827], vdw=0.500
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom Aromatic_1_ctr, pos=[25.014, 164.146, 10.827], label="Aromatic 1 (1.00)"
color ph4_Aromatic, Aromatic_1_ctr
group ph4_centers, Aromatic_1_ctr
pseudoatom PosIonizable_1, pos=[27.726, 164.777, 18.583], vdw=0.500
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom PosIonizable_1_ctr, pos=[27.726, 164.777, 18.583], label="PosIonizable 1 (0.67)"
color ph4_PosIonizable, PosIonizable_1_ctr
group ph4_centers, PosIonizable_1_ctr
pseudoatom ExcludedVolume_3, pos=[22.866, 168.267, 12.192], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_3
group ph4_ExcludedVolume, ExcludedVolume_3
pseudoatom ExcludedVolume_3_ctr, pos=[22.866, 168.267, 12.192], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_3_ctr
group ph4_centers, ExcludedVolume_3_ctr
pseudoatom ExcludedVolume_4, pos=[29.818, 163.135, 10.889], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_4
group ph4_ExcludedVolume, ExcludedVolume_4
pseudoatom ExcludedVolume_4_ctr, pos=[29.818, 163.135, 10.889], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_4_ctr
group ph4_centers, ExcludedVolume_4_ctr
pseudoatom ExcludedVolume_5, pos=[20.214, 165.937, 17.205], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_5
group ph4_ExcludedVolume, ExcludedVolume_5
pseudoatom ExcludedVolume_5_ctr, pos=[20.214, 165.937, 17.205], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_5_ctr
group ph4_centers, ExcludedVolume_5_ctr
pseudoatom ExcludedVolume_6, pos=[23.923, 170.402, 13.412], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_6_ctr, pos=[23.923, 170.402, 13.412], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_6_ctr
group ph4_centers, ExcludedVolume_6_ctr
pseudoatom ExcludedVolume_7, pos=[21.892, 166.105, 11.968], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_7_ctr, pos=[21.892, 166.105, 11.968], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_7_ctr
group ph4_centers, ExcludedVolume_7_ctr
pseudoatom ExcludedVolume_8, pos=[21.257, 167.097, 16.224], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_8_ctr, pos=[21.257, 167.097, 16.224], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_8_ctr
group ph4_centers, ExcludedVolume_8_ctr
pseudoatom ExcludedVolume_9, pos=[25.121, 171.149, 13.114], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_9_ctr, pos=[25.121, 171.149, 13.114], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_9_ctr
group ph4_centers, ExcludedVolume_9_ctr
pseudoatom ExcludedVolume_10, pos=[30.401, 164.863, 10.889], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_10_ctr, pos=[30.401, 164.863, 10.889], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_10_ctr
group ph4_centers, ExcludedVolume_10_ctr
pseudoatom ExcludedVolume_11, pos=[25.744, 170.663, 11.803], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_11_ctr, pos=[25.744, 170.663, 11.803], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_11_ctr
group ph4_centers, ExcludedVolume_11_ctr
pseudoatom ExcludedVolume_12, pos=[22.192, 167.596, 10.820], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_12_ctr, pos=[22.192, 167.596, 10.820], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_12_ctr
group ph4_centers, ExcludedVolume_12_ctr
pseudoatom ExcludedVolume_13, pos=[30.627, 165.192, 12.916], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_13_ctr, pos=[30.627, 165.192, 12.916], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_13_ctr
group ph4_centers, ExcludedVolume_13_ctr
pseudoatom ExcludedVolume_14, pos=[19.993, 166.681, 18.337], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_14_ctr, pos=[19.993, 166.681, 18.337], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_14_ctr
group ph4_centers, ExcludedVolume_14_ctr
pseudoatom ExcludedVolume_15, pos=[30.844, 169.479, 16.621], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_15_ctr, pos=[30.844, 169.479, 16.621], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_15_ctr
group ph4_centers, ExcludedVolume_15_ctr
pseudoatom ExcludedVolume_16, pos=[23.285, 168.784, 7.234], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_16_ctr, pos=[23.285, 168.784, 7.234], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_16_ctr
group ph4_centers, ExcludedVolume_16_ctr
pseudoatom ExcludedVolume_17, pos=[22.183, 168.999, 14.904], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_17_ctr, pos=[22.183, 168.999, 14.904], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_17_ctr
group ph4_centers, ExcludedVolume_17_ctr
pseudoatom ExcludedVolume_18, pos=[23.406, 170.949, 14.994], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_18_ctr, pos=[23.406, 170.949, 14.994], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_18_ctr
group ph4_centers, ExcludedVolume_18_ctr
pseudoatom ExcludedVolume_19, pos=[30.983, 166.588, 10.896], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_19_ctr, pos=[30.983, 166.588, 10.896], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_19_ctr
group ph4_centers, ExcludedVolume_19_ctr
pseudoatom ExcludedVolume_20, pos=[31.142, 166.832, 12.254], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_20_ctr, pos=[31.142, 166.832, 12.254], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_20_ctr
group ph4_centers, ExcludedVolume_20_ctr
pseudoatom ExcludedVolume_21, pos=[29.820, 169.301, 8.626], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_21_ctr, pos=[29.820, 169.301, 8.626], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_21_ctr
group ph4_centers, ExcludedVolume_21_ctr
pseudoatom ExcludedVolume_22, pos=[20.571, 165.830, 11.457], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_22_ctr, pos=[20.571, 165.830, 11.457], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_22_ctr
group ph4_centers, ExcludedVolume_22_ctr
pseudoatom ExcludedVolume_23, pos=[30.289, 168.913, 18.317], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_23_ctr, pos=[30.289, 168.913, 18.317], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_23_ctr
group ph4_centers, ExcludedVolume_23_ctr
pseudoatom ExcludedVolume_24, pos=[22.183, 169.023, 8.866], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_24_ctr, pos=[22.183, 169.023, 8.866], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_24_ctr
group ph4_centers, ExcludedVolume_24_ctr
pseudoatom ExcludedVolume_25, pos=[30.135, 171.278, 16.375], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_25_ctr, pos=[30.135, 171.278, 16.375], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_25_ctr
group ph4_centers, ExcludedVolume_25_ctr
pseudoatom ExcludedVolume_26, pos=[19.567, 165.104, 7.040], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_26_ctr, pos=[19.567, 165.104, 7.040], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_26_ctr
group ph4_centers, ExcludedVolume_26_ctr
pseudoatom ExcludedVolume_27, pos=[20.545, 167.946, 18.448], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_27_ctr, pos=[20.545, 167.946, 18.448], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_27_ctr
group ph4_centers, ExcludedVolume_27_ctr
pseudoatom ExcludedVolume_28, pos=[23.540, 166.979, 5.760], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_28_ctr, pos=[23.540, 166.979, 5.760], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_28_ctr
group ph4_centers, ExcludedVolume_28_ctr
pseudoatom ExcludedVolume_29, pos=[26.997, 171.411, 11.408], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_29_ctr, pos=[26.997, 171.411, 11.408], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_29_ctr
group ph4_centers, ExcludedVolume_29_ctr
pseudoatom ExcludedVolume_30, pos=[20.871, 165.627, 7.232], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_30_ctr, pos=[20.871, 165.627, 7.232], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_30_ctr
group ph4_centers, ExcludedVolume_30_ctr
pseudoatom ExcludedVolume_31, pos=[21.162, 169.723, 13.490], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_31_ctr, pos=[21.162, 169.723, 13.490], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_31_ctr
group ph4_centers, ExcludedVolume_31_ctr
pseudoatom ExcludedVolume_32, pos=[19.398, 164.701, 5.620], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_32_ctr, pos=[19.398, 164.701, 5.620], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_32_ctr
group ph4_centers, ExcludedVolume_32_ctr
pseudoatom ExcludedVolume_33, pos=[21.331, 168.443, 17.432], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_33_ctr, pos=[21.331, 168.443, 17.432], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_33_ctr
group ph4_centers, ExcludedVolume_33_ctr
pseudoatom ExcludedVolume_34, pos=[22.907, 168.038, 5.999], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_34_ctr, pos=[22.907, 168.038, 5.999], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_34_ctr
group ph4_centers, ExcludedVolume_34_ctr
pseudoatom ExcludedVolume_35, pos=[28.249, 170.984, 11.842], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_35_ctr, pos=[28.249, 170.984, 11.842], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_35_ctr
group ph4_centers, ExcludedVolume_35_ctr
pseudoatom ExcludedVolume_36, pos=[14.844, 160.484, 7.128], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_36_ctr, pos=[14.844, 160.484, 7.128], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_36_ctr
group ph4_centers, ExcludedVolume_36_ctr
pseudoatom ExcludedVolume_37, pos=[15.476, 158.736, 6.907], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_37_ctr, pos=[15.476, 158.736, 6.907], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_37_ctr
group ph4_centers, ExcludedVolume_37_ctr
pseudoatom ExcludedVolume_38, pos=[17.580, 164.155, 14.212], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_38_ctr, pos=[17.580, 164.155, 14.212], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_38_ctr
group ph4_centers, ExcludedVolume_38_ctr
pseudoatom ExcludedVolume_39, pos=[26.051, 173.266, 17.283], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_39_ctr, pos=[26.051, 173.266, 17.283], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_39_ctr
group ph4_centers, ExcludedVolume_39_ctr
pseudoatom ExcludedVolume_40, pos=[31.623, 168.180, 12.750], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_40_ctr, pos=[31.623, 168.180, 12.750], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_40_ctr
group ph4_centers, ExcludedVolume_40_ctr
pseudoatom ExcludedVolume_41, pos=[31.418, 159.211, 8.880], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
pseudoatom ExcludedVolume_41_ctr, pos=[31.418, 159.211, 8.880], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_41_ctr
group ph4_centers, ExcludedVolume_41_ctr
pseudoatom ExcludedVolume_42, pos=[24.810, 172.636, 13.025], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_42
group ph4_ExcludedVolume, ExcludedVolume_42
pseudoatom ExcludedVolume_42_ctr, pos=[24.810, 172.636, 13.025], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_42_ctr
group ph4_centers, ExcludedVolume_42_ctr
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
hide spheres, ph4_centers
show nb_spheres, ph4_centers
orient
