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
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "canonical cut/coverage/cluster/merge/extract workflow reviewed; not executed here"
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

Provide an ordered BAM manifest with one explicit path per line; its order becomes
the coverage-column order.

```bash
set -Eeuo pipefail
assembly="${1:?usage: run-concoct.sh ASSEMBLY BAM_LIST OUTPUT_DIR}"
bam_list="${2:?usage: run-concoct.sh ASSEMBLY BAM_LIST OUTPUT_DIR}"
out="${3:?usage: run-concoct.sh ASSEMBLY BAM_LIST OUTPUT_DIR}"
test -s "$assembly" && test -s "$bam_list" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
bams=()
while IFS= read -r bam || [[ -n "$bam" ]]; do
  [[ -z "$bam" || "$bam" = \#* ]] && continue
  test -s "$bam" || exit 2
  test -s "$bam.bai" || test -s "${bam%.bam}.bai" || exit 2
  samtools quickcheck "$bam"
  bams+=("$bam")
done <"$bam_list"
((${#bams[@]} > 0)) || exit 2
mkdir -p "$out/work/concoct_output" "$out/bins" "$out/logs"
cp "$bam_list" "$out/bam-manifest.txt"

(
  cut_up_fasta.py "$assembly" -c 10000 -o 0 --merge_last \
    -b "$out/work/contigs_10k.bed" >"$out/work/contigs_10k.fa"
  concoct_coverage_table.py "$out/work/contigs_10k.bed" "${bams[@]}" \
    >"$out/work/coverage.tsv"
  concoct --composition_file "$out/work/contigs_10k.fa" \
    --coverage_file "$out/work/coverage.tsv" -b "$out/work/concoct_output/"
  merge_cutup_clustering.py "$out/work/concoct_output/clustering_gt1000.csv" \
    >"$out/clustering_merged.csv"
  extract_fasta_bins.py "$assembly" "$out/clustering_merged.csv" \
    --output_path "$out/bins"
) >"$out/logs/concoct.stdout.log" 2>"$out/logs/concoct.stderr.log"

test -s "$out/work/coverage.tsv"
test -s "$out/clustering_merged.csv"
n_bins="$(find "$out/bins" -maxdepth 1 -type f -name '*.fa' | wc -l | tr -d ' ')"
printf 'candidate_bins\t%s\n' "$n_bins" >"$out/validation.tsv"
```

Require every BAM to be coordinate-sorted/indexed and aligned to the exact
assembly checksum; header compatibility must be checked before the run.

## Key parameters

| contig cut length | 10 kb common | Required prep |
| coverage | BAM-derived | |

## Decision notes

- Stage: **binning** — strong ensemble member (composition + multi-coverage)
- Cut contigs (~10 kb) before clustering; prefer multi-coverage inputs
- Feed into `basalt` ★ / `metawrap` / `dastool` for catalogues

## Validation, recovery, and provenance

Reconcile all FASTA IDs across BED, coverage, chunk clustering and merged assignments; require unique final contig membership and non-empty candidate FASTAs or an explicit no-bin outcome. Summarize binned/unbinned bases and assess candidates with CheckM2/GUNC before ensemble selection. Inspect sample order and coverage variance; a one-sample run loses much of CONCOCT's differential-coverage signal.

Use a fresh prefix/output after changing assembly, BAMs, chunking or release.
Record CONCOCT and mapping/samtools versions, full command, assembly/BAM
checksums, ordered sample manifest, chunk policy, logs, coverage/assignment
checksums, explicit zero-bin outcome, and candidate QC. Clusters are candidate
bins, not validated genomes.

## Related skills

metabat2 · maxbin2 · dastool · metawrap · `tool-selection` · `metagenomics-workflow`
