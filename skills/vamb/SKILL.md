---
name: vamb
description: >
  Deep variational autoencoder binning of metagenome contigs. Use this skill when working with vamb: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/RasmussenLab/vamb. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['binning', 'vae', 'deep-learning']
upstream: https://github.com/RasmussenLab/vamb
stage: binning
---

# VAMB

Upstream: [VAMB](https://github.com/RasmussenLab/vamb)

## Citation

Nissen, J. N. *et al.* Improved metagenome binning and assembly using deep variational autoencoders. *Nat. Biotechnol.* **39**, 555–560 (2021). https://doi.org/10.1038/s41587-020-00777-4

See also [docs/references.md](../../docs/references.md).

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

```bash
conda install -c bioconda vamb  # if packaged; else follow upstream

vamb --outdir temp/bins/vamb --fasta contigs.fa --bamfiles temp/map/*.bam -p 16
# GPU optional depending on VAMB version / docs
```

## Key parameters

| Flag | Notes |
|------|-------|
| `--bamfiles` | Sorted BAMs; multi-sample improves coabundance signal |
| multisplit / clustering | Follow upstream defaults unless reproducing a paper |
| GPU | Optional acceleration |

## Literature notes

- Do not confuse VAMB’s “multisplit bins” with BASALT multi-assembly refinement.
- Adding VAMB bins into DAS Tool ensembles was beneficial in the paper’s
  comparisons — diversity of algorithms matters.
- Closely related strains may still collapse; validate with `skani` / `instrain`.

## Related skills

`semibin2` · `comebin` · `metabat2` · `dastool` · `basalt` · `skani` ·
`tool-selection` · `metagenomics-workflow`
