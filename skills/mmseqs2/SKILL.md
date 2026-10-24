---
name: mmseqs2
description: >
  MMseqs2 — ultra-fast protein sequence search, clustering (Linclust), and contig
  taxonomy (Steinegger / Söding labs). Use when: (1) Building NR gene catalogues, (2)
  Sensitive BLASTP-scale search at metagenome size, (3) Contig taxonomy via
  easy-taxonomy / taxDB, (4) Contrasting with Foldseek structure search. For
  structure/motif search use foldseek / folddisco; route AI stack via metagenomics-llm.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MMseqs2, cluster, search, taxonomy, Linclust"
  metagenomics.upstream: "https://github.com/soedinglab/MMseqs2"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "easy-cluster/search/taxonomy command shapes statically reviewed; not executed here"
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

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

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

Choose one mode per immutable output root. This example creates a non-redundant
protein catalogue; search and taxonomy require separate result directories and
release-pinned target databases.

```bash
set -Eeuo pipefail
proteins="${1:?usage: cluster-mmseqs.sh PROTEINS_FAA OUTPUT_DIR}"
out="${2:?usage: cluster-mmseqs.sh PROTEINS_FAA OUTPUT_DIR}"
threads="${THREADS:-16}"
test -s "$proteins" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out/tmp"

mmseqs easy-cluster "$proteins" "$out/nr" "$out/tmp" \
  --min-seq-id 0.90 -c 0.80 --cov-mode 1 --threads "$threads" \
  >"$out/mmseqs.stdout.log" 2>"$out/mmseqs.stderr.log"
test -s "$out/nr_rep_seq.fasta"
test -s "$out/nr_cluster.tsv"
```

Protein search uses `mmseqs easy-search QUERY TARGET RESULT TMP`; contig taxonomy
uses `easy-taxonomy` with a taxonomy-aware database. Preserve their full output
fields and database build manifests.

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

## Validation, recovery, and provenance

For clustering, verify input-to-cluster completeness, unique representative IDs,
sequence counts, identity/coverage semantics, and cluster-size distribution. For
search/taxonomy, validate output fields, query coverage, E-values, taxonomic
ranks, and no-hit records. Keep raw mappings before best-hit or LCA filtering.

Use a new result and temporary directory after changing inputs, thresholds,
database, or release. Record MMseqs2 version/commit, target/taxonomy database
release and checksum, input checksum, sensitivity and coverage settings,
commands, logs, cluster/search tables, and result checksums. Similarity and LCA
assignments are not experimental functions or read abundance.

## Related skills

`foldseek` · `folddisco` · `cd-hit` · `diamond` · `eggnog-mapper` · `prodigal` ·
`kraken2` · `metabuli` · `metagenomics-llm` · `tool-selection`
