---
name: hostile
description: >-
  Remove host reads from paired short-read or long-read FASTQ with Hostile using Bowtie2 or minimap2 and standard, masked, or custom indexes. Use when auditable host depletion, JSON removal statistics, and microbial-retention-aware reference choice are needed.
license: MIT
compatibility: Requires Hostile 2.0.2, Bowtie2/minimap2, FASTQ input, and a downloaded or custom host index.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "hostile,host-depletion,human-reads,bowtie2,minimap2,privacy"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.0.2"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# Hostile

Hostile wraps Bowtie2 for paired/short reads and minimap2 for long reads, emitting cleaned FASTQ plus structured removal statistics.

## Reference decision

The default human index is `human-t2t-hla`. Masked standard indexes can reduce inadvertent removal of microbial sequences, but masking defines a trade-off between host sensitivity and microbial retention. For non-human studies, provide an appropriate custom genome/index.

```bash
hostile --version
hostile index list
# Optional reproducible prefetch rather than download during a batch job:
hostile index fetch --name human-t2t-hla-argos985 --bowtie2
```

Record the exact index name/release or custom-reference checksum. Host depletion is also a privacy control; access to raw reads must follow governance requirements.

## Paired short reads

```bash
set -euo pipefail
r1=${1:?usage: hostile-pe.sh R1.fastq.gz R2.fastq.gz output_dir}
r2=${2:?usage: hostile-pe.sh R1.fastq.gz R2.fastq.gz output_dir}
out=${3:?usage: hostile-pe.sh R1.fastq.gz R2.fastq.gz output_dir}
[[ -s "$r1" && -s "$r2" ]] || exit 2
mkdir -p "$out"
hostile clean --fastq1 "$r1" --fastq2 "$r2" --aligner bowtie2 \
  --index human-t2t-hla-argos985 --threads 16 --output "$out" \
  >"$out/hostile.json" 2>"$out/hostile.stderr.log"
python3 - "$out/hostile.json" <<'PY'
import json, sys
x=json.load(open(sys.argv[1]))
assert isinstance(x, list) and x, "missing Hostile JSON record"
for r in x:
    assert r["reads_in"] >= r["reads_out"] >= 0
    assert r["reads_removed"] == r["reads_in"] - r["reads_out"]
print(x)
PY
find "$out" -name '*.clean.fastq.gz' -size +0c -print | grep -q .
```

For a long-read FASTQ, pass only `--fastq1`; auto mode selects minimap2, or set `--aligner minimap2`. Use `--airplane`/offline mode after prefetching indexes on isolated compute.

## Validate

- compare input/output read pairs and ensure mates remain synchronized;
- inspect JSON `reads_in`, `reads_out`, `reads_removed`, proportion, aligner, index, and options;
- classify or align a sample of removed reads to assess microbial false removal;
- investigate unexpectedly high/low removal by checking reference, mode, read type, and input pairing;
- retain logs and cleaned-file checksums.

`--invert` keeps host-aligning reads and is diagnostic, not a decontaminated output. Do not expose inverted human reads in ordinary analysis storage.

## Failure recovery

An interrupted minimap2 index build can leave a corrupt `.mmi`; upstream recommends deleting the generated MMI or using the index-delete command before rebuilding. Do not use `--force` until partial outputs are archived or removed deliberately.

## Analytical thinking

No alignment threshold simultaneously guarantees all host reads are removed and all microbial reads retained. Report the observed removed fraction, reference, aligner, options, and residual-screening method; “host depleted” is not proof of zero host DNA.

## Source

- https://github.com/bede/hostile
