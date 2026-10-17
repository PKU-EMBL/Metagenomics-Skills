---
name: humann
description: >
  Gene-family and pathway abundance profiling from metagenomes. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "function, pathways, profiling"
  metagenomics.upstream: "https://github.com/biobakery/humann"
---

# HUMAnN

Upstream: [biobakery/humann](https://github.com/biobakery/humann)

## Citation

Beghini, F. *et al.* Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife* **10**, e65088 (2021). https://doi.org/10.7554/eLife.65088

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

HUMAnN maps reads to a gene catalog (UniRef-based) and aggregates to pathways.
Treat pathway abundance as **homology-supported functional potential**, not
measured enzyme activity or flux.

Prefer dehosted reads. HUMAnN commonly expects a single interleaved/merged PE
stream depending on version—follow the installed version’s input rules.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Dehosted reads | From `kneaddata` |
| DBs | chocophlan + uniref | Version-locked with HUMAnN |
| RAM | 32 GB | 64–128 GB |
| Time | High | Parallelize by sample |

## How to run

```bash
# After configuring humann databases (humann_config / humann_databases)
humann \
  --input temp/hr/${id}_merged.fastq \
  --output temp/humann/${id} \
  --threads 8
```

Post-process: join tables, renormalize (CPM/RPK), regroup to KO/GO as needed.

## Decision tree

```text
Need functional pathways from reads?
├─ Yes → humann
├─ Only taxonomy → metaphlan or kraken2
└─ Gene catalogue on assemblies → prodigal + eggnog-mapper (+ salmon)
```

## Related skills

`metaphlan` · `kneaddata` · `visualization` · `eggnog-mapper`

