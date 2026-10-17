---
name: concoct
description: >
  Composition and coverage binning of metagenomic contigs. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, concoct"
  metagenomics.upstream: "https://github.com/BinPro/CONCOCT"
  metagenomics.stage: "binning"
---

# CONCOCT

Upstream: [CONCOCT](https://github.com/BinPro/CONCOCT)

## Citation

Alneberg, J. *et al.* Binning metagenomic contigs by coverage and composition. *Nat. Methods* **11**, 1144–1146 (2014). https://doi.org/10.1038/nmeth.3103

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

CONCOCT (Alneberg *et al.*, 2014) pioneered joint **composition + multi-sample
coverage** clustering (Gaussian mixture models). It remains a valuable **ensemble
member** because its inductive bias differs from MetaBAT2/MaxBin2/DL binners.

Operational rules:

- Cut long contigs into chunks (commonly ~10 kb) before clustering, then merge
  cutup clusters back to contigs — required by the CONCOCT workflow.
- Multi-coverage inputs matter (Mattock & Watson 2023); single-sample coverage
  weakens the method’s original strength.
- Memory-heavy on complex communities; often optional inside MetaWRAP.


## How to run

```bash
set -euo pipefail
conda install -c conda-forge -c bioconda concoct
[[ -s contigs.fa && -d temp/map ]] || exit 2
mapfile -t bams < <(find temp/map -maxdepth 1 -name '*.bam' -size +0c | sort)
(( ${#bams[@]} > 0 )) || exit 3
mkdir -p temp/concoct result/concoct/bins
cut_up_fasta.py contigs.fa -c 10000 -o 0 --merge_last \
  -b temp/concoct/contigs_10k.bed > temp/concoct/contigs_10k.fa
concoct_coverage_table.py temp/concoct/contigs_10k.bed "${bams[@]}" \
  > temp/concoct/coverage.tsv
concoct --composition_file temp/concoct/contigs_10k.fa \
  --coverage_file temp/concoct/coverage.tsv -b temp/concoct/run_
merge_cutup_clustering.py temp/concoct/run_clustering_gt1000.csv \
  > result/concoct/clustering_merged.csv
extract_fasta_bins.py contigs.fa result/concoct/clustering_merged.csv \
  --output_path result/concoct/bins
```

Require each BAM to be coordinate-sorted, indexed, and aligned to this exact assembly.

## Key parameters

| contig cut length | 10 kb common | Required prep |
| coverage | BAM-derived | |

## Decision notes

- Stage: **binning** — strong ensemble member (composition + multi-coverage)
- Cut contigs (~10 kb) before clustering; prefer multi-coverage inputs
- Feed into `basalt` ★ / `metawrap` / `dastool` for catalogues

## Validation, recovery, and provenance

Reconcile all FASTA IDs across BED, coverage, chunk clustering and merged assignments; require unique final contig membership and non-empty candidate FASTAs or an explicit no-bin outcome. Summarize binned/unbinned bases and assess candidates with CheckM2/GUNC before ensemble selection. Inspect sample order and coverage variance; a one-sample run loses much of CONCOCT's differential-coverage signal.

Use a fresh prefix/output after changing assembly, BAMs, chunking or release. Record CONCOCT and mapping/samtools versions, full command, assembly/BAM checksums, ordered sample manifest, chunk policy, coverage/assignment checksums and candidate QC. Clusters are candidate bins, not validated genomes.

## Related skills

metabat2 · maxbin2 · dastool · metawrap · `tool-selection` · `metagenomics-workflow`
