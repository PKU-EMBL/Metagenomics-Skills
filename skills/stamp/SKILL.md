---
name: stamp
description: >
  STAMP — Statistical Analysis of Metagenomic Profiles; GUI for taxonomic / functional
  profile tests with effect sizes, CIs, and publication plots (extended error bars, PCA,
  heatmaps). Use for interactive exploratory DA and classic two-group/multi-group tests.
  Prefer MaAsLin2/ANCOM-BC for covariate-heavy designs.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "STAMP, GUI, differential-abundance, effect-size, metagenomics"
  metagenomics.upstream: "https://github.com/dparks1134/STAMP"
  metagenomics.stage: "report"
  metagenomics.maturity: "legacy-gui"
  metagenomics.upstream-version: "2.1.3"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "GUI entry point reviewed; interactive analysis not executed here"
---

# STAMP

Upstream: [dparks1134/STAMP](https://github.com/dparks1134/STAMP) ·
https://beikolab.cs.dal.ca/software/STAMP

## Citation

Parks, D. H., Tyson, G. W., Hugenholtz, P. & Beiko, R. G. STAMP: statistical
analysis of taxonomic and functional profiles. *Bioinformatics* **30**,
3123–3124 (2014). https://doi.org/10.1093/bioinformatics/btu494

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

STAMP emphasizes **effect sizes + confidence intervals** alongside p-values and
offers a GUI for profile exploration. Good for teaching, quick two-group
figures, and legacy Methods. For multivariable / longitudinal designs prefer
`maaslin2` or `ancombc`. Pin STAMP version, test (e.g. Welch), and multiple-test
correction.

## Inputs and run

Use a dedicated legacy-compatible environment and the signed/checksummed 2.1.3 release. Prepare a STAMP profile (`.spf`) and metadata/mapping table with unique, exactly matching sample IDs; avoid feeding transformed percentages to tests that assume counts.

```bash
set -euo pipefail
command -v STAMP >/dev/null
[[ -s profiles.spf && -s metadata.tsv ]] || exit 2
STAMP
```

In the GUI, load the two files, record every filter/test/CI/effect-size/multiple-testing choice, inspect group sizes, then export the complete results table, session/preferences if supported, and figure source data. A GUI launch is only a preflight; the agent must not claim interactive steps occurred unless they were observed.

## Decision tree

```text
Exploratory / GUI profile stats?
├─ Yes → stamp
├─ Covariates / mixed models → maaslin2
├─ Compositional bias correction → ancombc
└─ Scripted R figures → microeco / phyloseq
```

## Validation, recovery, and provenance

Check sample joins, profile hierarchy, non-negative values, group replication and scale before testing. Require exported full results including non-significant rows; verify effect direction, confidence intervals, adjusted p-values, feature filtering and exact group labels. Reproduce priority results in scripted R/Python or a current method before publication.

Never overwrite exports from a different GUI setup. Record STAMP/OS/Python/Qt versions, input checksums, screenshots or machine-readable settings, all statistical options, output tables and figure source checksums. STAMP is a legacy exploratory GUI; its results do not handle arbitrary covariates, repeated measures or compositional bias automatically.

## Related skills

`research-analysis` · `maaslin2` · `ancombc` · `lefse` · `microeco` ·
`visualization` · `tool-selection`
