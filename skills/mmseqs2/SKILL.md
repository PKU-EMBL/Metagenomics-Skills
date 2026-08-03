---
name: mmseqs2
description: >
  MMseqs2 — ultra-fast protein sequence search, clustering (Linclust), and
  contig taxonomy (Steinegger / Söding labs). Use when: (1) Building NR gene
  catalogues, (2) Sensitive BLASTP-scale search at metagenome size,
  (3) Contig taxonomy via easy-taxonomy / taxDB, (4) Contrasting with Foldseek
  structure search. Upstream: https://github.com/soedinglab/MMseqs2.
  For structure/motif search use foldseek / folddisco; route AI stack via
  metagenomics-llm.
license: MIT
category: analysis-tools
tags: [MMseqs2, cluster, search, taxonomy, Linclust]
upstream: https://github.com/soedinglab/MMseqs2
stage: function
---

# MMseqs2

Upstream: [MMseqs2](https://github.com/soedinglab/MMseqs2) · https://mmseqs.com

## Citation

Steinegger, M. & Söding, J. MMseqs2 enables sensitive protein sequence searching
for the analysis of massive data sets. *Nat. Biotechnol.* **35**, 1026–1028
(2017). https://doi.org/10.1038/nbt.3988

Mirdita, M. *et al.* Fast and sensitive taxonomic assignment to metagenomic
contigs. *Bioinformatics* **37**, 3029–3031 (2021).
https://doi.org/10.1093/bioinformatics/btab184

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

MMseqs2 is the **sequence** workhorse of the Steinegger stack. Same design
philosophy as Foldseek (k-mer prefilter → ungapped → alignment), but on amino
acids rather than 3Di structure letters.

| Mode | Role in shotgun pipelines |
|------|---------------------------|
| `easy-cluster` / Linclust | NR gene/protein catalogues (vs `cd-hit`) |
| `search` / `easy-search` | Homology annotation at catalogue scale |
| `easy-taxonomy` | Contig taxonomy: extract protein fragments → approx. 2bLCA → weighted vote |

Taxonomy mode covers all domains via fragment extraction (not prokaryote-only
ORF callers). Faster than CAT-style stacks on benchmarks in the 2021 note;
still a **different claim** from `kraken2` / `metabuli` read profilers or
`gtdbtk` MAG taxonomy.

| vs | Prefer MMseqs2 when |
|----|---------------------|
| `cd-hit` | Large catalogues / speed |
| `diamond` | Taxonomy workflows or Linclust-scale clustering |
| `foldseek` | Sequence-only; no structures / ProstT5 |
| `kraken2` | Contig protein→tax labels (not k-mer read profile) |

## How to run

```bash
# NR clustering
mmseqs easy-cluster genes.faa temp/mmseqs/clu temp/mmseqs/tmp \
  --min-seq-id 0.9 -c 0.8 --cov-mode 1

# protein search
mmseqs easy-search query.faa targetDB aln.m8 temp/mmseqs/tmp

# contig taxonomy (prepare taxDB first — see wiki / databases workflow)
mmseqs easy-taxonomy contigs.fa taxonomyDB temp/mmseqs/tax temp/mmseqs/tmp
```

## Key parameters

| Setting | Notes |
|---------|-------|
| `--min-seq-id` / `-c` / `--cov-mode` | Catalogue identity & coverage — declare for NR |
| `-s` | Sensitivity vs speed |
| taxDB | Required for easy-taxonomy; pin nr/UniProt/GTDB build |
| tmp dir | Fast local disk; large catalogues need RAM planning |

## Decision tree

```text
Sequence vs structure homology?
├─ Huge protein NR → mmseqs2 easy-cluster
├─ Classic small NR → cd-hit still fine
├─ Contig taxonomy (protein-based) → mmseqs2 easy-taxonomy
├─ BLASTP-like search → mmseqs2 / diamond
├─ Structure / twilight zone → foldseek (± ProstT5)
├─ Motif geometry → folddisco
└─ PLM remote homology, sequence-only → plmsearch / deepblast
```

## Related skills

`foldseek` · `folddisco` · `cd-hit` · `diamond` · `eggnog-mapper` · `prodigal` ·
`kraken2` · `metabuli` · `metagenomics-llm` · `tool-selection`
