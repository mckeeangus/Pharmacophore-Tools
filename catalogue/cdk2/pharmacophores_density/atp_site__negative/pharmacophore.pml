# cdk2/atp_site__negative — ensemble pharmacophore (54 features)
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

pseudoatom Donor_0, pos=[7.773, -23.262, -23.622], vdw=3.000
color ph4_Donor, Donor_0
group ph4_Donor, Donor_0
pseudoatom Donor_1, pos=[1.537, -25.284, -24.046], vdw=3.000
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_2, pos=[7.718, -22.053, -22.813], vdw=3.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[3.185, -26.759, -26.265], vdw=3.000
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom PosIonizable_4, pos=[8.620, -21.413, -22.302], vdw=2.908
color ph4_PosIonizable, PosIonizable_4
group ph4_PosIonizable, PosIonizable_4
pseudoatom PosIonizable_5, pos=[4.577, -26.195, -25.469], vdw=3.000
color ph4_PosIonizable, PosIonizable_5
group ph4_PosIonizable, PosIonizable_5
pseudoatom PosIonizable_6, pos=[1.787, -22.827, -19.991], vdw=3.000
color ph4_PosIonizable, PosIonizable_6
group ph4_PosIonizable, PosIonizable_6
pseudoatom PosIonizable_7, pos=[-0.417, -26.676, -27.742], vdw=3.000
color ph4_PosIonizable, PosIonizable_7
group ph4_PosIonizable, PosIonizable_7
pseudoatom Aromatic_8, pos=[7.538, -21.839, -22.456], vdw=3.000
color ph4_Aromatic, Aromatic_8
group ph4_Aromatic, Aromatic_8
pseudoatom Aromatic_9, pos=[4.773, -25.666, -25.899], vdw=3.000
color ph4_Aromatic, Aromatic_9
group ph4_Aromatic, Aromatic_9
pseudoatom LumpedHydrophobe_10, pos=[8.073, -20.551, -21.897], vdw=2.879
color ph4_LumpedHydrophobe, LumpedHydrophobe_10
group ph4_LumpedHydrophobe, LumpedHydrophobe_10
pseudoatom LumpedHydrophobe_11, pos=[3.254, -21.244, -20.936], vdw=2.884
color ph4_LumpedHydrophobe, LumpedHydrophobe_11
group ph4_LumpedHydrophobe, LumpedHydrophobe_11
pseudoatom LumpedHydrophobe_12, pos=[4.820, -25.909, -26.098], vdw=3.000
color ph4_LumpedHydrophobe, LumpedHydrophobe_12
group ph4_LumpedHydrophobe, LumpedHydrophobe_12
pseudoatom NegIonizable_13, pos=[2.750, -19.862, -17.951], vdw=3.000
color ph4_NegIonizable, NegIonizable_13
group ph4_NegIonizable, NegIonizable_13
pseudoatom ExcludedVolume_14, pos=[11.198, -15.782, -19.952], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_15, pos=[0.432, -16.200, -19.292], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_16, pos=[5.135, -28.960, -22.439], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_17, pos=[11.318, -24.929, -25.733], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_18, pos=[9.809, -26.826, -25.993], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_19, pos=[1.122, -21.709, -30.232], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_20, pos=[12.518, -18.230, -23.220], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_21, pos=[1.503, -12.258, -18.672], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_22, pos=[2.800, -27.992, -20.669], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_23, pos=[-0.470, -14.524, -19.193], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_24, pos=[3.761, -22.510, -15.527], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_25, pos=[6.125, -29.463, -24.592], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_26, pos=[1.161, -31.064, -23.189], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_27, pos=[0.516, -14.575, -22.411], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_28, pos=[7.213, -25.644, -20.790], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_29, pos=[3.364, -23.049, -33.462], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_30, pos=[11.160, -26.365, -25.453], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_31, pos=[4.619, -18.915, -14.978], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_32, pos=[12.591, -17.559, -20.807], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_33, pos=[12.150, -16.772, -19.739], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_34, pos=[6.821, -29.110, -22.859], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_35, pos=[5.877, -30.961, -24.792], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_36, pos=[6.735, -14.511, -21.064], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_37, pos=[9.180, -28.294, -26.883], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_38, pos=[4.276, -27.828, -20.388], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_39, pos=[3.981, -17.183, -23.293], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_40, pos=[0.291, -18.733, -24.634], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_41, pos=[3.983, -22.121, -27.859], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
pseudoatom ExcludedVolume_42, pos=[1.314, -20.686, -25.980], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_42
group ph4_ExcludedVolume, ExcludedVolume_42
pseudoatom ExcludedVolume_43, pos=[5.626, -18.055, -24.993], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_43
group ph4_ExcludedVolume, ExcludedVolume_43
pseudoatom ExcludedVolume_44, pos=[2.258, -29.096, -20.496], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_44
group ph4_ExcludedVolume, ExcludedVolume_44
pseudoatom ExcludedVolume_45, pos=[3.542, -25.420, -17.376], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_45
group ph4_ExcludedVolume, ExcludedVolume_45
pseudoatom ExcludedVolume_46, pos=[1.969, -21.779, -26.363], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_46
group ph4_ExcludedVolume, ExcludedVolume_46
pseudoatom ExcludedVolume_47, pos=[9.504, -19.372, -26.000], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_47
group ph4_ExcludedVolume, ExcludedVolume_47
pseudoatom ExcludedVolume_48, pos=[13.064, -21.597, -20.476], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_48
group ph4_ExcludedVolume, ExcludedVolume_48
pseudoatom ExcludedVolume_49, pos=[8.954, -25.037, -29.401], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_49
group ph4_ExcludedVolume, ExcludedVolume_49
pseudoatom ExcludedVolume_50, pos=[-0.770, -17.895, -22.455], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_50
group ph4_ExcludedVolume, ExcludedVolume_50
pseudoatom ExcludedVolume_51, pos=[2.464, -21.808, -27.810], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_51
group ph4_ExcludedVolume, ExcludedVolume_51
pseudoatom ExcludedVolume_52, pos=[5.143, -28.950, -20.982], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_52
group ph4_ExcludedVolume, ExcludedVolume_52
pseudoatom ExcludedVolume_53, pos=[13.730, -21.665, -25.436], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_53
group ph4_ExcludedVolume, ExcludedVolume_53
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
