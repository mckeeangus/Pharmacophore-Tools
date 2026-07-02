# drd1/orthosteric__positive — ensemble pharmacophore (43 features)
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

pseudoatom Acceptor_1, pos=[122.557, 119.425, 144.084], vdw=3.000, label="Acceptor 1 (0.94)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Aromatic_1, pos=[128.000, 122.965, 146.787], vdw=3.000, label="Aromatic 1 (0.75)"
color ph4_Aromatic, Aromatic_1
group ph4_Aromatic, Aromatic_1
pseudoatom PosIonizable_1, pos=[127.451, 121.743, 142.048], vdw=3.000, label="PosIonizable 1 (0.69)"
color ph4_PosIonizable, PosIonizable_1
group ph4_PosIonizable, PosIonizable_1
pseudoatom ExcludedVolume_3, pos=[127.166, 118.077, 142.744], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_3
group ph4_ExcludedVolume, ExcludedVolume_3
pseudoatom ExcludedVolume_4, pos=[131.275, 124.556, 151.882], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_4
group ph4_ExcludedVolume, ExcludedVolume_4
pseudoatom ExcludedVolume_5, pos=[119.407, 118.786, 140.425], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_5
group ph4_ExcludedVolume, ExcludedVolume_5
pseudoatom ExcludedVolume_6, pos=[130.466, 123.147, 151.105], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_7, pos=[128.049, 124.557, 142.234], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_8, pos=[132.392, 119.135, 147.699], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_9, pos=[135.332, 122.206, 146.982], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_10, pos=[119.148, 116.851, 142.781], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_11, pos=[132.635, 120.263, 139.335], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_12, pos=[120.152, 118.476, 145.923], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_13, pos=[131.612, 127.027, 150.796], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_14, pos=[129.076, 118.681, 144.036], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_15, pos=[129.899, 122.694, 137.735], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_16, pos=[129.492, 123.320, 138.887], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_17, pos=[128.471, 122.242, 152.190], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_18, pos=[120.011, 117.628, 139.878], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_19, pos=[126.158, 118.063, 147.450], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_20, pos=[124.963, 117.148, 146.698], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_21, pos=[121.216, 123.422, 142.896], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_22, pos=[127.702, 118.411, 138.518], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_23, pos=[132.433, 120.962, 142.884], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_24, pos=[127.902, 117.098, 142.117], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_25, pos=[130.629, 118.732, 147.449], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_26, pos=[120.147, 121.066, 139.060], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_27, pos=[127.163, 124.775, 140.833], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_28, pos=[118.884, 118.764, 145.361], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_29, pos=[131.123, 123.839, 139.031], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_30, pos=[124.022, 116.582, 140.121], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_31, pos=[118.657, 117.079, 144.440], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_32, pos=[129.542, 127.447, 144.850], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_33, pos=[126.133, 122.523, 138.112], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_34, pos=[129.523, 117.300, 142.921], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_35, pos=[124.894, 121.884, 137.861], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_36, pos=[131.881, 126.231, 152.321], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_37, pos=[119.896, 115.755, 144.595], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_38, pos=[122.609, 115.093, 145.292], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_39, pos=[127.491, 119.362, 136.946], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_40, pos=[133.428, 120.085, 140.270], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_41, pos=[122.476, 123.627, 144.726], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
pseudoatom ExcludedVolume_42, pos=[123.476, 122.818, 149.679], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_42
group ph4_ExcludedVolume, ExcludedVolume_42
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
