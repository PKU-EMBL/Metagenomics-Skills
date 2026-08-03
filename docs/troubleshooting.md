# Troubleshooting

## Skills not loading

1. Confirm `skills/<name>/SKILL.md` exists
2. Re-run `./scripts/install-platforms.sh` for your platform
3. Restart the agent session
4. For Claude, reinstall the marketplace plugin

## Missing bioinformatics binaries

Skills describe workflows; they do not install Conda packages automatically.
Use the `setup` skill and verify with `command -v`.

## QC / PE pairing

| Symptom | Action |
|---------|--------|
| PE count mismatch downstream | KneadData `--reorder`; compare headers |
| Almost all reads removed as host | Wrong host index or host-dominated library |
| fastp JSON missing | Always keep `-j/-h` reports |

## Mapping

| Symptom | Action |
|---------|--------|
| ~0% reads mapped | Contigs/reads mismatch; wrong sample |
| MetaBAT empty bins | Contig IDs in depth ≠ FASTA headers |
| Unsorted BAM errors | `aligner \| samtools sort` + `index` |
| Bowtie2 vs bwa-mem2 index errors | Indexes are **not** interchangeable; also ≠ strobealign cache |

## Assembly / polish

| Symptom | Action |
|---------|--------|
| metaSPAdes OOM | Raise mem node or use MEGAHIT |
| Polish makes things worse on community contigs | Prefer polish on isolate-like MAGs; avoid blind community Pilon |

## Binning / BASALT

| Symptom | Action |
|---------|--------|
| BASALT resume fails | Unchanged provenance; one CWD per run |
| Missing `BASALT_WEIGHT` | 5 ensemble CSVs + checksum |
| DAS Tool truncated help | CLI typo (docopt); verify `-i/-c/-o` |
| MetaWRAP refine empty | Check `-c/-x` vs CheckM tables; input bin dirs |

## Annotation / mining

| Symptom | Action |
|---------|--------|
| antiSMASH DB missing | `download-antismash-databases` |
| geNomad / CheckV DB path | Absolute pinned paths |
| DRAM annotate fails | Finish DRAM DB config; validate FASTA headers |
| RGI no hits | CARD version loaded? Protein vs contig mode |

## Taxonomy mixing

Never merge MetaPhlAn, Kraken/Bracken, and GTDB labels into one unlabeled table.
