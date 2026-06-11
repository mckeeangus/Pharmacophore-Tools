"""Apply curation (exclusions / cofactor keep / metal flagging) across a
target's structure hits and summarise what was kept vs dropped.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from . import exclusions
from .exclusions import LigandDecision
from .rcsb import LigandInstance, StructureHit


@dataclass
class CurationResult:
    decisions: dict[str, LigandDecision] = field(default_factory=dict)
    kept_instances: list[LigandInstance] = field(default_factory=list)
    # instance counts (how many bound copies across all structures)
    instance_counts: Counter = field(default_factory=Counter)
    # structure counts (in how many distinct PDB entries a HET appears)
    structure_counts: dict[str, set[str]] = field(default_factory=dict)

    def kept_het_codes(self) -> list[str]:
        return sorted({i.comp_id for i in self.kept_instances})

    def excluded_het_codes(self) -> list[str]:
        return sorted(c for c, d in self.decisions.items() if not d.keep)

    def flagged_het_codes(self) -> list[str]:
        return sorted(c for c, d in self.decisions.items() if d.flagged)

    def n_structures_for(self, comp_id: str) -> int:
        return len(self.structure_counts.get(comp_id, set()))


def curate_structures(hits: list[StructureHit],
                      keep_extra: list[str] | None = None,
                      exclude_extra: list[str] | None = None) -> CurationResult:
    res = CurationResult()
    keep_extra_set = set(keep_extra or [])
    exclude_extra_set = set(exclude_extra or [])

    for hit in hits:
        for inst in hit.instances:
            cid = inst.comp_id.upper()
            decision = res.decisions.get(cid)
            if decision is None:
                decision = exclusions.classify(cid, exclude_extra_set, keep_extra_set)
                res.decisions[cid] = decision
            if decision.keep:
                res.kept_instances.append(inst)
                res.instance_counts[cid] += 1
                res.structure_counts.setdefault(cid, set()).add(hit.pdb_id)
    return res
