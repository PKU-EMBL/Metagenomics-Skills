---
name: deeparg
description: >-
  Predict antibiotic-resistance-gene classes from nucleotide or protein sequences with the
  modern DeepARG 2.0 PyTorch/Transformers runtime. Use for long-sequence LS or short-read SS
  models, immutable Hugging Face bundle staging, probability and alignment filtering,
  optional read quantification, and comparison with curated ARG callers.
license: MIT
compatibility: Requires DeepARG 2.0.0, Python 3.10+, PyTorch/Transformers, DIAMOND, a pinned gaarangoa/deeparg model/database bundle, and nucleotide or protein FASTA.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "DeepARG,AMR,ARG,deep-learning,Transformers,DIAMOND"
  metagenomics.upstream: "https://github.com/gaarangoa/DeepARG"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.0.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "modern CLI/model/output contract reviewed; not executed here"
---

# DeepARG

DeepARG 2.0 modernizes the original LS/SS models while retaining DeepARG v2 feature
databases. Use `deeparg predict`, not the legacy `deepARG --align` command.

## Choose the model

- **LS**: assembled genes/ORFs or longer nucleotide sequences; protein input avoids
  nucleotide translation ambiguity when gene calls are controlled.
- **SS**: short-read/short-fragment classification and the `short_reads_pipeline`.

DeepARG classes, CARD AROs, NCBI AMRFinder families, SARG subtypes, and ResFinder gene names
are distinct namespaces. Preserve native labels and database hits.

## Stage an immutable model bundle

The default first run downloads `gaarangoa/deeparg` dynamically. For a reproducible run,
stage the reviewed snapshot once and checksum it:

```bash
set -euo pipefail
bundle=${DEEPARG_BUNDLE:-resources/deeparg-hf-07d2eaa}
revision=07d2eaa78502f41725c4222de1288b8b2f0d6259
for path in "$bundle" "${bundle}.sha256" \
  "${bundle}.download.stdout.log" "${bundle}.download.stderr.log"; do
  [[ ! -e "$path" ]] || { echo "refusing to overwrite: $path" >&2; exit 2; }
done
mkdir -p "$(dirname "$bundle")"
python3 - "$bundle" "$revision" \
  >"${bundle}.download.stdout.log" 2>"${bundle}.download.stderr.log" <<'PY'
import hashlib
from pathlib import Path
import sys
from huggingface_hub import snapshot_download
bundle = Path(sys.argv[1])
snapshot_download(repo_id="gaarangoa/deeparg", revision=sys.argv[2], local_dir=bundle)
with Path(str(bundle) + ".sha256").open("w", encoding="utf-8") as out:
    for path in sorted(item for item in bundle.rglob("*") if item.is_file()):
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        out.write(f"{digest.hexdigest()}  {path.relative_to(bundle).as_posix()}\n")
PY
[[ -s "${bundle}.sha256" && -s "$bundle/LS/config.json" && \
   -s "$bundle/SS/config.json" && -s "$bundle/LS/database/features.dmnd" && \
   -s "$bundle/SS/database/features.dmnd" ]] || exit 3
for model in LS SS; do
  find "$bundle/$model" -maxdepth 1 -type f \
    \( -name '*.safetensors' -o -name 'pytorch_model*.bin' \) \
    -size +0c -print -quit | grep -q .
done
```

The reviewed snapshot bundles LS/SS weights/config, DIAMOND databases, gene lengths,
Linux DIAMOND binaries, and optional gg13 Bowtie2 files. Preserve licensing and source
metadata for every asset. On non-Linux systems provide a compatible native DIAMOND.

## Predict assembled proteins

```bash
set -euo pipefail
sample=${SAMPLE_ID:?set SAMPLE_ID}
proteins=${PROTEINS:?set PROTEINS}
bundle=${DEEPARG_BUNDLE:?set DEEPARG_BUNDLE}
out=${OUTDIR:-results/deeparg/$sample}
[[ -s "$proteins" && -d "$bundle/LS" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
python3 -c 'from importlib.metadata import version; print(version("deeparg"))' \
  >"$out/software-version.txt"
deeparg predict --model LS --type prot -i "$proteins" -o "$out/$sample" \
  --hf-model-path "$bundle" --hf-device cpu --min-prob 0.8 \
  >"$out/predict.stdout.log" 2>"$out/predict.stderr.log"
[[ -e "$out/$sample.mapping.ARG" && \
   -e "$out/$sample.mapping.potential.ARG" && \
   -e "$out/$sample.align.daa.tsv" ]] || exit 3
```

For nucleotide genes use `--type nucl`. Empty high-confidence/potential files can be valid
no-hit states; require existence and reconcile sequence IDs rather than requiring a
positive call. Retain the DIAMOND alignment table.

For paired reads, use `deeparg short_reads_pipeline --forward-pe-file R1 --reverse-pe-file
R2 --output-file PREFIX`; it additionally requires Trimmomatic and vsearch. Optional
`--normalize-16s` requires Bowtie2/samtools and estimates a marker-based denominator, not
absolute abundance. Prefer independently QC-filtered reads and `$absolute-abundance` for
external calibration.

## Validation

- reconcile every predicted `QUERY_ID` with the input and retain no-hit sequences;
- inspect probability, best-hit identity, alignment length/bitscore, class, and interval;
- predeclare probability/identity/coverage rules and sensitivity-test them;
- treat `*.potential.ARG` as a separate uncertainty tier;
- review model/database training-domain overlap and false positives in homologous proteins;
- compare priority predictions with `$rgi`, `$amrfinderplus`, or `$resfinder`;
- link to MGE/host only through coordinate-preserving evidence.

## Recovery and provenance

Reuse the local bundle only after checksum verification. Input, model revision, DIAMOND,
threshold, or sequence-type changes require a new output directory. Record DeepARG,
PyTorch/Transformers/DIAMOND versions, model repo/revision/checksums, command, input
checksums, model, sequence type, device, thresholds, and all post-filters.

## Interpretation

DeepARG predicts sequence/class compatibility, not expression, phenotypic resistance,
clinical susceptibility, host, or mobility. Model agreement with a related training
database is not independent experimental validation.

## Sources

- https://github.com/gaarangoa/DeepARG
- https://huggingface.co/gaarangoa/deeparg
- https://doi.org/10.1186/s40168-018-0401-z

## Related skills

`resistome-analysis` · `rgi` · `amrfinderplus` · `resfinder` · `args-oap` ·
`absolute-abundance` · `arg-mge-host-linkage`
