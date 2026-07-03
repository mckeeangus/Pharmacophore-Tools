# adora2a/orthosteric__neutral — ensemble pharmacophore (42 features)
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

pseudoatom Acceptor_1, pos=[1.172, 95.304, 52.547], vdw=0.500
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[1.172, 95.304, 52.547], label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Donor_1, pos=[-1.794, 98.014, 51.587], vdw=0.500
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[-1.794, 98.014, 51.587], label="Donor 1 (0.80)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom ExcludedVolume_2, pos=[2.154, 90.967, 48.170], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_2
group ph4_ExcludedVolume, ExcludedVolume_2
pseudoatom ExcludedVolume_2_ctr, pos=[2.154, 90.967, 48.170], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_2_ctr
group ph4_centers, ExcludedVolume_2_ctr
pseudoatom ExcludedVolume_3, pos=[-0.849, 101.560, 50.837], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_3
group ph4_ExcludedVolume, ExcludedVolume_3
pseudoatom ExcludedVolume_3_ctr, pos=[-0.849, 101.560, 50.837], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_3_ctr
group ph4_centers, ExcludedVolume_3_ctr
pseudoatom ExcludedVolume_4, pos=[1.964, 96.403, 57.140], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_4
group ph4_ExcludedVolume, ExcludedVolume_4
pseudoatom ExcludedVolume_4_ctr, pos=[1.964, 96.403, 57.140], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_4_ctr
group ph4_centers, ExcludedVolume_4_ctr
pseudoatom ExcludedVolume_5, pos=[-5.820, 104.493, 54.584], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_5
group ph4_ExcludedVolume, ExcludedVolume_5
pseudoatom ExcludedVolume_5_ctr, pos=[-5.820, 104.493, 54.584], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_5_ctr
group ph4_centers, ExcludedVolume_5_ctr
pseudoatom ExcludedVolume_6, pos=[1.839, 100.296, 60.698], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_6_ctr, pos=[1.839, 100.296, 60.698], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_6_ctr
group ph4_centers, ExcludedVolume_6_ctr
pseudoatom ExcludedVolume_7, pos=[-7.206, 100.988, 52.162], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_7_ctr, pos=[-7.206, 100.988, 52.162], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_7_ctr
group ph4_centers, ExcludedVolume_7_ctr
pseudoatom ExcludedVolume_8, pos=[6.373, 95.871, 59.445], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_8_ctr, pos=[6.373, 95.871, 59.445], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_8_ctr
group ph4_centers, ExcludedVolume_8_ctr
pseudoatom ExcludedVolume_9, pos=[2.189, 98.981, 61.000], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_9_ctr, pos=[2.189, 98.981, 61.000], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_9_ctr
group ph4_centers, ExcludedVolume_9_ctr
pseudoatom ExcludedVolume_10, pos=[-3.699, 95.169, 50.190], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_10_ctr, pos=[-3.699, 95.169, 50.190], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_10_ctr
group ph4_centers, ExcludedVolume_10_ctr
pseudoatom ExcludedVolume_11, pos=[-6.496, 102.258, 50.176], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_11_ctr, pos=[-6.496, 102.258, 50.176], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_11_ctr
group ph4_centers, ExcludedVolume_11_ctr
pseudoatom ExcludedVolume_12, pos=[3.644, 97.244, 50.120], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_12_ctr, pos=[3.644, 97.244, 50.120], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_12_ctr
group ph4_centers, ExcludedVolume_12_ctr
pseudoatom ExcludedVolume_13, pos=[4.056, 88.743, 47.499], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_13_ctr, pos=[4.056, 88.743, 47.499], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_13_ctr
group ph4_centers, ExcludedVolume_13_ctr
pseudoatom ExcludedVolume_14, pos=[-1.026, 93.585, 47.796], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_14_ctr, pos=[-1.026, 93.585, 47.796], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_14_ctr
group ph4_centers, ExcludedVolume_14_ctr
pseudoatom ExcludedVolume_15, pos=[6.633, 96.892, 60.909], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_15_ctr, pos=[6.633, 96.892, 60.909], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_15_ctr
group ph4_centers, ExcludedVolume_15_ctr
pseudoatom ExcludedVolume_16, pos=[1.553, 98.328, 49.871], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_16_ctr, pos=[1.553, 98.328, 49.871], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_16_ctr
group ph4_centers, ExcludedVolume_16_ctr
pseudoatom ExcludedVolume_17, pos=[7.811, 98.242, 53.864], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_17_ctr, pos=[7.811, 98.242, 53.864], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_17_ctr
group ph4_centers, ExcludedVolume_17_ctr
pseudoatom ExcludedVolume_18, pos=[5.240, 95.891, 61.556], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_18_ctr, pos=[5.240, 95.891, 61.556], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_18_ctr
group ph4_centers, ExcludedVolume_18_ctr
pseudoatom ExcludedVolume_19, pos=[1.151, 104.961, 60.142], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_19_ctr, pos=[1.151, 104.961, 60.142], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_19_ctr
group ph4_centers, ExcludedVolume_19_ctr
pseudoatom ExcludedVolume_20, pos=[3.114, 96.097, 49.371], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_20_ctr, pos=[3.114, 96.097, 49.371], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_20_ctr
group ph4_centers, ExcludedVolume_20_ctr
pseudoatom ExcludedVolume_21, pos=[-3.732, 89.578, 49.173], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_21_ctr, pos=[-3.732, 89.578, 49.173], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_21_ctr
group ph4_centers, ExcludedVolume_21_ctr
pseudoatom ExcludedVolume_22, pos=[-3.873, 99.648, 56.484], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_22_ctr, pos=[-3.873, 99.648, 56.484], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_22_ctr
group ph4_centers, ExcludedVolume_22_ctr
pseudoatom ExcludedVolume_23, pos=[-4.367, 96.603, 50.885], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_23_ctr, pos=[-4.367, 96.603, 50.885], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_23_ctr
group ph4_centers, ExcludedVolume_23_ctr
pseudoatom ExcludedVolume_24, pos=[-0.813, 92.460, 54.643], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_24_ctr, pos=[-0.813, 92.460, 54.643], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_24_ctr
group ph4_centers, ExcludedVolume_24_ctr
pseudoatom ExcludedVolume_25, pos=[3.118, 98.959, 50.721], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_25_ctr, pos=[3.118, 98.959, 50.721], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_25_ctr
group ph4_centers, ExcludedVolume_25_ctr
pseudoatom ExcludedVolume_26, pos=[1.442, 96.667, 49.030], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_26_ctr, pos=[1.442, 96.667, 49.030], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_26_ctr
group ph4_centers, ExcludedVolume_26_ctr
pseudoatom ExcludedVolume_27, pos=[3.236, 91.109, 47.067], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_27_ctr, pos=[3.236, 91.109, 47.067], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_27_ctr
group ph4_centers, ExcludedVolume_27_ctr
pseudoatom ExcludedVolume_28, pos=[-0.368, 102.732, 49.955], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_28_ctr, pos=[-0.368, 102.732, 49.955], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_28_ctr
group ph4_centers, ExcludedVolume_28_ctr
pseudoatom ExcludedVolume_29, pos=[-4.627, 99.465, 48.726], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_29_ctr, pos=[-4.627, 99.465, 48.726], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_29_ctr
group ph4_centers, ExcludedVolume_29_ctr
pseudoatom ExcludedVolume_30, pos=[5.346, 88.931, 48.886], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_30_ctr, pos=[5.346, 88.931, 48.886], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_30_ctr
group ph4_centers, ExcludedVolume_30_ctr
pseudoatom ExcludedVolume_31, pos=[5.229, 91.011, 50.950], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_31_ctr, pos=[5.229, 91.011, 50.950], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_31_ctr
group ph4_centers, ExcludedVolume_31_ctr
pseudoatom ExcludedVolume_32, pos=[-5.604, 103.209, 58.014], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_32_ctr, pos=[-5.604, 103.209, 58.014], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_32_ctr
group ph4_centers, ExcludedVolume_32_ctr
pseudoatom ExcludedVolume_33, pos=[-3.776, 88.656, 50.119], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_33_ctr, pos=[-3.776, 88.656, 50.119], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_33_ctr
group ph4_centers, ExcludedVolume_33_ctr
pseudoatom ExcludedVolume_34, pos=[-2.800, 98.770, 55.323], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_34_ctr, pos=[-2.800, 98.770, 55.323], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_34_ctr
group ph4_centers, ExcludedVolume_34_ctr
pseudoatom ExcludedVolume_35, pos=[-4.792, 90.364, 49.315], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_35_ctr, pos=[-4.792, 90.364, 49.315], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_35_ctr
group ph4_centers, ExcludedVolume_35_ctr
pseudoatom ExcludedVolume_36, pos=[0.553, 103.713, 60.791], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_36_ctr, pos=[0.553, 103.713, 60.791], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_36_ctr
group ph4_centers, ExcludedVolume_36_ctr
pseudoatom ExcludedVolume_37, pos=[-8.041, 102.956, 56.693], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_37_ctr, pos=[-8.041, 102.956, 56.693], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_37_ctr
group ph4_centers, ExcludedVolume_37_ctr
pseudoatom ExcludedVolume_38, pos=[-7.406, 101.150, 50.760], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_38_ctr, pos=[-7.406, 101.150, 50.760], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_38_ctr
group ph4_centers, ExcludedVolume_38_ctr
pseudoatom ExcludedVolume_39, pos=[5.090, 87.499, 49.730], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_39_ctr, pos=[5.090, 87.499, 49.730], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_39_ctr
group ph4_centers, ExcludedVolume_39_ctr
pseudoatom ExcludedVolume_40, pos=[7.637, 100.305, 58.707], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_40_ctr, pos=[7.637, 100.305, 58.707], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_40_ctr
group ph4_centers, ExcludedVolume_40_ctr
pseudoatom ExcludedVolume_41, pos=[-7.356, 100.729, 57.404], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
pseudoatom ExcludedVolume_41_ctr, pos=[-7.356, 100.729, 57.404], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_41_ctr
group ph4_centers, ExcludedVolume_41_ctr
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
hide spheres, ph4_centers
show nb_spheres, ph4_centers
orient
