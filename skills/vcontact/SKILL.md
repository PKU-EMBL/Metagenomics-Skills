---
name: vcontact
description: >
  vConTACT2 / vConTACT3 — gene-sharing network and ML-based hierarchical virus taxonomy
  for prokaryotic (and in v3, broader realm) viral genomes/contigs. Use after viral
  discovery (geNomad / VirSorter2) and quality (CheckV): (1) Genus-to-order style
  clustering, (2) Placing vMAGs vs RefSeq/ICTV, (3) Choosing v2 vs v3.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "virus, taxonomy, vConTACT, gene-sharing, ICTV"
  metagenomics.upstream: "https://bitbucket.org/MAVERICLab/vcontact3"
  metagenomics.stage: "mining"
---

# vConTACT2 / vConTACT3

Upstream: [vConTACT2](https://bitbucket.org/MAVERICLab/vcontact2) ·
[vConTACT3](https://bitbucket.org/MAVERICLab/vcontact3)

## Citation

Jang, H. B. *et al.* Taxonomic assignment of uncultivated prokaryotic virus
genomes is enabled by gene-sharing networks. *Nat. Biotechnol.* **37**, 632–639
(2019). https://doi.org/10.1038/s41587-019-0100-8

Bolduc, B. *et al.* Machine learning enables scalable and systematic hierarchical
virus taxonomy. *Nat. Biotechnol.* (2025).
https://doi.org/10.1038/s41587-025-02946-9

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Viruses lack a universal marker gene. vConTACT builds **gene-sharing networks**
(v2) and, in v3, **ML hierarchical taxonomy** with realm-aware cut-offs, scaling
to large metagenomic viral sets and improving agreement with ICTV-style ranks.

Pipeline position:

```text
contigs → genomad | virsorter2 → checkv (quality filter)
       → proteins (Prodigal/Bakta as required by vConTACT)
       → vcontact3 (prefer for new work) | vcontact2
```

| Edition | Prefer when |
|---------|-------------|
| vConTACT3 | New analyses; hierarchical ranks; broader realms; scale |
| vConTACT2 | Reproducing older Methods / published networks |

Network clusters ≠ wet-lab host range. Report reference DB (Viral RefSeq /
ICTV snapshot) and software version.

## How to run

```bash
# follow Bitbucket/Apptainer docs for your edition — CLI differs by version
# typical inputs: viral genomes/contigs + predicted proteins + reference set
```

## Decision tree

```text
Viral sequences in hand?
├─ Not yet discovered → genomad / virsorter2
├─ Need quality → checkv
├─ Need taxonomy / clustering → vcontact (v3 preferred)
└─ Only presence of viral contigs → stop at genomad/checkv
```

## Related skills

`genomad` · `virsorter2` · `checkv` · `microbial-mining` · `prodigal` ·
`tool-selection`
