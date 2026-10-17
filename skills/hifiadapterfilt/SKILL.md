---
name: hifiadapterfilt
description: >-
  Detect and remove PacBio HiFi reads containing residual SMRTbell adapter sequence with HiFiAdapterFilt or its FCS-adaptor pathway. Use before HiFi genome/metagenome assembly when adapter-contaminated reads could create false duplications or misassemblies.
license: MIT
compatibility: Requires HiFiAdapterFilt 3.0.1 scripts, BLAST+, BamTools for BAM input, and optionally pigz/FCS-adaptor.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "pacbio,hifi,adapter-removal,long-read,qc,hifiadapterfilt"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "3.0.1 script"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# HiFiAdapterFilt

HiFiAdapterFilt removes whole PacBio HiFi reads with detected remnant adapter matches. It is not an ONT quality filter.

## Inputs and setup

Accepts `.bam`, `.fastq`, `.fastq.gz`, `.fq`, or `.fq.gz`. Put the script directory and bundled `DB` directory on `PATH`, then record their git release/commit and adapter-database checksums.

```bash
export PATH="/opt/HiFiAdapterFilt:/opt/HiFiAdapterFilt/DB:$PATH"
command -v hifiadapterfilt.sh blastn bamtools
```

Do not process multiple samples in one working directory unless prefixes are unambiguous.

## Run one prefix

```bash
set -euo pipefail
prefix=${1:?usage: hifi-filter.sh file_prefix output_dir}
out=${2:?usage: hifi-filter.sh file_prefix output_dir}
mkdir -p "$out"
# The prefix resolves a .bam/.fastq[.gz]/.fq[.gz] in the working directory.
bash "$(command -v hifiadapterfilt.sh)" -p "$prefix" -l 44 -m 97 -t 16 -o "$out" \
  >"$out/${prefix}.stdout.log" 2>"$out/${prefix}.stderr.log"
[[ -s "$out/${prefix}.filt.fastq.gz" && -s "$out/${prefix}.stats" ]] || {
  echo "expected HiFiAdapterFilt outputs missing" >&2; exit 3;
}
gzip -t "$out/${prefix}.filt.fastq.gz"
```

The upstream defaults shown here require a minimum 44-bp adapter match at 97% identity. Do not alter them without preserving a sensitivity comparison.

If NCBI FCS Adaptor was used to detect contaminated reads:

```bash
bash hifiadapterfiltFCS.sh -f fcs_adaptor_report.txt -r hifi.fastq.gz \
  -t 16 -o hifi_fcs_filtered
```

## Outputs and checks

Expect `<prefix>.contaminant.blastout`, `<prefix>.blocklist`, `<prefix>.filt.fastq.gz`, and `<prefix>.stats`. Verify:

- every blocklisted ID exists in the input;
- filtered read count equals input minus unique blocked reads;
- gzip and FASTQ structure are valid;
- removal fraction is plausible and reported;
- assembly pilot metrics improve or at least do not degrade unexpectedly.

An empty blocklist may be legitimate, but missing stats or filtered FASTQ is not. Keep original HiFi reads and all matching evidence.

## Analytical thinking

Adapter matching is a technical-artifact screen, not general read-quality selection. Removing whole reads can reduce depth, while leaving adapter chimeras can create assembly errors. Report thresholds, database/script version, and observed removals rather than saying adapters were completely eliminated.

## Source

- https://github.com/sheinasim-USDA/HiFiAdapterFilt
