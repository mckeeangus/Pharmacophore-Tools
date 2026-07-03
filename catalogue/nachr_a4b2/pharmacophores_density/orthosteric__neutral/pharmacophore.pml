# nachr_a4b2/orthosteric__neutral — ensemble pharmacophore (43 features)
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

pseudoatom Acceptor_1, pos=[169.083, 121.144, 184.892], vdw=0.500
color ph4_Acceptor, Acceptor_1
group ph4_Acceptor, Acceptor_1
pseudoatom Acceptor_1_ctr, pos=[169.083, 121.144, 184.892], label="Acceptor 1 (1.00)"
color ph4_Acceptor, Acceptor_1_ctr
group ph4_centers, Acceptor_1_ctr
pseudoatom Acceptor_2, pos=[163.031, 123.987, 180.657], vdw=0.500
color ph4_Acceptor, Acceptor_2
group ph4_Acceptor, Acceptor_2
pseudoatom Acceptor_2_ctr, pos=[163.031, 123.987, 180.657], label="Acceptor 2 (0.56)"
color ph4_Acceptor, Acceptor_2_ctr
group ph4_centers, Acceptor_2_ctr
pseudoatom Donor_1, pos=[170.890, 120.757, 182.363], vdw=0.500
color ph4_Donor, Donor_1
group ph4_Donor, Donor_1
pseudoatom Donor_1_ctr, pos=[170.890, 120.757, 182.363], label="Donor 1 (0.56)"
color ph4_Donor, Donor_1_ctr
group ph4_centers, Donor_1_ctr
pseudoatom ExcludedVolume_3, pos=[163.179, 125.191, 184.562], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_3
group ph4_ExcludedVolume, ExcludedVolume_3
pseudoatom ExcludedVolume_3_ctr, pos=[163.179, 125.191, 184.562], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_3_ctr
group ph4_centers, ExcludedVolume_3_ctr
pseudoatom ExcludedVolume_4, pos=[159.302, 126.122, 181.311], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_4
group ph4_ExcludedVolume, ExcludedVolume_4
pseudoatom ExcludedVolume_4_ctr, pos=[159.302, 126.122, 181.311], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_4_ctr
group ph4_centers, ExcludedVolume_4_ctr
pseudoatom ExcludedVolume_5, pos=[167.428, 112.094, 182.688], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_5
group ph4_ExcludedVolume, ExcludedVolume_5
pseudoatom ExcludedVolume_5_ctr, pos=[167.428, 112.094, 182.688], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_5_ctr
group ph4_centers, ExcludedVolume_5_ctr
pseudoatom ExcludedVolume_6, pos=[169.034, 114.886, 189.331], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_6
group ph4_ExcludedVolume, ExcludedVolume_6
pseudoatom ExcludedVolume_6_ctr, pos=[169.034, 114.886, 189.331], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_6_ctr
group ph4_centers, ExcludedVolume_6_ctr
pseudoatom ExcludedVolume_7, pos=[164.422, 116.588, 180.179], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_7
group ph4_ExcludedVolume, ExcludedVolume_7
pseudoatom ExcludedVolume_7_ctr, pos=[164.422, 116.588, 180.179], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_7_ctr
group ph4_centers, ExcludedVolume_7_ctr
pseudoatom ExcludedVolume_8, pos=[159.866, 124.823, 181.834], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_8
group ph4_ExcludedVolume, ExcludedVolume_8
pseudoatom ExcludedVolume_8_ctr, pos=[159.866, 124.823, 181.834], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_8_ctr
group ph4_centers, ExcludedVolume_8_ctr
pseudoatom ExcludedVolume_9, pos=[166.339, 127.374, 184.878], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_9
group ph4_ExcludedVolume, ExcludedVolume_9
pseudoatom ExcludedVolume_9_ctr, pos=[166.339, 127.374, 184.878], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_9_ctr
group ph4_centers, ExcludedVolume_9_ctr
pseudoatom ExcludedVolume_10, pos=[167.952, 126.764, 180.731], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_10
group ph4_ExcludedVolume, ExcludedVolume_10
pseudoatom ExcludedVolume_10_ctr, pos=[167.952, 126.764, 180.731], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_10_ctr
group ph4_centers, ExcludedVolume_10_ctr
pseudoatom ExcludedVolume_11, pos=[165.966, 112.343, 182.386], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_11
group ph4_ExcludedVolume, ExcludedVolume_11
pseudoatom ExcludedVolume_11_ctr, pos=[165.966, 112.343, 182.386], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_11_ctr
group ph4_centers, ExcludedVolume_11_ctr
pseudoatom ExcludedVolume_12, pos=[164.948, 119.281, 187.536], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_12
group ph4_ExcludedVolume, ExcludedVolume_12
pseudoatom ExcludedVolume_12_ctr, pos=[164.948, 119.281, 187.536], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_12_ctr
group ph4_centers, ExcludedVolume_12_ctr
pseudoatom ExcludedVolume_13, pos=[167.476, 123.983, 189.029], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_13
group ph4_ExcludedVolume, ExcludedVolume_13
pseudoatom ExcludedVolume_13_ctr, pos=[167.476, 123.983, 189.029], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_13_ctr
group ph4_centers, ExcludedVolume_13_ctr
pseudoatom ExcludedVolume_14, pos=[168.751, 127.385, 184.903], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_14
group ph4_ExcludedVolume, ExcludedVolume_14
pseudoatom ExcludedVolume_14_ctr, pos=[168.751, 127.385, 184.903], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_14_ctr
group ph4_centers, ExcludedVolume_14_ctr
pseudoatom ExcludedVolume_15, pos=[167.166, 121.384, 178.281], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_15
group ph4_ExcludedVolume, ExcludedVolume_15
pseudoatom ExcludedVolume_15_ctr, pos=[167.166, 121.384, 178.281], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_15_ctr
group ph4_centers, ExcludedVolume_15_ctr
pseudoatom ExcludedVolume_16, pos=[174.315, 120.894, 186.889], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_16
group ph4_ExcludedVolume, ExcludedVolume_16
pseudoatom ExcludedVolume_16_ctr, pos=[174.315, 120.894, 186.889], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_16_ctr
group ph4_centers, ExcludedVolume_16_ctr
pseudoatom ExcludedVolume_17, pos=[169.182, 127.285, 186.757], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_17
group ph4_ExcludedVolume, ExcludedVolume_17
pseudoatom ExcludedVolume_17_ctr, pos=[169.182, 127.285, 186.757], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_17_ctr
group ph4_centers, ExcludedVolume_17_ctr
pseudoatom ExcludedVolume_18, pos=[166.613, 118.771, 188.092], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_18
group ph4_ExcludedVolume, ExcludedVolume_18
pseudoatom ExcludedVolume_18_ctr, pos=[166.613, 118.771, 188.092], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_18_ctr
group ph4_centers, ExcludedVolume_18_ctr
pseudoatom ExcludedVolume_19, pos=[170.373, 116.684, 179.071], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_19
group ph4_ExcludedVolume, ExcludedVolume_19
pseudoatom ExcludedVolume_19_ctr, pos=[170.373, 116.684, 179.071], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_19_ctr
group ph4_centers, ExcludedVolume_19_ctr
pseudoatom ExcludedVolume_20, pos=[162.420, 127.383, 183.050], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_20
group ph4_ExcludedVolume, ExcludedVolume_20
pseudoatom ExcludedVolume_20_ctr, pos=[162.420, 127.383, 183.050], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_20_ctr
group ph4_centers, ExcludedVolume_20_ctr
pseudoatom ExcludedVolume_21, pos=[161.987, 128.561, 182.208], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_21
group ph4_ExcludedVolume, ExcludedVolume_21
pseudoatom ExcludedVolume_21_ctr, pos=[161.987, 128.561, 182.208], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_21_ctr
group ph4_centers, ExcludedVolume_21_ctr
pseudoatom ExcludedVolume_22, pos=[169.416, 112.818, 185.981], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_22
group ph4_ExcludedVolume, ExcludedVolume_22
pseudoatom ExcludedVolume_22_ctr, pos=[169.416, 112.818, 185.981], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_22_ctr
group ph4_centers, ExcludedVolume_22_ctr
pseudoatom ExcludedVolume_23, pos=[169.189, 126.114, 180.838], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_23
group ph4_ExcludedVolume, ExcludedVolume_23
pseudoatom ExcludedVolume_23_ctr, pos=[169.189, 126.114, 180.838], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_23_ctr
group ph4_centers, ExcludedVolume_23_ctr
pseudoatom ExcludedVolume_24, pos=[165.941, 122.981, 176.995], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_24
group ph4_ExcludedVolume, ExcludedVolume_24
pseudoatom ExcludedVolume_24_ctr, pos=[165.941, 122.981, 176.995], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_24_ctr
group ph4_centers, ExcludedVolume_24_ctr
pseudoatom ExcludedVolume_25, pos=[166.866, 127.284, 186.618], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_25
group ph4_ExcludedVolume, ExcludedVolume_25
pseudoatom ExcludedVolume_25_ctr, pos=[166.866, 127.284, 186.618], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_25_ctr
group ph4_centers, ExcludedVolume_25_ctr
pseudoatom ExcludedVolume_26, pos=[169.387, 118.751, 193.188], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_26
group ph4_ExcludedVolume, ExcludedVolume_26
pseudoatom ExcludedVolume_26_ctr, pos=[169.387, 118.751, 193.188], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_26_ctr
group ph4_centers, ExcludedVolume_26_ctr
pseudoatom ExcludedVolume_27, pos=[178.092, 117.861, 182.017], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_27
group ph4_ExcludedVolume, ExcludedVolume_27
pseudoatom ExcludedVolume_27_ctr, pos=[178.092, 117.861, 182.017], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_27_ctr
group ph4_centers, ExcludedVolume_27_ctr
pseudoatom ExcludedVolume_28, pos=[163.188, 115.735, 182.178], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_28
group ph4_ExcludedVolume, ExcludedVolume_28
pseudoatom ExcludedVolume_28_ctr, pos=[163.188, 115.735, 182.178], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_28_ctr
group ph4_centers, ExcludedVolume_28_ctr
pseudoatom ExcludedVolume_29, pos=[172.149, 116.296, 180.992], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_29
group ph4_ExcludedVolume, ExcludedVolume_29
pseudoatom ExcludedVolume_29_ctr, pos=[172.149, 116.296, 180.992], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_29_ctr
group ph4_centers, ExcludedVolume_29_ctr
pseudoatom ExcludedVolume_30, pos=[166.109, 121.630, 177.658], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_30
group ph4_ExcludedVolume, ExcludedVolume_30
pseudoatom ExcludedVolume_30_ctr, pos=[166.109, 121.630, 177.658], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_30_ctr
group ph4_centers, ExcludedVolume_30_ctr
pseudoatom ExcludedVolume_31, pos=[160.654, 119.461, 180.890], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_31
group ph4_ExcludedVolume, ExcludedVolume_31
pseudoatom ExcludedVolume_31_ctr, pos=[160.654, 119.461, 180.890], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_31_ctr
group ph4_centers, ExcludedVolume_31_ctr
pseudoatom ExcludedVolume_32, pos=[162.247, 120.964, 178.083], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_32
group ph4_ExcludedVolume, ExcludedVolume_32
pseudoatom ExcludedVolume_32_ctr, pos=[162.247, 120.964, 178.083], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_32_ctr
group ph4_centers, ExcludedVolume_32_ctr
pseudoatom ExcludedVolume_33, pos=[164.222, 114.126, 182.122], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_33
group ph4_ExcludedVolume, ExcludedVolume_33
pseudoatom ExcludedVolume_33_ctr, pos=[164.222, 114.126, 182.122], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_33_ctr
group ph4_centers, ExcludedVolume_33_ctr
pseudoatom ExcludedVolume_34, pos=[176.812, 119.755, 186.802], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_34
group ph4_ExcludedVolume, ExcludedVolume_34
pseudoatom ExcludedVolume_34_ctr, pos=[176.812, 119.755, 186.802], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_34_ctr
group ph4_centers, ExcludedVolume_34_ctr
pseudoatom ExcludedVolume_35, pos=[175.851, 120.679, 178.772], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_35
group ph4_ExcludedVolume, ExcludedVolume_35
pseudoatom ExcludedVolume_35_ctr, pos=[175.851, 120.679, 178.772], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_35_ctr
group ph4_centers, ExcludedVolume_35_ctr
pseudoatom ExcludedVolume_36, pos=[173.146, 120.814, 192.233], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_36
group ph4_ExcludedVolume, ExcludedVolume_36
pseudoatom ExcludedVolume_36_ctr, pos=[173.146, 120.814, 192.233], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_36_ctr
group ph4_centers, ExcludedVolume_36_ctr
pseudoatom ExcludedVolume_37, pos=[169.122, 127.204, 188.469], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_37
group ph4_ExcludedVolume, ExcludedVolume_37
pseudoatom ExcludedVolume_37_ctr, pos=[169.122, 127.204, 188.469], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_37_ctr
group ph4_centers, ExcludedVolume_37_ctr
pseudoatom ExcludedVolume_38, pos=[158.321, 126.740, 182.286], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_38
group ph4_ExcludedVolume, ExcludedVolume_38
pseudoatom ExcludedVolume_38_ctr, pos=[158.321, 126.740, 182.286], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_38_ctr
group ph4_centers, ExcludedVolume_38_ctr
pseudoatom ExcludedVolume_39, pos=[168.005, 112.730, 186.551], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_39
group ph4_ExcludedVolume, ExcludedVolume_39
pseudoatom ExcludedVolume_39_ctr, pos=[168.005, 112.730, 186.551], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_39_ctr
group ph4_centers, ExcludedVolume_39_ctr
pseudoatom ExcludedVolume_40, pos=[176.039, 123.340, 181.681], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_40
group ph4_ExcludedVolume, ExcludedVolume_40
pseudoatom ExcludedVolume_40_ctr, pos=[176.039, 123.340, 181.681], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_40_ctr
group ph4_centers, ExcludedVolume_40_ctr
pseudoatom ExcludedVolume_41, pos=[162.367, 126.153, 185.115], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_41
group ph4_ExcludedVolume, ExcludedVolume_41
pseudoatom ExcludedVolume_41_ctr, pos=[162.367, 126.153, 185.115], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_41_ctr
group ph4_centers, ExcludedVolume_41_ctr
pseudoatom ExcludedVolume_42, pos=[163.793, 124.240, 189.280], vdw=0.500
color ph4_ExcludedVolume, ExcludedVolume_42
group ph4_ExcludedVolume, ExcludedVolume_42
pseudoatom ExcludedVolume_42_ctr, pos=[163.793, 124.240, 189.280], label="ExcludedVolume (0.00)"
color ph4_ExcludedVolume, ExcludedVolume_42_ctr
group ph4_centers, ExcludedVolume_42_ctr
show spheres, ph4_*
set sphere_transparency, 0.4, ph4_*
hide spheres, ph4_centers
show nb_spheres, ph4_centers
orient
