# quarantine — 1 molecules (reference frame; protein omitted)
reinitialize
bg_color white
set valence, 1

load 5IKQ_JMS_B602.mol2, 5IKQ_JMS_B602
show sticks
hide everything, hydro
util.cbag *
set stick_radius, 0.16
orient
