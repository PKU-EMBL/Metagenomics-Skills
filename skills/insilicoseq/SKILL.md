---
name: insilicoseq
description: >
  InSilicoSeq — simulate realistic Illumina (meta)genomic reads for benchmarking and
  experimental design. Use when: (1) Generating Illumina-like test sets from genomes,
  (2) Simple abundance-controlled mock communities, (3) Complementing CAMISIM for
  CAMI-style community simulation. For full CAMI gold standards prefer cami / CAMISIM.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "simulation, Illumina, benchmark, InSilicoSeq"
  metagenomics.upstream: "https://github.com/HadrienG/InSilicoSeq"
  metagenomics.stage: "assessment"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "2.0.1"
  metagenomics.command-status: "current generate options and paired output names checked against upstream source/docs; not executed here"
---

# InSilicoSeq

Upstream: [HadrienG/InSilicoSeq](https://github.com/HadrienG/InSilicoSeq) ·
Docs: https://insilicoseq.readthedocs.io/

## Citation

Gourlé, H., Karlsson-Lindsjö, O., Hayer, J. & Bongcam-Rudloff, E. Simulating
Illumina metagenomic data with InSilicoSeq. *Bioinformatics* **35**, 521–522
(2019). https://doi.org/10.1093/bioinformatics/bty630

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

| Simulator | Strength |
|-----------|----------|
| `insilicoseq` | Fast Illumina metagenome reads; simple CLI |
| CAMISIM (`cami`) | Multi-sample designs, strain diversity, CAMI gold standards |

Use InSilicoSeq for lightweight tool tests; use CAMISIM/CAMI when you need
challenge-grade gold standards for assembly/binning/profiling.

## How to run

Install InSilicoSeq 2.0.1 in a locked conda environment or pinned container.

```bash
set -euo pipefail
out=${ISS_OUT_DIR:?set a fresh output directory}
abundance=${ISS_ABUNDANCE_FILE:?set a two-column abundance file}
genomes=("genome1.fa" "genome2.fa")  # replace; each path remains a separate argument
[[ -s "$abundance" ]] || exit 2
for genome in "${genomes[@]}"; do [[ -s "$genome" ]] || exit 3; done
[[ ! -e "$out" ]] || { echo "refusing to overwrite: $out" >&2; exit 4; }
mkdir -p "$out/logs" "$out/provenance"
iss --version >"$out/provenance/iss.version.txt" 2>&1
sha256sum "${genomes[@]}" "$abundance" >"$out/provenance/inputs.sha256"
iss generate --genomes "${genomes[@]}" --model NovaSeq \
  --abundance_file "$abundance" --output "$out/mock" --n_reads 5M \
  --seed 42 --cpus 8 >"$out/logs/stdout.log" 2>"$out/logs/stderr.log"
[[ -s "$out/mock_R1.fastq" && -s "$out/mock_R2.fastq" ]]
[[ -s "$out/mock_abundance.txt" ]]
gzip -n "$out/mock_R1.fastq" "$out/mock_R2.fastq"
for fq in "$out/mock_R1.fastq.gz" "$out/mock_R2.fastq.gz"; do gzip -t "$fq"; done
r1=$(gzip -cd "$out/mock_R1.fastq.gz" | awk 'END {if (NR%4) exit 2; print NR/4}')
r2=$(gzip -cd "$out/mock_R2.fastq.gz" | awk 'END {if (NR%4) exit 2; print NR/4}')
printf 'file\treads\nR1\t%s\nR2\t%s\n' "$r1" "$r2" \
  >"$out/provenance/read-counts.tsv"
[[ "$r1" -gt 0 && "$r1" -eq "$r2" ]]
```

For complete genomes, every FASTA record is treated as a genome. Use `--draft`
for multi-contig draft genomes. Abundance-file identifiers must match the input
records and sum to 1; distinguish read abundance from cell abundance. `--n_reads`
is the total number of reads, not read pairs.

## Validation, recovery, and provenance

Validate unique reference identifiers, abundance reconciliation, nonzero and
matched R1/R2 counts, FASTQ structure, read-length/quality/error/insert-size
profiles and realized per-genome abundance by remapping. Include negative,
low-abundance, near-strain and unseen-genome cases appropriate to the benchmark.
One simulated community is not evidence of real-biome performance.

Rerun in a fresh directory after changing references, abundances, model, seed or
version. Archive input FASTA/abundance checksums, ISS version/environment,
built-in or custom model identity/checksum, seed, requested and realized read
counts, exact command/logs and validation summaries. Preserve failed runs; do not
silently regenerate with a new random seed.

## Related skills

`cami` · `quast` · `metaphlan` · `kraken2` · `tool-selection`
