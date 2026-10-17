---
name: micom
description: >-
  Build abundance-weighted microbial community metabolic models and simulate cooperative growth and exchanges with MICOM. Use when taxon models, sample abundances, medium, solver, trade-off choice, failed-model coverage, and flux uncertainty can be validated explicitly.
license: MIT
compatibility: Requires MICOM 0.39.1, COBRA models or a MICOM model database, Python, a supported solver, and sample-level taxon abundances.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "micom,community-model,flux-balance,tradeoff,cross-feeding,metabolism"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "0.39.1"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "Python API reviewed against upstream; template not executed here"
---

# MICOM

MICOM combines taxon GEMs with relative abundance and optimizes community/taxon growth. It predicts feasible flux states; it does not observe metabolite exchange.

## Input contract

For a single sample, provide a TSV with at least `id`, `file`, and `abundance`; model files may be SBML XML/XML.GZ, JSON, MAT, or MICOM-supported formats. IDs and paths must be unique, abundances non-negative, and retained abundance should cover a declared fraction of the measured community.

Provide a medium TSV with `reaction` and positive `flux` columns using exchange IDs compatible with every model. Reconcile identifiers before simulation.

## Build and simulate one sample

```bash
cat > run_micom.py <<'PY'
import sys, pickle, pandas as pd
from micom import Community, __version__
if len(sys.argv) != 5:
    raise SystemExit("usage: run_micom.py taxonomy.tsv medium.tsv out_prefix solver")
tax = pd.read_csv(sys.argv[1], sep="\t")
med = pd.read_csv(sys.argv[2], sep="\t")
need = {"id", "file", "abundance"}
assert need <= set(tax), need-set(tax)
assert tax.id.is_unique and (tax.abundance >= 0).all() and tax.abundance.sum() > 0
assert {"reaction", "flux"} <= set(med) and med.reaction.is_unique
assert (med.flux > 0).all()
tax["abundance"] /= tax.abundance.sum()
com = Community(tax, solver=sys.argv[4])
com.medium = dict(zip(med.reaction, med.flux))
sol = com.cooperative_tradeoff(fraction=0.5, fluxes=True, pfba=True)
assert sol is not None and sol.members.growth_rate.notna().any()
sol.members.to_csv(sys.argv[3] + ".members.tsv", sep="\t")
sol.fluxes.to_csv(sys.argv[3] + ".fluxes.tsv", sep="\t")
with open(sys.argv[3] + ".community.pickle", "wb") as fh: pickle.dump(com, fh)
print("MICOM", __version__, "community_growth", sol.growth_rate,
      "taxa", len(com.taxa))
PY
set -euo pipefail
python3 run_micom.py taxonomy.tsv medium.tsv sample01 glpk \
  >sample01.micom.log 2>sample01.micom.stderr.log
[[ -s sample01.members.tsv && -s sample01.fluxes.tsv && \
   -s sample01.community.pickle ]] || exit 3
```

For cohorts, use `micom.workflows.build`, `tradeoff`, and `grow` with a model database, output folder, threads, and a pinned medium. First scan a trade-off grid rather than selecting 0.5 solely by convention.

## Validation

- report modeled and excluded taxa plus abundance coverage per sample;
- inspect model build warnings, solver status, community/taxon growth, and infeasible samples;
- confirm medium IDs actually open intended exchanges and flux signs are interpreted correctly;
- compare multiple cooperative trade-off fractions and plausible media/bounds;
- assess alternate optima/flux variability before highlighting exchanges;
- validate predicted production/consumption against metabolomics or culture evidence where available.

## Recovery and provenance

MICOM cohort build can resume existing valid models, but changed databases/inputs should use a new folder. Keep taxonomy/abundance tables, model-database checksum, medium, solver/version, trade-off, pickle/results, code, and logs.

## Analytical thinking

Predicted exchange does not establish pairwise cross-feeding, and abundance weights are not biomass measurements by default. Community objective, missing taxa, gap-filled models, medium, and alternate optima can reverse conclusions. Phrase outputs as model-predicted potentials.

## Source

- https://github.com/micom-dev/micom
