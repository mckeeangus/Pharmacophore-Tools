# adora2a/orthosteric__negative — ensemble pharmacophore (42 features)
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

pseudoatom Acceptor_1, pos=[1.080, 95.956, 52.586], vdw=3.000, label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[2.013, 103.408, 56.589], vdw=3.000, label="Acceptor 2 (0.52)"
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom ExcludedVolume_2, pos=[-3.699, 95.169, 50.190], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_2
group ph4_ExcludedVolume, ExcludedVolume_2
pseudoatom ExcludedVolume_3, pos=[2.154, 90.967, 48.170], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_3
group ph4_ExcludedVolume, ExcludedVolume_3
pseudoatom ExcludedVolume_4, pos=[6.373, 95.871, 59.445], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_4
group ph4_ExcludedVolume, ExcludedVolume_4
pseudoatom ExcludedVolume_5, pos=[3.114, 96.097, 49.371], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_5
group ph4_ExcludedVolume, ExcludedVolume_5
pseudoatom ExcludedVolume_6, pos=[2.189, 98.981, 61.000], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_7, pos=[1.442, 96.667, 49.030], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_8, pos=[6.633, 96.892, 60.909], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_9, pos=[-5.820, 104.493, 54.584], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_10, pos=[-2.800, 98.770, 55.323], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_11, pos=[-3.732, 89.578, 49.173], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_12, pos=[-4.367, 96.603, 50.885], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_13, pos=[-7.206, 100.988, 52.162], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_14, pos=[-5.305, 103.477, 55.359], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_15, pos=[-4.627, 99.465, 48.726], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_16, pos=[-0.813, 92.460, 54.643], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_17, pos=[-4.792, 90.364, 49.315], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_18, pos=[1.280, 103.311, 62.053], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_19, pos=[-3.247, 103.483, 60.988], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_20, pos=[-1.026, 93.585, 47.796], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_21, pos=[5.240, 95.891, 61.556], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_22, pos=[-0.368, 102.732, 49.955], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_23, pos=[-2.706, 100.408, 57.599], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_24, pos=[-1.923, 102.917, 60.846], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_25, pos=[1.964, 96.403, 57.140], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_26, pos=[1.553, 98.328, 49.871], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_27, pos=[7.811, 98.242, 53.864], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_28, pos=[4.627, 101.665, 50.932], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_29, pos=[-6.496, 102.258, 50.176], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_30, pos=[-3.776, 88.656, 50.119], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_31, pos=[6.555, 94.590, 48.648], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_32, pos=[1.151, 104.961, 60.142], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_33, pos=[-5.604, 103.209, 58.014], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_34, pos=[1.216, 88.433, 53.286], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_35, pos=[4.056, 88.743, 47.499], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_36, pos=[5.530, 91.019, 57.425], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_37, pos=[0.553, 103.713, 60.791], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_38, pos=[3.118, 98.959, 50.721], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_39, pos=[5.229, 91.011, 50.950], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_40, pos=[-7.406, 101.150, 50.760], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_41, pos=[5.920, 100.871, 67.071], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
