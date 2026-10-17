---
name: votu-workflow
description: >-
  Build a non-redundant viral operational taxonomic unit catalogue from quality-gated viral genomes using all-versus-all nucleotide similarity, explicit ANI/aligned-fraction thresholds, deterministic representatives, and membership validation. Use when clustering viral contigs into species-level vOTUs for abundance or comparative viromics.
license: MIT
compatibility: Requires BLAST+, CheckV anicalc/aniclust, Python 3, and POSIX shell.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "votu,viral-dereplication,ani,miuvig,checkv,blastn"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "CheckV 1.0.x utilities"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "commands reviewed against CheckV upstream; not executed here"
---

# vOTU workflow

This workflow implements a common species-rank operational rule: at least 95% nucleotide identity over at least 85% of the shorter/target sequence. State the exact rule in Methods.

## Input contract

Use nucleotide viral genomes after caller reconciliation and CheckV quality filtering. IDs must be unique and free of spaces; sequences should represent viral regions rather than untrimmed host-plus-provirus contigs.

```bash
set -euo pipefail
fna=${1:?usage: votu.sh viral_quality_gated.fna output_dir}
out=${2:?usage: votu.sh viral_quality_gated.fna output_dir}
[[ -s "$fna" ]] || { echo "missing FASTA: $fna" >&2; exit 2; }
mkdir -p "$out"
python3 - "$fna" <<'PY'
import sys
ids=[]
for line in open(sys.argv[1]):
    if line.startswith(">"):
        x=line[1:].strip().split()[0]; ids.append(x)
assert ids, "no FASTA records"
assert len(ids)==len(set(ids)), "duplicate FASTA IDs"
assert all(" " not in x and "\t" not in x for x in ids)
print(f"sequences={len(ids)}")
PY
```

## Cluster with CheckV utilities

```bash
makeblastdb -in "$fna" -dbtype nucl -out "$out/viral_db" \
  >"$out/makeblastdb.log" 2>&1
blastn -query "$fna" -db "$out/viral_db" -out "$out/all_vs_all.tsv" \
  -outfmt '6 std qlen slen' -max_target_seqs 10000 -num_threads 16 \
  >"$out/blast.stdout.log" 2>"$out/blast.stderr.log"
anicalc -i "$out/all_vs_all.tsv" -o "$out/ani.tsv"
aniclust --fna "$fna" --ani "$out/ani.tsv" --out "$out/votu_clusters.tsv" \
  --min_ani 95 --min_tcov 85 --min_qcov 0
```

CheckV installations may expose commands as `anicalc.py` and `aniclust.py`; inspect `--help` and record the invoked executable. Do not mix outputs from incompatible utility versions.

## Deterministic representatives

Select one representative per cluster by a declared hierarchy, for example:

1. complete/high-quality CheckV category;
2. greater estimated completeness;
3. lower contamination;
4. longer sequence;
5. lexical sequence ID as final tie-break.

Do not select representatives by arbitrary input order. Emit both membership and representative-selection evidence.

## Validation

```bash
[[ -s "$out/ani.tsv" && -s "$out/votu_clusters.tsv" ]] || exit 3
python3 - "$fna" "$out/votu_clusters.tsv" <<'PY'
import sys, csv
ids={x[1:].split()[0] for x in open(sys.argv[1]) if x.startswith(">")}
rows=list(csv.reader(open(sys.argv[2]), delimiter="\t"))
assert rows, "empty cluster table"
text="\n".join("\t".join(r) for r in rows)
missing=[x for x in ids if x not in text]
assert not missing, f"unrepresented sequences (first 10): {missing[:10]}"
print(f"input_sequences={len(ids)} cluster_rows={len(rows)}")
PY
```

Also inspect cluster-size distribution, singleton fraction, and representative quality. Re-run a sensitivity analysis if changing minimum length, quality gate, ANI, or coverage materially changes ecological conclusions.

## Failure recovery

BLAST output scales quadratically. For large catalogues, partition safely or use a validated scalable ANI implementation while preserving the same identity and coverage semantics. Resume only from complete, non-empty files; use fresh output directories when changing thresholds.

## Analytical thinking

A vOTU is an operational sequence cluster, not an ICTV taxonomic assignment and not necessarily a biological species. Fragmentation can split populations, while shared conserved regions can create misleading local matches; the aligned-fraction criterion is essential.

## Source

- CheckV clustering protocol: https://bitbucket.org/berkeleylab/checkv/src/master/README.md
