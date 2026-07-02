# hiv1_protease/active_site__negative — ensemble pharmacophore (46 features)
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

pseudoatom Donor_1, pos=[-9.609, 17.821, 26.583], vdw=3.000, label="Donor 1 (0.91)"
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Acceptor_1, pos=[-8.251, 15.094, 26.955], vdw=3.000, label="Acceptor 1 (0.94)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_2, pos=[-11.434, 15.165, 34.169], vdw=3.000, label="Acceptor 2 (0.75)"
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_3, pos=[-7.363, 17.910, 20.841], vdw=3.000, label="Acceptor 3 (0.75)"
color ph4_Acceptor, Acceptor_3
group ph4_Acceptor, Acceptor_3
pseudoatom LumpedHydrophobe_1, pos=[-4.803, 18.263, 26.434], vdw=3.000, label="LumpedHydrophobe 1 (0.94)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom LumpedHydrophobe_2, pos=[-13.095, 13.183, 29.044], vdw=3.000, label="LumpedHydrophobe 2 (0.91)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_2
group ph4_LumpedHydrophobe, LumpedHydrophobe_2
pseudoatom ExcludedVolume_6, pos=[-10.362, 17.745, 17.563], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_7, pos=[-1.095, 16.053, 29.195], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_8, pos=[-18.126, 15.732, 32.565], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_9, pos=[-18.477, 13.440, 32.131], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_10, pos=[-2.993, 22.044, 21.845], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_11, pos=[-10.706, 12.784, 41.236], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_12, pos=[-9.524, 21.037, 29.345], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_13, pos=[-5.956, 21.049, 19.950], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_14, pos=[-17.221, 11.959, 28.568], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_15, pos=[-11.272, 18.888, 37.264], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_16, pos=[-11.285, 16.689, 39.540], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_17, pos=[-15.768, 15.571, 35.561], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_18, pos=[-8.279, 13.762, 20.276], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_19, pos=[-13.357, 18.405, 34.674], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_20, pos=[-11.136, 18.986, 17.918], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_21, pos=[-8.948, 21.733, 24.926], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_22, pos=[-9.284, 20.958, 20.983], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_23, pos=[-11.032, 21.646, 29.428], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_24, pos=[-6.807, 21.926, 20.080], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_25, pos=[-10.020, 21.011, 18.677], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_26, pos=[-12.940, 20.590, 26.561], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_27, pos=[-7.366, 14.101, 35.509], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_28, pos=[-12.445, 18.389, 19.160], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_29, pos=[-13.850, 8.802, 26.856], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_30, pos=[-9.702, 19.808, 37.085], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_31, pos=[-5.656, 19.392, 30.856], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_32, pos=[-3.823, 22.743, 22.641], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_33, pos=[-15.773, 16.783, 35.536], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_34, pos=[-2.909, 20.441, 27.990], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_35, pos=[-4.305, 13.258, 27.077], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_36, pos=[-14.217, 19.198, 30.961], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_37, pos=[-10.625, 12.455, 23.406], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_38, pos=[-11.140, 19.916, 32.741], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_39, pos=[-14.295, 17.998, 31.125], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_40, pos=[-6.819, 22.767, 20.976], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_41, pos=[-14.448, 8.841, 28.264], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
pseudoatom ExcludedVolume_42, pos=[-4.385, 13.584, 23.547], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_42
group ph4_ExcludedVolume, ExcludedVolume_42
pseudoatom ExcludedVolume_43, pos=[-9.375, 10.635, 32.279], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_43
group ph4_ExcludedVolume, ExcludedVolume_43
pseudoatom ExcludedVolume_44, pos=[-0.157, 17.301, 27.349], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_44
group ph4_ExcludedVolume, ExcludedVolume_44
pseudoatom ExcludedVolume_45, pos=[-4.600, 12.994, 24.685], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_45
group ph4_ExcludedVolume, ExcludedVolume_45
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
