---
name: strainfacts
description: >-
  Deconvolve strain genotypes and relative abundances across many metagenomes with
  StrainFacts from biallelic core-site metagenotypes. Use when mixed populations invalidate
  consensus-only comparisons, when choosing strain number and seeds, or when auditing
  model fit, uncertainty, identifiability, and downstream strain-sharing claims.
license: MIT
compatibility: Requires StrainFacts 0.6.0 source/runtime, PyTorch/Pyro dependencies, multi-sample metagenotypes such as filtered GT-Pro output, and CPU/GPU resources.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "StrainFacts,strain-deconvolution,metagenotype,mixture,Pyro"
  metagenomics.upstream: "https://github.com/bsmith89/StrainFacts"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "0.6.0 commit bd6f3ff3bc7b"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/data/model contract reviewed against upstream; not executed here"
---

# StrainFacts

StrainFacts jointly infers latent strain genotypes and their relative abundance across
samples. It needs multiple samples with biallelic core-site allele counts for one species;
it does not take raw metagenomic reads directly.

## Input contract

- metagenotype counts from one pinned reference/catalogue and species;
- exact sample/site crosswalk and allele orientation;
- biallelic core positions with mapping/quality filters documented;
- enough covered samples and polymorphic positions after filtering;
- predeclared candidate strain counts, seeds, model-selection criterion, and convergence
  diagnostics.

GT-Pro is the upstream-preferred metagenotyper. MIDAS2 can be adapted only after its allele
semantics are transformed and verified.

## Load, filter, fit, and export

```bash
set -euo pipefail
input=${GTPRO_METAGENOTYPE:?set GTPRO_METAGENOTYPE}
out=${OUTDIR:-results/strainfacts}
strains=${NUM_STRAINS:-10}
[[ -s "$input" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
{
  sfacts load --gtpro-metagenotype "$input" "$out/raw.mgen.nc"
  sfacts filter_mgen --min-minor-allele-freq 0.05 --min-horizontal-cvrg 0.10 \
    "$out/raw.mgen.nc" "$out/filtered.mgen.nc"
} >"$out/prepare.stdout.log" 2>"$out/prepare.stderr.log"
sfacts fit --verbose --device cpu --precision 32 --random-seed 0 \
  --num-strains "$strains" --history-outpath "$out/fit.history.tsv" \
  "$out/filtered.mgen.nc" "$out/fit.world.nc" \
  >"$out/fit.stdout.log" 2>"$out/fit.stderr.log"
sfacts dump "$out/fit.world.nc" --genotype "$out/genotypes.tsv" \
  --community "$out/communities.tsv" \
  >"$out/dump.stdout.log" 2>"$out/dump.stderr.log"
[[ -s "$out/fit.world.nc" && -s "$out/fit.history.tsv" && \
   -s "$out/genotypes.tsv" && -s "$out/communities.tsv" ]] || exit 3
```

The filter values and strain count are explicit examples, not defaults to apply blindly.
Fit a predeclared grid of plausible strain counts and multiple seeds in separate output
directories. Never select the solution solely because it best matches exposure labels.

## Validation

- report samples/positions before and after filtering and all dropped samples;
- inspect optimization history, convergence/ELBO behavior, replicate-seed stability, and
  posterior predictive/metagenotype reconstruction error;
- identify label switching and near-duplicate/low-abundance latent strains;
- compare estimated abundance/genotype stability across strain counts and site subsets;
- validate with simulations or known mixtures matched to coverage and error;
- only compare inferred strains across samples when genotype uncertainty permits.

## Recovery and provenance

A fit can be rerun from an immutable NetCDF metagenotype, but model, filters, strain count,
seed, precision, or package changes require a new output. Record StrainFacts/PyTorch/Pyro
versions, metagenotyper/reference/database, all filters, commands, seeds, hardware,
optimization settings, and input/output checksums.

## Interpretation

Latent factors are model-inferred strains and can be weakly identifiable. Relative
abundances do not provide absolute load. Similar latent genotypes across people support
shared-strain hypotheses only after coverage, uncertainty, background, time, and
alternative mixtures are considered; they do not prove direct transmission.

## Source

- https://github.com/bsmith89/StrainFacts
- https://doi.org/10.3389/fbinf.2022.867386

## Related skills

`strain-transmission` · `midas2` · `instrain` · `strainge` ·
`strain-resolved-analysis` · `absolute-abundance`
