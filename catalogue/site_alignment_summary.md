# Site-alignment summary

Ligands kept only if their pose superposes into the reference site (binding-site-local fit) and the centroid lands within cutoff of the anchor. Dropped categories: `off_site` (wrong location), `poor_fit` / `no_pocket` (no matching pocket, e.g. wrong protein/allosteric), `not_found` (instance/structure unavailable).

| Target | Ref | Anchor kept | Candidates | Dropped breakdown |
|--------|-----|------------:|-----------:|-------------------|
| cavab | 6KE5 | 6 | 110 | {'off_site': 104} |
| cox2 | 5KIR | 12 | 36 | {'off_site': 24} |
| hmgcr | 1HWK | 85 | 125 | {'off_site': 40} |
| net_slc6a2 | 8ZOY | 57 | 99 | {'off_site': 42} |
