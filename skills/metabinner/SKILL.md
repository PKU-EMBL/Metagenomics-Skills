---
name: metabinner
description: >
  MetaBinner — stand-alone ensemble contig binning using multi-feature k-means
  components and two-stage single-copy-gene ensemble integration. Use when: (1) Running
  MetaBinner as an ensemble-style single tool, (2) Comparing to MetaWRAP/DAS
  Tool/COMEBin, (3) Diversifying bin sets before further refinement. For recommended
  multi-assembly refinement still prefer basalt ★.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, MetaBinner, ensemble, SCG"
  metagenomics.upstream: "https://github.com/ziyewang/MetaBinner"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "snapshot 50a1281"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# MetaBinner

Upstream: [ziyewang/MetaBinner](https://github.com/ziyewang/MetaBinner)

## Citation

Wang, Z. *et al.* MetaBinner: a high-performance and stand-alone ensemble
binning method to recover individual genomes from complex microbial
communities. *Genome Biol.* **24**, 1 (2023).
https://doi.org/10.1186/s13059-022-02832-6

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

MetaBinner is an **internal ensemble**: multiple k-means component binning
results (multi-feature) integrated with SCG-aware two-stage selection — a
stand-alone alternative to piping MetaBAT/MaxBin into MetaWRAP/DAS Tool.

Still feed outputs through CheckM2; for related multi-assembly catalogues prefer
`basalt` ★. Complements `comebin` from the same group.

## Inputs and run

Supply the length-filtered assembly, a tab-delimited coverage profile (contigs × samples), and the matching comma-delimited k-mer profile. All paths passed to the wrapper must be absolute and contig IDs/order must reconcile with the FASTA.

```bash
set -euo pipefail
MB=$(dirname "$(command -v run_metabinner.sh)")
contigs=$(realpath final.contigs_f1k.fa)
coverage=$(realpath coverage_profile_f1k.tsv)
kmer=$(realpath kmer_4_f1000.csv)
out=$(realpath -m result/metabinner)
[[ -s "$contigs" && -s "$coverage" && -s "$kmer" ]] || exit 2
bash "$MB/run_metabinner.sh" -a "$contigs" -o "$out" \
  -d "$coverage" -k "$kmer" -p "$MB" -t 16 -s large \
  >metabinner.stdout.log 2>metabinner.stderr.log
test -s "$out/metabinner_res/metabinner_result.tsv"
```

## Validation, recovery, and provenance

Validate that every assignment in `metabinner_res/metabinner_result.tsv` names a real contig, no contig is assigned to multiple final bins, and generated bin FASTAs reconstruct those memberships. Tabulate binned/unbinned bases and evaluate candidates with CheckM2 and GUNC before refinement/dereplication; compare against independent binners under the same minimum-contig policy.

Use a new output after changing assembly, profiles, scale or threads; do not combine component/intermediate results across runs. Record MetaBinner commit/environment, command, assembly/profile checksums and schemas, sample order, minimum contig length, output assignments and candidate checksums. An ensemble assignment remains a binning hypothesis.

## Related skills

`comebin` · `metawrap` · `dastool` · `basalt` · `checkm2` · `tool-selection`
