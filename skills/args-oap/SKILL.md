---
name: args-oap
description: >-
  Profile and quantify antibiotic-resistance genes in environmental metagenomic reads
  with ARGs-OAP and the structured SARG database. Use for type/subtype/gene tables,
  cell- or 16S-normalized profiles, optional metadata-based absolute estimates, and
  auditable paired-read handling without presenting normalization as measured phenotype.
license: MIT
compatibility: Requires ARGs-OAP 4.0.0, DIAMOND, BWA, BLAST, samtools, its SARG assets, and consistently named paired FASTA/FASTQ-derived inputs.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ARGs-OAP,SARG,resistome,environmental,quantification,AMR"
  metagenomics.upstream: "https://github.com/xinehc/args_oap"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "4.0.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/output contract reviewed against upstream; not executed here"
---

# ARGs-OAP

ARGs-OAP maps reads through the SARG hierarchy and reports ARG type, subtype, and gene
profiles under several denominators. It is complementary to assembly/protein callers such
as RGI and AMRFinderPlus.

## Input contract

- quality- and host-filtered prokaryotic reads in one input directory;
- paired files named with supported `_1/_2`, `_R1/_R2`, or `_fwd/_rev` suffixes;
- unique sample IDs and a manifest that records every mate pair;
- pinned ARGs-OAP/SARG release and dependency versions;
- a predeclared denominator and filtering policy.

ARGs-OAP’s cell and 16S estimates depend on marker detection and community composition.
Host/fungal contamination can bias those estimates.

## Run two stages

```bash
set -euo pipefail
input=${1:?usage: run-args-oap.sh input_dir output_dir}
out=${2:?usage: run-args-oap.sh input_dir output_dir}
logdir=${LOGDIR:-${out}.logs}
[[ -d "$input" ]] || exit 2
[[ ! -e "$out" && ! -e "$logdir" ]] || {
  echo "use new output and log directories: $out ; $logdir" >&2; exit 2;
}
mkdir -p "$(dirname "$out")" "$logdir"
absolute_args=(-m "$logdir/absolute-quantification.disabled")
if [[ -n ${ABSOLUTE_METADATA:-} ]]; then
  [[ -s "$ABSOLUTE_METADATA" ]] || exit 2
  absolute_args=(-m "$ABSOLUTE_METADATA")
fi
args_oap --version >"$logdir/args-oap.version.txt" 2>&1
args_oap stage_one -i "$input" -o "$out" -f fq -t 16 \
  "${absolute_args[@]}" \
  >"$logdir/args-oap.stage-one.stdout.log" 2>"$logdir/args-oap.stage-one.stderr.log"
args_oap stage_two -i "$out" -t 16 \
  >"$logdir/args-oap.stage-two.stdout.log" 2>"$logdir/args-oap.stage-two.stderr.log"
[[ -s "$out/metadata.txt" && -s "$out/blastout.filtered.txt" ]] || exit 3
find "$out" -maxdepth 1 -type f -name '*normalized*' -size +0c -print -quit | grep -q .
```

Set `-f` to the actual upstream-supported input format. Do not rename one mate without the
other. For a custom database, build it with `args_oap make_db` and provide the matching
hierarchical structure to both stages.

## Optional absolute estimates

Version 4.0 accepts a metadata table containing positive sample volume, elution volume,
and DNA concentration values and emits `absolute_quantification.*.txt`; set
`ABSOLUTE_METADATA` to enable it. Otherwise the command uses a deliberately nonexistent
sentinel instead of the CLI's ambient `input/meta.txt` default. These are
model-based estimates without spike-ins or qPCR. Label them accordingly and sensitivity-
test extraction yield and marker assumptions; use `$absolute-abundance` for externally
calibrated designs.

## Validation

- compare the discovered sample list and `nRead` with the input manifest;
- verify both mates were assigned to one sample and no file was silently skipped;
- inspect `n16S`, `nCell`, zero/NA samples, extracted ARG-like sequences, and filtered hits;
- ensure type/subtype/gene matrices have identical sample columns and finite values;
- keep raw hit counts, normalized tables, and no-hit samples;
- compare selected determinants with assembly-based curated calls where possible.

## Recovery and provenance

Stage two may be rerun only when stage-one outputs, database, and parameters are unchanged;
otherwise start a new directory. Record ARGs-OAP, DIAMOND/BWA/BLAST/samtools versions,
SARG release/checksum, all commands, input checksums, pairing audit, denominator, metadata,
and any custom hierarchy.

## Interpretation

Normalized ARG copies or hits are computational abundance estimates, not gene expression,
cellular phenotype, host, or mobility. Use `$arg-mge-host-linkage` on coordinate-bearing
assembly evidence for ARG–MGE–host claims.

## Sources

- https://github.com/xinehc/args_oap
- https://doi.org/10.1093/bioinformatics/bty053

## Related skills

`resistome-analysis` · `rgi` · `amrfinderplus` · `deeparg` ·
`absolute-abundance` · `arg-mge-host-linkage`
