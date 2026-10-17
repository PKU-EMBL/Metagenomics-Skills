---
name: carveme
description: >-
  Reconstruct prokaryotic genome-scale metabolic models from protein or DNA sequences with CarveMe, optionally gap-filling against explicit media and exporting SBML. Use when model inputs, solver, universe, medium, and gap-filled reactions will be pinned and validated.
license: MIT
compatibility: Requires CarveMe 1.6.6, DIAMOND, a supported optimization solver, and protein FASTA or nucleotide genome.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "carveme,genome-scale-model,gem,gap-filling,sbml,flux-balance"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.6.6"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# CarveMe

CarveMe builds a genome-scale metabolic model by mapping proteins to a curated universe and solving a reconstruction problem.

## Preflight

```bash
set -euo pipefail
command -v carve diamond >/dev/null
carve --help > carveme.help.txt
python3 - <<'PY'
import carveme, cobra
print("carveme", getattr(carveme, "__version__", "record pip metadata"))
print("cobra", cobra.__version__)
PY
```

A commercial academic solver (CPLEX/Gurobi) or open-source SCIP is required. Record solver and version because performance and numerical behavior may differ.

## Input contract

Use a consistently called protein FASTA per bacterial/archaeal genome/MAG. Preserve genome quality, translation table, gene-to-protein map, and checksums. For nucleotide input, `--dna` invokes gene prediction; this can reduce annotation consistency across a catalogue.

## Reconstruct and validate

```bash
set -euo pipefail
faa=${1:?usage: carveme.sh proteins.faa model.xml}
out=${2:?usage: carveme.sh proteins.faa model.xml}
[[ -s "$faa" ]] || exit 2
[[ ! -e "$out" ]] || { echo "refusing to overwrite $out" >&2; exit 2; }
carve "$faa" --solver scip --fbc2 -o "$out" \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
python3 - "$out" <<'PY'
import sys, cobra
m = cobra.io.read_sbml_model(sys.argv[1])
assert len(m.reactions)>0 and len(m.metabolites)>0 and len(m.genes)>0
print(m.id, len(m.reactions), len(m.metabolites), len(m.genes), m.solver)
PY
```

For named-media gap filling:

```bash
carve proteins.faa --solver scip --gapfill M9,LB --fbc2 -o model.gapfilled.xml \
  >carve.gapfill.stdout.log 2>carve.gapfill.stderr.log
```

Use a custom media library with `--mediadb` when named built-ins do not represent the environment. Keep ungapfilled and gapfilled models separately. Upstream also supports `--egg` for compatible eggNOG-mapper annotations and `--universe-file` for custom universes.

## Quality gates

- SBML parses with COBRApy and has a defined biomass objective;
- model reaches only expected feasibility/growth under declared media;
- exchange bounds/sign conventions are inspected;
- added gap-fill reactions are enumerated and biologically reviewed;
- blocked/reaction/gene/metabolite counts and model warnings are reported;
- known growth phenotypes are tested where available.

Batch reconstruction should emit a manifest for successes and failures rather than silently omitting difficult MAGs.

## Recovery and provenance

Use new output names for changed universes/media/solver. Cache databases responsibly but record their release/checksum. Preserve input proteome, model, environment lock, solver, full command/log, medium, and validation report.

## Analytical thinking

Gap filling restores mathematical feasibility, not evidence that the organism encodes the inserted reaction. Gene absence in incomplete MAGs is uncertain. A reconstructed GEM describes potential under assumptions and needs `$micom` or other simulation plus empirical validation for community claims.

## Source

- https://github.com/cdanielmachado/carveme
