# Literature efficacy curation — batch 2 notes

Targets: `adora2a`, `chrm2`, `gr_nr3c1`, `nav1_7_pore`, `nav1_7_vsd4`
Outcome: **56 resolved** (55 efficacy + 1 `separate_state`), **5 unknown**.
Abstracts retrieved from **PubMed**; DOI links below.

## Left unknown (5)

| het | target | pdb / pmid | reason |
|---|---|---|---|
| 9Y2   | adora2a      | 5OLV / 29311713 | in-meso soaking *methods* paper; soaked screening ligand, no functional/efficacy assay. Binding only. |
| A1COM | adora2a      | 7IN9 / 42129437 | crystallographic fragment; binding confirmed by GCI, no functional direction assayed. |
| A1COV | adora2a      | 7INI / 42129437 | crystallographic fragment; binding only. |
| A1COY | adora2a      | 7INL / 42129437 | crystallographic fragment; binding only. |
| 9Z9   | nav1_7_pore  | 7W9K / 35476982 | **likely mispaired.** (25R)-spirost-5-ene 3-O-ether = glyco-diosgenin (GDN)-type detergent/sterol; also appears in the same group's Nav1.1 structure (7DTD). Primary paper characterises toxin-induced S6 alpha->pi gating, not a small-molecule pore blocker. Routed out as a non-pharmacological additive. |

## Calls worth a second glance

- **LJX** (8CU6) is the *antagonist* product of the agonist->antagonist switch paper (LJ-4517, C8-thiophene, Ki ~18 nM) -> `negative`, not positive.
- The five **A1H3*** xanthines are istradefylline-derived photo-*affinity* switches (modulate binding kinetics, not efficacy) -> all `negative`.
- **A1H1S** (LUF5834) and **RVZ** are confirmed dicyanopyridine *partial agonists* -> `positive`.
- **WCH** is photoNECA, a NECA / 2-substituted-adenosine agonist scaffold -> `positive` (medium).
- **QJK** is a GR/14-3-3 *molecular glue* (binds the 14-3-3 interface, not the steroid LBD) -> `track: separate_state`.
- `chrm2` rows are all orthosteric; none is the extracellular-vestibule allosteric modulator, so the vestibule caveat did not apply this batch.

## Medium-confidence rows that could be promoted to high via full text

- `A1IR0`, `A1IR1` (PMID 40592852, open access) — confirm antagonism of the two co-crystallised binders against the functional assay.
- GR SGRM `positive`s (`8W5`, `8W8`, `A1ACE`, `LSJ`, `NN7`, `R8C`) — anchored to chemotype/class rather than an explicit efficacy statement in the abstract.
- `8JN`, `WCH` — chemotype-anchored.

## Sources (PubMed; DOI links)

adora2a:
- 27312113  https://doi.org/10.1021/acs.jmedchem.6b00653
- 28167788  https://doi.org/10.1073/pnas.1621423114
- 35174942  https://doi.org/10.1002/anie.202115545
- 28712806  https://doi.org/10.1016/j.str.2017.06.012
- 42084562  https://doi.org/10.1021/acs.jmedchem.5c03405
- 42129437  https://doi.org/10.1038/s42004-026-02059-7
- 38751633  https://doi.org/10.1021/acsptsci.4c00051
- 39738009  https://doi.org/10.1038/s41467-024-55109-w
- 40592852  https://doi.org/10.1038/s41467-025-60629-0
- 35977382  https://doi.org/10.1021/acs.jmedchem.2c00462
- 32542862  https://doi.org/10.1002/anie.202003788
- 33764785  https://doi.org/10.1021/acs.jmedchem.0c01856
- 22220592  https://doi.org/10.1021/jm201376w
- 35933788  https://doi.org/10.1016/j.ejmech.2022.114620
- 38319473  https://doi.org/10.1007/s11427-023-2459-8
- 38171234  https://doi.org/10.1016/j.bbrc.2023.149393
- 21885291  https://doi.org/10.1016/j.str.2011.06.014
- 29311713  https://doi.org/10.1038/s41598-017-18570-w

chrm2:
- 30420692  https://doi.org/10.1038/s41589-018-0152-y
- 36690613  https://doi.org/10.1038/s41467-022-35726-z
- 24256733  https://doi.org/10.1038/nature12735
- 22278061  https://doi.org/10.1038/nature10753

gr_nr3c1:
- 36747092  https://doi.org/10.1038/s41594-022-00914-4
- 18952422  https://doi.org/10.1016/j.bmcl.2008.10.021
- 28937774  https://doi.org/10.1021/acs.jmedchem.7b01215
- 38516584  https://doi.org/10.1039/d3md00540b
- 29424542  https://doi.org/10.1021/acs.jmedchem.7b01690
- 26602186  https://doi.org/10.1016/j.str.2015.09.012
- 18160712  https://doi.org/10.1128/MCB.01541-07
- 28043796  https://doi.org/10.1016/j.bmcl.2016.12.047
- 30091920  https://doi.org/10.1021/acs.jmedchem.8b00743
- 19822747  https://doi.org/10.1073/pnas.0909125106
- 24446728  https://doi.org/10.1021/jm401616g
- 24755427  https://doi.org/10.1016/j.bmcl.2014.03.070
- 36484727  https://doi.org/10.1021/acs.jmedchem.2c01635
- 27810243  https://doi.org/10.1016/j.bmcl.2016.10.052
- (29M / PDB 4MDD — no PMID/DOI in worklist; antagonist per structure title)

nav1_7:
- 35476982  https://doi.org/10.1016/j.celrep.2022.110735
- 37270609  https://doi.org/10.1038/s41467-023-38942-3
- 26680203  https://doi.org/10.1126/science.aac5464
- 36975198  https://doi.org/10.7554/eLife.84151
