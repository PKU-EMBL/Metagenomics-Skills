---
name: metaflye
description: >
  Long-read metagenome assembly with Flye/metaFlye. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "assembly, long-read"
  metagenomics.upstream: "https://github.com/fenderglass/Flye"
  metagenomics.stage: "assembly"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "Flye meta-mode CLI template statically reviewed; not executed here"
---

# metaFlye

Upstream: [metaFlye](https://github.com/fenderglass/Flye)

## Citation

Kolmogorov, M. *et al.* metaFlye: scalable long-read metagenome assembly using repeat graphs. *Nat. Methods* **17**, 1103–1110 (2020). https://doi.org/10.1038/s41592-020-00971-x

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Primary long-read metagenome assembler for noisy ONT/PacBio CLR. For HiFi prefer metaMDBG/hifiasm-meta. Still map reads back for binning.

## How to run

Choose the read-mode flag from basecaller/chemistry metadata, not from filename.

```bash
set -Eeuo pipefail
reads="${1:?usage: assemble-lr.sh READS.fastq.gz OUTPUT_DIR}"
out="${2:?usage: assemble-lr.sh READS.fastq.gz OUTPUT_DIR}"
threads="${THREADS:-32}"
read_mode="${READ_MODE:---nano-hq}"
test -s "$reads" || exit 2
[[ "$threads" =~ ^[1-9][0-9]*$ ]] || exit 2
case "$read_mode" in
  --nano-raw|--nano-hq|--pacbio-raw|--pacbio-hifi) ;;
  *) echo "unsupported READ_MODE: $read_mode" >&2; exit 2 ;;
esac
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$(dirname "$out")" logs

flye --meta "$read_mode" "$reads" --out-dir "$out" --threads "$threads" \
  >"logs/$(basename "$out").flye.stdout.log" \
  2>"logs/$(basename "$out").flye.stderr.log"
```

Do not pool technologies or samples unless the assembly design explicitly calls
for it. HiFi may also justify `metamdbg`; pilot when assembler choice affects the
biological endpoint.

## Key parameters

| `--meta` | metagenome mode | Required |
| read type flag | match chemistry | |

## Decision notes

- Stage: **assembly** (long-read metagenomes)
- Prefer ONT/PacBio community assemblies; polish when chemistry requires
- Downstream: long-read-aware binning (`lorbin`, SemiBin2 LR)

## Validation, recovery, and provenance

```bash
test -s "$out/assembly.fasta"
test -s "$out/assembly_info.txt"
test -s "$out/flye.log"
seqkit stats -T "$out/assembly.fasta"
```

Inspect Flye warnings, repeat/graph summaries, total span, contig-length
spectrum, read recruitment, and `$quast` results; contiguity alone does not prove
correctness. Resume only an unchanged run with Flye's documented resume behavior;
otherwise retain the partial directory and start under a new path. Record Flye
version, read-mode flag, input checksum, command, resource use, logs, and assembly
checksum.

## Related skills

`minimap2` · `metamdbg` · `megahit` · `metaspades` · `quast` ·
`tool-selection` · `metagenomics-workflow`
