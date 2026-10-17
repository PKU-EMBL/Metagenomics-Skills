---
name: megahit
description: >
  Ultra-fast memory-efficient metagenome assembler. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "assembly, contigs"
  metagenomics.upstream: "https://github.com/voutcn/megahit"
  metagenomics.stage: "assembly"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI contract reviewed; not executed here"
---

# MEGAHIT

Upstream: [voutcn/megahit](https://github.com/voutcn/megahit) (v1.2.9 widely used)

## Citation

Li, D., Liu, C.-M., Luo, R., Sadakane, K. & Lam, T.-W. MEGAHIT: an ultra-fast single-node solution for large and complex metagenomics assembly via succinct de Bruijn graph. *Bioinformatics* **31**, 1674–1676 (2015). https://doi.org/10.1093/bioinformatics/btv033

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

MEGAHIT is the default **fast metagenome assembler** for Illumina PE when memory
or turnaround time dominate. Co-assembly increases shared-genome continuity but
can smear strains—decide with `study-design` first.

Always evaluate assemblies (QUAST) before gene calling or binning. Delete
`intermediate_contigs` after success to save disk.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Dehosted PE | From `kneaddata` |
| RAM | 32 GB small | 128–512 GB co-assemblies |
| CPU | 8 | 32+ |

## How to run

```bash
conda install -c bioconda megahit
megahit --test

megahit -t 32 \
  -1 s1_1.fastq,s2_1.fastq \
  -2 s1_2.fastq,s2_2.fastq \
  -o temp/megahit
```

Single sample: `-1`/`-2` one pair. Output contigs: `temp/megahit/final.contigs.fa`.

## Key parameters

| Parameter | Notes |
|-----------|-------|
| `-t` | Threads |
| `--min-contig-len` | Raise to shrink huge contig sets before binning |
| `-o` | Must not exist (delete to rerun) |

## Decision tree

```text
Need contigs quickly with moderate memory?
├─ Yes → megahit
├─ Need max continuity, can pay RAM/time → metaspades
└─ Long reads dominant → long-read assembler (not megahit alone)
```

## Validation, recovery, and provenance

Require non-empty `final.contigs.fa`, a completed `log`, and expected input-library accounting. Check unique contig IDs, total assembled bases, contig count/N50/length distribution with `$quast`, read recruitment with a mapper, and assembly sensitivity to individual versus coassembly design. N50 alone is not a biological quality score.

MEGAHIT refuses an existing output directory; use `--continue` only for an unchanged interrupted run supported by the pinned release, otherwise archive/remove the partial directory and start clean. Preserve `log`, `options.json`/command output where present, MEGAHIT version, read manifests/checksums, resource usage, and final-contig checksum before deleting intermediates.

## Related skills

`metaspades` · `prodigal` · `metawrap` · `basalt` · `study-design`

