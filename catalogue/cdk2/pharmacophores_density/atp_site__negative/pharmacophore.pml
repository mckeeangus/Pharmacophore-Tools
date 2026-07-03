# cdk2/atp_site__negative — ensemble pharmacophore (42 features)
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

pseudoatom Acceptor_1, pos=[7.911, -22.142, -22.974], vdw=2.000
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[7.911, -22.142, -22.974], label="Acceptor 1 (0.98)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Acceptor_2, pos=[3.364, -26.655, -26.140], vdw=2.000
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[3.364, -26.655, -26.140], label="Acceptor 2 (0.61)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom ExcludedVolume_2, pos=[11.198, -15.782, -19.952], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_2
group ph4_ExcludedVolume, ExcludedVolume_2
pseudoatom ExcludedVolume_3, pos=[0.432, -16.200, -19.292], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_3
group ph4_ExcludedVolume, ExcludedVolume_3
pseudoatom ExcludedVolume_4, pos=[5.135, -28.960, -22.439], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_4
group ph4_ExcludedVolume, ExcludedVolume_4
pseudoatom ExcludedVolume_5, pos=[11.318, -24.929, -25.733], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_5
group ph4_ExcludedVolume, ExcludedVolume_5
pseudoatom ExcludedVolume_6, pos=[9.809, -26.826, -25.993], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_7, pos=[1.122, -21.709, -30.232], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_8, pos=[12.518, -18.230, -23.220], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_9, pos=[1.503, -12.258, -18.672], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_10, pos=[2.800, -27.992, -20.669], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_11, pos=[-0.470, -14.524, -19.193], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_12, pos=[3.761, -22.510, -15.527], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_13, pos=[6.125, -29.463, -24.592], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_14, pos=[1.161, -31.064, -23.189], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_15, pos=[0.516, -14.575, -22.411], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_16, pos=[7.213, -25.644, -20.790], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_17, pos=[3.364, -23.049, -33.462], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_18, pos=[11.160, -26.365, -25.453], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_19, pos=[4.619, -18.915, -14.978], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_20, pos=[12.591, -17.559, -20.807], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_21, pos=[12.150, -16.772, -19.739], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_22, pos=[6.821, -29.110, -22.859], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_23, pos=[5.877, -30.961, -24.792], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_24, pos=[6.735, -14.511, -21.064], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_25, pos=[9.180, -28.294, -26.883], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_26, pos=[4.276, -27.828, -20.388], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_27, pos=[3.981, -17.183, -23.293], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_28, pos=[0.291, -18.733, -24.634], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_29, pos=[3.983, -22.121, -27.859], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_30, pos=[1.314, -20.686, -25.980], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_31, pos=[5.626, -18.055, -24.993], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_32, pos=[2.258, -29.096, -20.496], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_33, pos=[3.542, -25.420, -17.376], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_34, pos=[1.969, -21.779, -26.363], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_35, pos=[9.504, -19.372, -26.000], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_36, pos=[13.064, -21.597, -20.476], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_37, pos=[8.954, -25.037, -29.401], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_38, pos=[-0.770, -17.895, -22.455], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_39, pos=[2.464, -21.808, -27.810], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_40, pos=[5.143, -28.950, -20.982], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_41, pos=[13.730, -21.665, -25.436], vdw=1.000
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
hide spheres, ph4_centers
show nb_spheres, ph4_centers
orient
