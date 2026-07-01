# gaba_a/bzd_site__positive — ensemble pharmacophore (41 features)
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

pseudoatom Acceptor_1, pos=[239.843, 218.441, 240.514], vdw=2.908, label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom ExcludedVolume_1, pos=[238.807, 218.810, 237.113], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_1
group ph4_ExcludedVolume, ExcludedVolume_1
pseudoatom ExcludedVolume_2, pos=[235.223, 213.274, 247.887], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_2
group ph4_ExcludedVolume, ExcludedVolume_2
pseudoatom ExcludedVolume_3, pos=[240.666, 215.904, 242.393], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_3
group ph4_ExcludedVolume, ExcludedVolume_3
pseudoatom ExcludedVolume_4, pos=[236.761, 219.273, 238.238], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_4
group ph4_ExcludedVolume, ExcludedVolume_4
pseudoatom ExcludedVolume_5, pos=[232.768, 210.968, 236.758], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_5
group ph4_ExcludedVolume, ExcludedVolume_5
pseudoatom ExcludedVolume_6, pos=[237.536, 218.426, 237.474], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_7, pos=[234.366, 216.805, 240.431], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_8, pos=[241.530, 210.936, 241.796], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_9, pos=[242.221, 212.078, 239.678], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_10, pos=[236.812, 220.970, 239.067], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_11, pos=[233.798, 210.794, 243.088], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_12, pos=[234.619, 216.712, 237.159], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_13, pos=[236.178, 209.910, 246.286], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_14, pos=[238.522, 220.871, 238.270], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_15, pos=[239.305, 220.030, 237.509], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_16, pos=[241.066, 216.981, 243.219], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_17, pos=[234.612, 212.252, 248.216], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_18, pos=[239.014, 213.334, 247.772], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_19, pos=[232.956, 215.548, 241.245], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_20, pos=[242.499, 210.922, 240.618], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_21, pos=[231.953, 213.355, 245.289], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_22, pos=[240.152, 214.112, 246.580], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_23, pos=[239.241, 211.606, 247.258], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_24, pos=[235.522, 209.132, 238.846], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_25, pos=[240.604, 213.003, 245.900], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_26, pos=[240.158, 211.731, 246.227], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_27, pos=[238.789, 215.062, 248.279], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_28, pos=[237.025, 208.872, 241.246], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_29, pos=[232.946, 209.307, 236.514], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_30, pos=[243.698, 215.694, 241.407], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_31, pos=[233.344, 218.746, 241.522], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_32, pos=[231.607, 215.137, 245.337], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_33, pos=[233.224, 211.515, 247.113], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_34, pos=[242.966, 216.827, 242.984], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_35, pos=[232.139, 213.064, 246.630], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_36, pos=[233.358, 208.740, 238.548], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_37, pos=[230.439, 212.584, 237.347], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_38, pos=[234.760, 209.649, 247.171], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_39, pos=[237.176, 209.439, 239.703], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_40, pos=[232.936, 216.739, 237.159], vdw=1.000, label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
orient
