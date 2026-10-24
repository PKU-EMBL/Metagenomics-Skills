---
name: racon
description: >
  Ultrafast consensus polishing of assemblies using mapped long (or short) reads. Use
  after long-read or hybrid assembly before binning/annotation.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "polish, assembly, long-read"
  metagenomics.upstream: "https://github.com/lbcb-sci/racon"
  metagenomics.stage: "assembly"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "minimap2-to-Racon CLI contract statically reviewed; not executed here"
---

# Racon

Upstream: [lbcb-sci/racon](https://github.com/lbcb-sci/racon)

## Citation

Vaser, R., Sović, I., Nagarajan, N. & Šikić, M. Fast and accurate de novo
genome assembly from long uncorrected reads. *Genome Res.* **27**, 737–746
(2017). https://doi.org/10.1101/gr.214270.116

## Analytical thinking

Racon polishes contigs given **overlaps from mapping** (usually Minimap2 PAF).
Typical long-read loop: assemble → map reads → racon → (optional repeat). Do
not expect Racon alone to fix massive mis-assemblies; it refines consensus.

For Illumina polishing of long-read drafts, consider `pilon` / Polypolish
ecosystems as alternatives.

## How to run

Use the preset matching the reads used as polishing evidence and write each round
to a new directory.

```bash
set -Eeuo pipefail
reads="${1:?usage: racon-round.sh READS DRAFT_FASTA OUTPUT_DIR}"
draft="${2:?usage: racon-round.sh READS DRAFT_FASTA OUTPUT_DIR}"
out="${3:?usage: racon-round.sh READS DRAFT_FASTA OUTPUT_DIR}"
threads="${THREADS:-16}"
preset="${MINIMAP_PRESET:-map-ont}"
for input in "$reads" "$draft"; do test -s "$input" || exit 2; done
[[ "$threads" =~ ^[1-9][0-9]*$ ]] || exit 2
case "$preset" in map-ont|map-pb|map-hifi) ;; *) exit 2 ;; esac
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

minimap2 -x "$preset" -t "$threads" "$draft" "$reads" \
  >"$out/read-to-draft.paf" 2>"$out/minimap2.stderr.log"
test -s "$out/read-to-draft.paf"
racon -t "$threads" "$reads" "$out/read-to-draft.paf" "$draft" \
  >"$out/polished.tmp.fa" 2>"$out/racon.stderr.log"
test -s "$out/polished.tmp.fa"
mv "$out/polished.tmp.fa" "$out/assembly.racon.fa"
```

## Validation, recovery, and provenance

Compare pre/post-polish assembly statistics, read alignment identity/coverage,
consensus QV when truth or k-mer evidence is available, and `$quast` metrics. A
larger assembly or another Racon round is not automatically better; stop when
independent quality evidence plateaus or worsens. Never overwrite the draft.

Archive the PAF, logs, input and polished checksums, Minimap2/Racon versions,
preset, round number, command, and validation table. A failed or parameter-changed
round should use a fresh directory so partial stdout is never mistaken for a
finished FASTA.

## Related skills

`minimap2` · `metaflye` · `metamdbg` · `pilon` · `quast`
