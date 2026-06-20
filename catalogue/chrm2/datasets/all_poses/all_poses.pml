# all_poses — 13 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 5YC8_3C0_A501.mol2, 5YC8_3C0_A501
load 5ZK8_3C0_A501.mol2, 5ZK8_3C0_A501
load 5ZKC_3C0_A501.mol2, 5ZKC_3C0_A501
load 5ZKB_82F_A1201.mol2, 5ZKB_82F_A1201
load 7T8X_ACH_A501.mol2, 7T8X_ACH_A501
load 7T90_ACH_A501.mol2, 7T90_ACH_A501
load 7T94_ACH_A501.mol2, 7T94_ACH_A501
load 7T96_ACH_A501.mol2, 7T96_ACH_A501
load 4MQS_IXO_A501.mol2, 4MQS_IXO_A501
load 4MQT_IXO_A501.mol2, 4MQT_IXO_A501
load 6OIK_IXO_R501.mol2, 6OIK_IXO_R501
load 3UON_QNB_A1162.mol2, 3UON_QNB_A1162
load 5ZK3_QNB_A501.mol2, 5ZK3_QNB_A501
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
