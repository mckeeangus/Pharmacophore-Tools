# nav1_7_pore/pore_site__negative — ensemble pharmacophore (42 features)
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

pseudoatom Acceptor_1, pos=[122.860, 123.030, 104.650], vdw=3.000, label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom LumpedHydrophobe_1, pos=[122.326, 125.585, 108.311], vdw=3.000, label="LumpedHydrophobe 1 (0.60)"
color ph4_LumpedHydrophobe, LumpedHydrophobe_1
group ph4_LumpedHydrophobe, LumpedHydrophobe_1
pseudoatom ExcludedVolume_2, pos=[125.285, 128.615, 109.702], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_2
group ph4_ExcludedVolume, ExcludedVolume_2
pseudoatom ExcludedVolume_3, pos=[118.571, 124.814, 108.499], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_3
group ph4_ExcludedVolume, ExcludedVolume_3
pseudoatom ExcludedVolume_4, pos=[128.884, 126.873, 113.370], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_4
group ph4_ExcludedVolume, ExcludedVolume_4
pseudoatom ExcludedVolume_5, pos=[122.094, 129.466, 107.548], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_5
group ph4_ExcludedVolume, ExcludedVolume_5
pseudoatom ExcludedVolume_6, pos=[124.017, 119.809, 106.890], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_7, pos=[122.776, 118.885, 103.729], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_8, pos=[127.282, 125.121, 109.020], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_9, pos=[121.879, 129.222, 115.534], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_10, pos=[125.197, 130.130, 109.824], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_11, pos=[120.641, 129.134, 113.060], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_12, pos=[128.473, 118.746, 107.226], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_13, pos=[129.030, 124.512, 100.526], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_14, pos=[126.226, 117.204, 106.244], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_15, pos=[130.569, 122.665, 104.011], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_16, pos=[126.537, 116.659, 104.927], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_17, pos=[122.245, 128.235, 99.688], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_18, pos=[126.529, 126.881, 104.684], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_19, pos=[124.352, 128.443, 100.272], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_20, pos=[124.518, 119.233, 108.202], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_21, pos=[128.024, 116.832, 104.622], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_22, pos=[127.906, 117.140, 102.264], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_23, pos=[120.704, 122.656, 112.388], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_24, pos=[127.558, 125.625, 98.914], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_25, pos=[125.217, 130.543, 111.281], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_26, pos=[120.576, 129.964, 110.396], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_27, pos=[129.548, 128.778, 113.382], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_28, pos=[130.610, 126.872, 114.384], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_29, pos=[119.287, 129.308, 111.270], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_30, pos=[124.960, 117.242, 106.673], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_31, pos=[123.679, 130.317, 96.014], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_32, pos=[126.218, 122.002, 112.071], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_33, pos=[122.120, 122.567, 115.196], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_34, pos=[120.638, 122.580, 114.892], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_35, pos=[125.500, 128.982, 103.850], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_36, pos=[130.690, 122.523, 101.150], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_37, pos=[123.522, 119.569, 109.315], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_38, pos=[117.007, 123.231, 108.612], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_39, pos=[129.858, 125.406, 105.257], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_40, pos=[128.374, 116.454, 103.197], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_41, pos=[130.587, 128.221, 114.108], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
