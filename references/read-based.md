# Read-based taxonomic and functional profiling

Apply this module when the primary deliverables are **sample-level composition or
pathway abundance tables derived from reads**, rather than MAG assemblies.
Parameter defaults follow EasyMetagenome ([easymetagenome.md](easymetagenome.md)).

## Profiler selection

| Analytical question | Preferred method | Rationale |
|---|---|---|
| Clade or species profiles from conserved markers | MetaPhlAn4 | Marker-based specificity on host-depleted paired-end data |
| Gene-family and pathway abundances | HUMAnN4 | Joint taxonomic and functional inference on merged pairs |
| Broad k-mer classification or custom reference databases | Kraken2 with Bracken | Throughput; sensitivity and specificity are database-limited |
| Group-wise biomarker discovery | LEfSe, MaAsLin2, or STAMP | Requires defined metadata contrasts and transparent multiple-testing practice |

Do not merge MetaPhlAn and Kraken abundances into a single unlabeled table.

## Recommended sequence

1. Complete quality control and host depletion (`temp/hr/${id}_1.fastq`, `_2.fastq`).
2. Prepare merged paired-end input for HUMAnN as required by the pipeline.
3. Run HUMAnN4; export and curate MetaPhlAn taxonomic tables.
4. Optionally generate GraPhlAn visualizations and LEfSe contrasts on declared groups.
5. Optionally run Kraken2 classification followed by Bracken re-estimation.
6. Produce figures through EasyMetagenome statistical plotting scripts.

## Interpretive limits

- Relative abundance is not absolute microbial load absent calibration or spike-ins.
- HUMAnN pathway detection reflects homology-supported potential, not measured flux.
- Bracken redistributes Kraken assignments under model assumptions; rare taxa remain uncertain.
- Inspect ordinations for batch structure before biological group testing in
  multi-centre designs.

## Subsequent modules

- Assembled gene catalogues and CAZy/CARD annotation → EasyMetagenome assembly branch.
- Genome recovery → MetaWRAP (EasyMetagenome) or BASALT (PKU-EMBL refinement).
