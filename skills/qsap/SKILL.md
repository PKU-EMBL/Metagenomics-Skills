---
name: qsap
description: >
  QSAP — quorum-sensing (QS) related gene annotation pipeline against the QSP database
  (DIAMOND and/or HMMER). Use when mining autoinducer / QS circuitry (AHL, AIP,
  AI-2-related families as covered by QSP) from proteins or assemblies. Related
  secondary metabolites → antismash; Fe siderophores → fegenie.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "QSAP, quorum-sensing, QS, autoinducer, signaling, genome-mining"
  metagenomics.upstream: "https://github.com/chunxiao-dcx/QSAP"
  metagenomics.stage: "mining"
---

# QSAP (quorum sensing)

Upstream: [chunxiao-dcx/QSAP](https://github.com/chunxiao-dcx/QSAP) ·
QSP database: https://github.com/chunxiao-dcx/QSP

## Citation

Pipeline/DB: Dai, C. QSAP / QSP — quorum-sensing protein resources
(https://github.com/chunxiao-dcx/QSAP). Cite the upstream repository and QSP
release used; add peer-reviewed QSP/QSAP citation when available in Methods.

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

**Quorum sensing (群体感应)** coordinates population behaviors via signal
synthases/receptors/transporters. QSAP classifies QS-related sequences from
the QSP collection. Treat hits as genetic potential — not measured autoinducer
concentrations.

| Related claim | Prefer |
|---------------|--------|
| QS genes | `qsap` |
| Specialized metabolite / AHL-adjacent BGCs | `antismash` |
| Siderophores (Fe acquisition signals/competition) | `fegenie` |
| Broad metabolism | `dram` / `element-cycling` |

## How to run

```bash
# Run from a pinned QSAP checkout after dependency and QSP-database preflight.
perl QSAP.pl -i input.list -o qsap_out -s sub -n 8
# Record the selected DIAMOND/HMM strategy and sub/union integration rule.
```

## Decision tree

```text
Cell–cell signaling / QS?
├─ QS gene annotation → qsap
├─ BGC / natural products → antismash
├─ Siderophores → fegenie
└─ Plasmid-borne QS context → genomad / mob-suite ∩ qsap
```

## Related skills

`antismash` · `fegenie` · `dram` · `genomad` · `mob-suite` ·
`microbial-mining` · `tool-selection`
