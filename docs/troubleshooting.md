# Troubleshooting

## Skills not loading

1. Confirm `<skills-root>/<name>/SKILL.md` exists and is readable.
2. Print the authoritative targets:
   `python3 scripts/install-skills.py --list-platforms`.
3. Preview the exact install:
   `python3 scripts/install-skills.py --dry-run --user --profile routing <platform>`.
4. If links are present but ignored, retry into a temporary target with
   `--mode copy`; some sandboxes do not follow external symlinks.
5. Start a new agent session or refresh its Skills cache/panel.
6. Check for a same-name project skill shadowing the user skill.
7. Run `python3 scripts/validate-skills.py` in the source checkout.

Platform checks:

| Client | Check |
|--------|-------|
| Kimi Code | `kimi --skills-dir /absolute/path/to/skills` isolates discovery problems |
| ZCode | Inspect `~/.zcode/skills` and `.agents/skills`; plugin users must install/enable the marketplace entry |
| Qwen Code | Inspect `~/.qwen/skills` or `.qwen/skills`, restart, then open `/skills` |
| Codex | Run `codex plugin list`; for direct installs inspect `~/.agents/skills` / `.agents/skills` |
| Claude Code | Reinstall/update the marketplace plugin or inspect `.claude/skills` |

A smaller profile can also prevent metadata-budget truncation: install
`routing` or `core` into a clean target instead of all 226 skills.

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

## Binning / BASALT / QC

| Symptom | Action |
|---------|--------|
| BASALT resume fails | Unchanged provenance; one CWD per run |
| Missing `BASALT_WEIGHT` | 5 ensemble CSVs + checksum |
| DAS Tool truncated help | CLI typo (docopt); verify `-i/-c/-o` |
| MetaWRAP refine empty | Check `-c/-x` vs CheckM tables; input bin dirs |
| Many high-contamination bins | Prefer multi-coverage binning; try `deepurify` then re-run CheckM2/GUNC |
| Interactive refine needed | `anvio` — still re-QC after export |

## Databases / versions

| Symptom | Action |
|---------|--------|
| MetaPhlAn vs HUMAnN disagree wildly | ChocoPhlAn / UniRef releases out of sync — pin both |
| GTDB-Tk weird placements | Wrong `GTDBTK_DATA_PATH` release vs cited GTDB |
| Kraken+Bracken empty / nonsense | Bracken DB not built from **same** Kraken DB; check `-r` read length |
| eggNOG / CARD / CheckV path errors | Absolute pinned paths; re-download matching software major version |

## Taxonomy mixing

| Symptom | Action |
|---------|--------|
| “Species X confirmed by all methods” | Methods report different abundance types — do not merge unlabeled |
| Sequence vs taxonomic abundance confusion | DNA-to-DNA (Kraken) ≠ marker taxonomic abundance (MetaPhlAn/mOTUs) |
| Environmental “empty” community | Try `singlem` — many lineages lack genomes in other DBs |

Never merge MetaPhlAn, SingleM, Kraken/Bracken, and GTDB labels into one
unlabeled table.

## Annotation / mining

| Symptom | Action |
|---------|--------|
| antiSMASH DB missing | `download-antismash-databases` |
| geNomad / CheckV DB path | Absolute pinned paths |
| Viral “complete genomes” without CheckV | Run `checkv` before `vcontact` or publication |
| DRAM annotate fails | Finish DRAM DB config; validate FASTA headers |
| RGI no hits | CARD version loaded? Protein vs contig mode |
| gapseq hollow models | MAG completeness too low — filter with `mag-qc` first |
