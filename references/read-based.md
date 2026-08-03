# Module C — Read-based taxonomic and functional profiling

Use when primary deliverables are **sample-level composition or pathway tables
from reads**, not MAG assemblies.

## Profiler selection

| Analytical question | Preferred method | Rationale |
|---|---|---|
| Clade or species profiles from conserved markers | MetaPhlAn4 | Marker-based specificity on host-depleted paired-end data |
| Gene-family and pathway abundances | HUMAnN4 | Joint taxonomic and functional inference on merged pairs |
| Broad k-mer classification or custom databases | Kraken2 with Bracken | Throughput; performance is database-limited |
| Group-wise biomarker discovery | LEfSe, MaAsLin2, or STAMP | Requires defined metadata contrasts |

Do not merge MetaPhlAn and Kraken abundances into one unlabeled table.

## Recommended sequence

1. Complete Module B preprocessing.
2. Prepare merged paired-end input for HUMAnN when required.
3. Run HUMAnN4; export and curate MetaPhlAn taxonomic tables.
4. Optionally generate clade visualizations and LEfSe contrasts.
5. Optionally run Kraken2 classification and Bracken re-estimation.
6. Proceed to Module G for comparative figures.

## Interpretive limits

- Relative abundance is not absolute load without calibration or spike-ins.
- HUMAnN pathway detection is homology-supported potential, not measured flux.
- Bracken redistributes Kraken assignments under model assumptions; rare taxa
  remain uncertain.
- Inspect batch effects before biological group testing.

## Next modules

- Gene catalogues and CAZy/CARD on assembled ORFs → Module D.
- Genome recovery → Module E (classical) or Module F (BASALT).
