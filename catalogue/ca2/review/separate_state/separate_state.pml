# separate_state — 12 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 3U7C_BCT_A303.mol2, 3U7C_BCT_A303
load 6KLZ_BCT_A303.mol2, 6KLZ_BCT_A303
load 6KM0_BCT_A303.mol2, 6KM0_BCT_A303
load 6KM1_BCT_A304.mol2, 6KM1_BCT_A304
load 6KM2_BCT_A304.mol2, 6KM2_BCT_A304
load 3D92_CO2_A301.mol2, 3D92_CO2_A301
load 3D93_CO2_A301.mol2, 3D93_CO2_A301
load 3U7C_CO2_A301.mol2, 3U7C_CO2_A301
load 5Y2R_CO2_A302.mol2, 5Y2R_CO2_A302
load 5Y2S_CO2_A302.mol2, 5Y2S_CO2_A302
load 6KM1_CO2_A305.mol2, 6KM1_CO2_A305
load 6KM2_CO2_A305.mol2, 6KM2_CO2_A305
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
