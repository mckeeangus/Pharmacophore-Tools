# adora2a/orthosteric__negative — ensemble pharmacophore (52 features)
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

pseudoatom Donor_0, pos=[-0.871, 97.935, 52.383], vdw=2.971
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[1.491, 103.711, 56.034], vdw=3.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[1.080, 95.956, 52.586], vdw=3.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[2.013, 103.408, 56.589], vdw=3.000
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom Aromatic_4, pos=[0.847, 95.368, 52.362], vdw=3.000
color ph4_Aromatic, Aromatic_4
group ph4_Aromatic, Aromatic_4
pseudoatom Aromatic_5, pos=[1.293, 101.699, 55.550], vdw=3.000
color ph4_Aromatic, Aromatic_5
group ph4_Aromatic, Aromatic_5
pseudoatom LumpedHydrophobe_6, pos=[0.647, 102.761, 55.584], vdw=2.477
color ph4_LumpedHydrophobe, LumpedHydrophobe_6
group ph4_LumpedHydrophobe, LumpedHydrophobe_6
pseudoatom LumpedHydrophobe_7, pos=[-0.171, 92.432, 50.938], vdw=2.787
color ph4_LumpedHydrophobe, LumpedHydrophobe_7
group ph4_LumpedHydrophobe, LumpedHydrophobe_7
pseudoatom LumpedHydrophobe_8, pos=[-2.815, 106.048, 56.769], vdw=2.664
color ph4_LumpedHydrophobe, LumpedHydrophobe_8
group ph4_LumpedHydrophobe, LumpedHydrophobe_8
pseudoatom LumpedHydrophobe_9, pos=[2.600, 97.311, 54.227], vdw=3.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_9
group ph4_LumpedHydrophobe, LumpedHydrophobe_9
pseudoatom PosIonizable_10, pos=[0.968, 97.102, 52.906], vdw=2.902
color ph4_PosIonizable, PosIonizable_10
group ph4_PosIonizable, PosIonizable_10
pseudoatom PosIonizable_11, pos=[1.079, 102.457, 55.855], vdw=3.000
color ph4_PosIonizable, PosIonizable_11
group ph4_PosIonizable, PosIonizable_11
pseudoatom ExcludedVolume_12, pos=[-3.699, 95.169, 50.190], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_13, pos=[2.154, 90.967, 48.170], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_14, pos=[6.373, 95.871, 59.445], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_15, pos=[3.114, 96.097, 49.371], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_16, pos=[2.189, 98.981, 61.000], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_17, pos=[1.442, 96.667, 49.030], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_18, pos=[6.633, 96.892, 60.909], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_19, pos=[-5.820, 104.493, 54.584], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_20, pos=[-2.800, 98.770, 55.323], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_21, pos=[-3.732, 89.578, 49.173], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_22, pos=[-4.367, 96.603, 50.885], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_23, pos=[-7.206, 100.988, 52.162], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_24, pos=[-5.305, 103.477, 55.359], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_25, pos=[-4.627, 99.465, 48.726], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_26, pos=[-0.813, 92.460, 54.643], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_27, pos=[-4.792, 90.364, 49.315], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_28, pos=[1.280, 103.311, 62.053], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_29, pos=[-3.247, 103.483, 60.988], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_30, pos=[-1.026, 93.585, 47.796], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_31, pos=[5.240, 95.891, 61.556], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_32, pos=[-0.368, 102.732, 49.955], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_33, pos=[-2.706, 100.408, 57.599], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_34, pos=[-1.923, 102.917, 60.846], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_35, pos=[1.964, 96.403, 57.140], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_36, pos=[1.553, 98.328, 49.871], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_37, pos=[7.811, 98.242, 53.864], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_38, pos=[4.627, 101.665, 50.932], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_39, pos=[-6.496, 102.258, 50.176], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_40, pos=[-3.776, 88.656, 50.119], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_41, pos=[6.555, 94.590, 48.648], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
pseudoatom ExcludedVolume_42, pos=[1.151, 104.961, 60.142], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_42
group ph4_ExcludedVolume, ExcludedVolume_42
pseudoatom ExcludedVolume_43, pos=[-5.604, 103.209, 58.014], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_43
group ph4_ExcludedVolume, ExcludedVolume_43
pseudoatom ExcludedVolume_44, pos=[1.216, 88.433, 53.286], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_44
group ph4_ExcludedVolume, ExcludedVolume_44
pseudoatom ExcludedVolume_45, pos=[4.056, 88.743, 47.499], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_45
group ph4_ExcludedVolume, ExcludedVolume_45
pseudoatom ExcludedVolume_46, pos=[5.530, 91.019, 57.425], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_46
group ph4_ExcludedVolume, ExcludedVolume_46
pseudoatom ExcludedVolume_47, pos=[0.553, 103.713, 60.791], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_47
group ph4_ExcludedVolume, ExcludedVolume_47
pseudoatom ExcludedVolume_48, pos=[3.118, 98.959, 50.721], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_48
group ph4_ExcludedVolume, ExcludedVolume_48
pseudoatom ExcludedVolume_49, pos=[5.229, 91.011, 50.950], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_49
group ph4_ExcludedVolume, ExcludedVolume_49
pseudoatom ExcludedVolume_50, pos=[-7.406, 101.150, 50.760], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_50
group ph4_ExcludedVolume, ExcludedVolume_50
pseudoatom ExcludedVolume_51, pos=[5.920, 100.871, 67.071], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_51
group ph4_ExcludedVolume, ExcludedVolume_51
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
