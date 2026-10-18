---
name: transphylo
description: >-
  Infer probabilistic transmission trees and unsampled intermediates from a dated pathogen
  phylogeny with TransPhylo. Use only after recombination-aware, clock-supported phylogenetic
  analysis and when generation-time, sampling-time, sampling-proportion priors, MCMC
  diagnostics, and epidemiological exclusions can be justified.
license: MIT
compatibility: Requires R, ape, coda, TransPhylo 1.4.10, a rooted dated phylogeny with one tip per case, sampling dates, and external generation/sampling-time distributions.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "TransPhylo,transmission-tree,MCMC,dated-phylogeny,unsampled-hosts"
  metagenomics.upstream: "https://github.com/xavierdidelot/TransPhylo"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.4.10"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "R API and matrix/consensus contract reviewed; not executed here"
---

# TransPhylo

TransPhylo samples transmission trees conditional on a dated phylogeny and epidemiological
parameters. It can include unsampled hosts. A close or monophyletic pair is not sufficient
input: branch lengths must be in time units and the population/outbreak scope coherent.

## Preconditions

Require all of the following:

1. one pathogen/strain lineage with explicit case/tip crosswalk;
2. recombination-aware phylogeny, e.g. `$gubbins`, and a supported temporal signal;
3. branch lengths in declared time units and consistent sampling-date origin;
4. external generation-time and sampling-time distributions;
5. justified prior on sampling proportion and end-of-observation date;
6. plausible contact/location/time exclusions retained for posterior filtering.

Do not estimate generation time from the same transmission links you then claim to infer.

## One-chain auditable runner

Save this as a run-specific script and execute independent chains with different seeds.

```r
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 12)
suppressPackageStartupMessages({library(ape); library(coda); library(TransPhylo)})
tree <- read.tree(args[1])
date_last_sample <- as.numeric(args[2])
date_observation_end <- as.numeric(args[3])
w_mean <- as.numeric(args[4]); w_sd <- as.numeric(args[5])
ws_mean <- as.numeric(args[6]); ws_sd <- as.numeric(args[7])
start_pi <- as.numeric(args[8])
iterations <- as.integer(args[9]); thinning <- as.integer(args[10])
seed <- as.integer(args[11]); prefix <- args[12]
stopifnot(is.rooted(tree), !is.null(tree$edge.length),
          !anyDuplicated(tree$tip.label), all(is.finite(tree$edge.length)),
          all(tree$edge.length >= 0),
          w_mean > 0, w_sd > 0, ws_mean > 0, ws_sd > 0,
          start_pi > 0, start_pi < 1, iterations > thinning, thinning > 0,
          date_observation_end >= date_last_sample)
output_paths <- paste0(prefix, c(".chain.rds", ".who-infected-whom.tsv",
                                ".consensus-ttree.tsv", ".consensus-names.tsv",
                                ".consensus.rds", ".traces.pdf", ".ess.tsv"))
stopifnot(!any(file.exists(output_paths)))
dir.create(dirname(prefix), recursive = TRUE, showWarnings = FALSE)
set.seed(seed)
ptree <- ptreeFromPhylo(tree, dateLastSample = date_last_sample)
res <- inferTTree(ptree, w.mean = w_mean, w.std = w_sd,
                  ws.mean = ws_mean, ws.std = ws_sd, startPi = start_pi,
                  mcmcIterations = iterations, thinning = thinning,
                  updatePi = TRUE, dateT = date_observation_end)
chain_path <- paste0(prefix, ".chain.rds")
matrix_path <- paste0(prefix, ".who-infected-whom.tsv")
saveRDS(res, chain_path)
mat <- computeMatWIW(res, burnin = 0.5)
write.table(mat, matrix_path, sep = "\t", quote = FALSE, col.names = NA)
cons <- consTTree(res, burnin = 0.5)
write.table(cons$ttree, paste0(prefix, ".consensus-ttree.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE,
            col.names = c("infection_time", "sampling_time", "infector_index"))
write.table(data.frame(sample_index = seq_along(cons$nam), sample_name = cons$nam),
            paste0(prefix, ".consensus-names.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)
saveRDS(cons, paste0(prefix, ".consensus.rds"))
pdf(paste0(prefix, ".traces.pdf")); plotTraces(res, burnin = 0.5); dev.off()
ess <- effectiveSize(convertToCoda(res, burnin = 0.5))
write.table(data.frame(parameter = names(ess), effective_size = as.numeric(ess)),
            paste0(prefix, ".ess.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
stopifnot(file.info(chain_path)$size > 0, file.info(matrix_path)$size > 0)
```

Invoke the script with a dated Newick tree, time origin/end, externally justified means and
standard deviations, a defensible sampling-proportion starting value, sufficient
iterations/thinning, seed, and a new prefix. With `updatePi=TRUE`, TransPhylo 1.4.10 uses
its implemented uniform prior and `startPi` is an initialization, not a custom prior;
report and sensitivity-test both. The function names are `inferTTree`, `computeMatWIW`,
and `consTTree` in 1.4.10. `consTTree` returns a
TransPhylo `ttree`, not an `ape::phylo`; therefore the script writes its matrix and sampled
case-name crosswalk rather than fabricating a Newick tree.

## Validation

- verify every tree tip maps uniquely to a sampled case and date;
- assess temporal signal, branch uncertainty, and recombination/mixed-infection effects;
- run multiple dispersed chains and inspect trace, effective sample size, convergence, and
  sensitivity to burn-in, thinning, priors, generation/sampling distributions, and `dateT`;
- report posterior link probabilities, unsampled intermediates, and credible uncertainty;
- remove epidemiologically impossible links only under predeclared rules and renormalize/
  explain the effect;
- compare consensus summaries with the full `computeMatWIW` matrix.

A consensus transmission tree hides posterior alternatives and must not replace the matrix.

## Recovery and provenance

Never overwrite chains. Continue only through a documented package-supported state with
unchanged tree/priors; otherwise run new prefixes. Record TransPhylo/R/ape/coda versions,
tree and tip metadata checksums, time units/origin, all priors/distributions, observation
window, commands, chain seeds, MCMC settings, diagnostics, and exclusion rules.

## Interpretation

Posterior edges are model-dependent transmission hypotheses. They do not prove direct
contact, direction with certainty, or absence of unsampled intermediates. Phylogenetic
compatibility, strain sharing, and epidemiological plausibility remain separate evidence.

## Source

- https://github.com/xavierdidelot/TransPhylo
- https://doi.org/10.1093/molbev/msw275

## Related skills

`strain-transmission` · `gubbins` · `poppunk` · `iqtree` ·
`transfer-network-analysis` · `study-design`
