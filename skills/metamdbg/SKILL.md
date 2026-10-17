---
name: metamdbg
description: >
  High-quality metagenome assembly from long accurate reads. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "assembly, hifi, long-read"
  metagenomics.upstream: "https://github.com/GaetanBenoitDev/metaMDBG"
  metagenomics.stage: "assembly"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.4"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream 1.4 README; not executed here"
---

# metaMDBG

Upstream: [metaMDBG](https://github.com/GaetanBenoitDev/metaMDBG)

## Citation

Benoit, G. *et al.* High-quality metagenome assembly from long accurate reads with metaMDBG. *Nat. Biotechnol.* **42**, 1378–1383 (2024). https://doi.org/10.1038/s41587-023-01983-6

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Preferred for PacBio HiFi / accurate long-read metagenomes. Pair with long-read-aware binning (SemiBin2/LorBin/BASALT).

## How to run

```bash
set -euo pipefail
reads=${READS:?set READS to non-empty HiFi or ONT R10.4+ FASTQ}
platform=${LONG_READ_PLATFORM:?set hifi or ont}
out=temp/asm/metamdbg
[[ -s "$reads" && ! -e "$out" ]] || exit 2
mkdir -p "$(dirname "$out")"
case "$platform" in
  hifi) input_flag=--in-hifi ;;
  ont) input_flag=--in-ont ;;
  *) echo 'LONG_READ_PLATFORM must be hifi or ont' >&2; exit 2 ;;
esac
metaMDBG asm --out-dir "$out" "$input_flag" "$reads" --threads 32 \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
test -s "$out/contigs.fasta.gz"
gzip -t "$out/contigs.fasta.gz"
```

## Validation and recovery

Record platform/basecaller/chemistry, read checksums and length/quality/yield before and after any filter. Validate gzip/FASTA syntax, contig count/length/coverage, read remapping, assembly graph and `$quast` metrics; compare recovery/duplication of marker genomes rather than optimizing N50 alone.

metaMDBG can resume checkpoints only by resubmitting the identical command after interruption. If reads or result-affecting parameters change, archive the partial directory and start fresh. Record metaMDBG version, exact command, dependencies, logs and output checksums.

## Decision notes

- Stage: **assembly** (long accurate reads)
- Prefer HiFi / accurate long reads; follow with long-read binning (`lorbin` / SemiBin2 LR)
- Pin version; report polish status

## Related skills

metaflye · minimap2 · semibin2 · basalt · `tool-selection` · `metagenomics-workflow`
