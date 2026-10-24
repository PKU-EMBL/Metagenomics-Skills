---
name: foldseek
description: >
  Foldseek — ultrafast protein structure search and clustering via the 3Di structural
  alphabet (Steinegger / Söding labs). Use when: (1) Searching MAG or predicted
  structures against AFDB/PDB/ESM Atlas, (2) Foldseek-Multimer complex search for
  distant systems (e.g. CRISPR–Cas), (3) Structure clustering at AFDB scale, (4)
  Sequence→structure search with ProstT5. Route via homology-search / metagenomics-llm;
  pairs with mmseqs2 (sequence) and folddisco (motifs).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Foldseek, 3Di, structure-search, AFDB, multimer, ProstT5, homology"
  metagenomics.upstream: "https://github.com/steineggerlab/foldseek"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "easy-search/ProstT5/multimer interfaces checked against current upstream README; not executed here"
---

# Foldseek

Upstream: [steineggerlab/foldseek](https://github.com/steineggerlab/foldseek) ·
Web: https://search.foldseek.com

## Citation

van Kempen, M. *et al.* Fast and accurate protein structure search with Foldseek.
*Nat. Biotechnol.* **42**, 243–246 (2024). https://doi.org/10.1038/s41587-023-01773-0

Kim, W. *et al.* Rapid and sensitive protein complex alignment with
Foldseek-Multimer. *Nat. Methods* **22**, 469–472 (2025).
https://doi.org/10.1038/s41592-025-02593-7

Barrio-Hernandez, I. *et al.* Clustering predicted structures at the scale of
the known protein universe. *Nature* **622**, 637–645 (2023).
https://doi.org/10.1038/s41586-023-06510-w

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Sequence search (`mmseqs2` / `diamond`) fails for many remote homologs. Foldseek
turns tertiary geometry into a **3Di** letter sequence and reuses MMseqs2-style
prefilters — roughly **10⁴–10⁵×** faster than TM-align/Dali/CE with comparable
sensitivity. Metagenomics use cases: AFDB/ESMAtlas annotation of dark MAG
proteins, structural NR clustering, and complex-level mining
(`easy-multimersearch`).

Martin Steinegger “AI and evolution” stack (conservation level → tool):

| Level | Prefer |
|-------|--------|
| Sequence / single-chain structure | `mmseqs2` · `foldseek` |
| Multimer / interface | Foldseek-Multimer (`easy-multimersearch`) |
| Local structural motif | `folddisco` |
| Conserved gene neighborhoods | `spacedust` (uses Foldseek) |

| vs | Prefer Foldseek when |
|----|----------------------|
| `mmseqs2` / `diamond` | Structures or ProstT5 path available; twilight-zone homology |
| `plmsearch` / `deepblast` | Real/predicted structures exist (or AFDB targets) |
| `folddisco` | Need whole-chain / complex fold match, not a short motif |
| TM-align / US-align | Database-scale search (not gold-standard pairwise polish) |

Hard rules:

1. Structural hits ≠ experimental function — pin AFDB/PDB release + Foldseek version
2. Low-confidence AF models (pLDDT) inflate false positives — filter inputs
3. Multimer claims need chain pairing / complex TM reporting, not monomer E-values alone
4. Do not merge Foldseek tables with BLAST/MMseqs unlabeled

## How to run

This monomer template searches structures against an already pinned Foldseek
target database and exports interpretable structural fields.

```bash
set -Eeuo pipefail
query="${1:?usage: search-foldseek.sh QUERY_STRUCTURE_OR_DIR TARGET_DB OUTPUT_DIR}"
target="${2:?usage: search-foldseek.sh QUERY_STRUCTURE_OR_DIR TARGET_DB OUTPUT_DIR}"
out="${3:?usage: search-foldseek.sh QUERY_STRUCTURE_OR_DIR TARGET_DB OUTPUT_DIR}"
threads="${THREADS:-8}"
test -e "$query" && test -e "$target" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out/tmp"
foldseek easy-search "$query" "$target" "$out/hits.tsv" "$out/tmp" \
  --threads "$threads" \
  --format-output 'query,target,evalue,bits,prob,alntmscore,qtmscore,ttmscore,lddt' \
  >"$out/foldseek.stdout.log" 2>"$out/foldseek.stderr.log"
test -f "$out/hits.tsv"
printf 'hits\t%s\n' "$(wc -l <"$out/hits.tsv" | tr -d ' ')" \
  >"$out/validation.tsv"
```

For FASTA queries, add a checksummed ProstT5 model via `--prostt5-model`; TM-score,
LDDT and coordinate-dependent fields are unavailable for 3Di-only databases.
Use `easy-multimersearch` for complexes and preserve its `_report` output.
Download/build databases in a separate frozen setup step.
Webserver: https://search.foldseek.com

## Key parameters

| Setting | Notes |
|---------|-------|
| Input | PDB/mmCIF structures, or FASTA + `--prostt5-model` |
| Target DBs | AFDB proteomes, PDB100, ESMAtlas clusters — pin release |
| `--alignment-type` | 3Di/AA vs TM-align-style rescoring when needed |
| `--cluster-search` | Clustered DBs (AFDB50): reps-only vs expand members |
| `--gpu` | Optional GPU prefilter (Ampere+ preferred) |
| Multimer report | Use `_report` for chain pairing, TM, transforms |

## Decision tree

```text
Homology / structure need?
├─ Close sequence homologs → mmseqs2 / diamond
├─ Dark proteins, have/ predict structures → foldseek easy-search
├─ Sequence-only, no GPU structures → foldseek+ProstT5 or plmsearch / deepblast
├─ Multi-chain complexes / interfaces → foldseek easy-multimersearch
├─ Short active-site / motif geometry → folddisco
├─ Conserved neighborhoods → spacedust
└─ Structure NR catalogue → foldseek easy-cluster
```

## Validation, recovery, and provenance

Reconcile all queries to hits/no-hits and inspect duplicate targets, coverage,
E-value/probability, TM/LDDT metrics, alignment mode, multidomain behavior,
query/target-normalized scores, structure confidence, clustered-DB expansion,
and controls. Visualize and independently check top novel hits; do not transfer
a specific function from global fold alone.

Use fresh output after changing query, database, model, mode, or thresholds.
Record Foldseek version/build/device, database release/build/checksum, structure
source and confidence policy, ProstT5 revision when used, input checksums,
command/logs, native fields, and filters. Keep monomer, multimer, motif and
sequence-only evidence separately labeled.

## Related skills

`homology-search` · `protein-language-model` · `prostt5` · `esm` ·
`foldcomp` · `folddisco` · `foldmason` · `unicore` · `mmseqs2` · `hh-suite` ·
`petasearch` · `spacedust` · `plmsearch` · `deepblast` · `eggnog-mapper` ·
`microbial-mining` · `tool-selection`
