---
name: humann
description: >
  Gene-family and pathway abundance profiling from metagenomes. Use this skill when working with humann: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/biobakery/humann. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['function', 'pathways', 'profiling']
upstream: https://github.com/biobakery/humann
---

# HUMAnN

Upstream: [biobakery/humann](https://github.com/biobakery/humann)

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

