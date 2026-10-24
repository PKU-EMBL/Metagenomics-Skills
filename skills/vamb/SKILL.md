---
name: vamb
description: >
  Deep variational autoencoder binning of metagenome contigs. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, vae, deep-learning"
  metagenomics.upstream: "https://github.com/RasmussenLab/vamb"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "current vamb bin default contract checked against upstream docs; not executed here"
---

# VAMB

Upstream: [VAMB](https://github.com/RasmussenLab/vamb)

## Citation

Nissen, J. N. *et al.* Improved metagenome binning and assembly using deep variational autoencoders. *Nat. Biotechnol.* **39**, 555–560 (2021). https://doi.org/10.1038/s41587-020-00777-4

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

VAMB encodes **coabundance + k-mer** features with a VAE, then clusters the
latent space. Key design claims from the paper:

- Integrates composition and coverage **without** hand-tuned fusion weights.
- **Multisplit**: cluster across samples, then split into per-sample bins —
  aims to use coabundance while avoiding between-sample chimeric genomes that
  plague naive coassembly+binning.
- Reported large gains in near-complete genomes on CAMI/MetaHIT-style
  benchmarks; strain separation claimed up to ~99.5% ANI in that work.
- Benchmark difficulty (genome entropy) correlated with VAMB’s relative gains —
  expect more benefit in complex communities, not a flat uplift everywhere.

Use VAMB as a **diverse ensemble member** vs MetaBAT2/MaxBin2. Still run
CheckM2; prefer `basalt` ★ / `metawrap` / `dastool` for multi-binner consensus
when publishing catalogues.

## How to run

Current Vamb uses the `vamb bin default` interface. Place only BAMs mapped to the
exact input FASTA in the dedicated BAM directory, or supply a precomputed
abundance TSV.

```bash
set -Eeuo pipefail
assembly="${1:?usage: run-vamb.sh ASSEMBLY BAM_DIR OUTPUT_DIR}"
bamdir="${2:?usage: run-vamb.sh ASSEMBLY BAM_DIR OUTPUT_DIR}"
out="${3:?usage: run-vamb.sh ASSEMBLY BAM_DIR OUTPUT_DIR}"
threads="${THREADS:-16}"
seed="${VAMB_SEED:-1}"
test -s "$assembly" && test -d "$bamdir" || exit 2
find "$bamdir" -maxdepth 1 -type f -name '*.bam' -print -quit | grep -q . || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$(dirname "$out")" logs

vamb bin default --outdir "$out" --fasta "$assembly" --bamdir "$bamdir" \
  -p "$threads" --seed "$seed" --minfasta 200000 \
  >"logs/$(basename "$out").vamb.stdout.log" \
  2>"logs/$(basename "$out").vamb.stderr.log"
```

For multi-assembly binsplitting, preserve Vamb's required sample/contig naming
scheme and separator. `--cuda` accelerates supported installations but does not
guarantee bitwise reproducibility.

## Key parameters

| Flag | Notes |
|------|-------|
| `--bamfiles` | Sorted BAMs; multi-sample improves coabundance signal |
| multisplit / clustering | Record installed defaults; override only under a declared benchmark/reproduction |
| GPU | Optional acceleration |

## Literature notes

- Do not confuse VAMB’s “multisplit bins” with BASALT multi-assembly refinement.
- Adding VAMB bins into DAS Tool ensembles was beneficial in the paper’s
  comparisons — diversity of algorithms matters.
- Closely related strains may still collapse; validate with `skani` / `instrain`.

## Validation, recovery, and provenance

Require completed logs, composition/abundance artifacts, cluster tables, and a
non-empty `bins` directory when `--minfasta` is used. Verify Vamb's reference
hash checks, BAM/reference identity, sample order, binsplit behavior, unique
contig assignment, and binned fraction. Reassess bins with `checkm2` and `gunc`
and compare seed/model sensitivity for priority conclusions.

Use a new output directory after changing FASTA, abundance, model, seed, or Vamb
release. Record Vamb/PyTorch versions, CPU/GPU and seed, input checksums,
reference-hash status, commands, logs, cluster mapping, QC tables, and bin
checksums. Deep embeddings and clusters remain computational predictions.

## Related skills

`semibin2` · `comebin` · `metabat2` · `dastool` · `basalt` · `skani` ·
`checkm2` · `gunc` · `tool-selection` · `metagenomics-workflow`
