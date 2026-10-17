---
name: diamond
description: >
  Ultra-fast protein alignment (BLASTP/X alternative) for functional/taxonomic searches.
  Use for installation, parameter choice, execution, output interpretation, or
  troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, protein, blast"
  metagenomics.upstream: "https://github.com/bbuchfink/diamond"
  metagenomics.stage: "mapping"
---

# DIAMOND

Upstream: [DIAMOND](https://github.com/bbuchfink/diamond)

## Citation

Buchfink, B., Reuter, K. & Drost, H.-G. Sensitive protein alignments at tree-of-life scale using DIAMOND. *Nat. Methods* **18**, 366–368 (2021). https://doi.org/10.1038/s41592-021-01101-x

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

DIAMOND provides sensitive protein alignments at proteome/tree-of-life scale
(Buchfink *et al.*, 2021) — the workhorse behind many functional and taxonomic
protein searches (eggNOG-mapper, DAS Tool protein search, custom NR/UniRef).

- Use `blastx`/`blastp` for genes/proteins; not a substitute for nucleotide
  coverage mappers (`strobealign` / `bowtie2`) needed for binning.
- Sensitivity modes (`--fast` → `--ultra-sensitive`) trade speed for remote
  homolog recall — state the mode in Methods.
- Tabular `-f 6` is pipeline-friendly; keep DB version pinned.


## How to run

```bash
conda install -c bioconda diamond  # if packaged; else follow upstream

diamond makedb --in proteins.faa -d ref
diamond blastp -q query.faa -d ref -o hits.tsv -p 16 -f 6
```

## Key parameters

| `blastp/blastx` | mode | |
| `-f 6` | tabular | BLAST-like |

## Related skills

eggnog-mapper · mmseqs2 · blast · `tool-selection` · `metagenomics-workflow`
