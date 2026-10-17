---
name: lexicmap
description: >
  LexicMap — efficient nucleotide alignment of moderate-length queries (genes, plasmids,
  long reads; typically >250 bp) against up to millions of prokaryotic genomes. Use
  when: (1) Searching genes/plasmids vs huge genome databases, (2) Scaling beyond
  BLAST/minimap2 for AllTheBacteria / GTDB-scale refs, (3) Epidemiology/ecology queries
  needing fast genome hits. Not a substitute for short-read→contig coverage mappers
  (strobealign/bowtie2) used in binning.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "alignment, search, LexicMap, genomes, BLAST"
  metagenomics.upstream: "https://github.com/shenwei356/LexicMap"
  metagenomics.stage: "mapping"
---

# LexicMap

Upstream: [shenwei356/LexicMap](https://github.com/shenwei356/LexicMap)

## Citation

Shen, W., Lees, J. A. & Iqbal, Z. Efficient sequence alignment against millions
of prokaryotic genomes with LexicMap. *Nat. Biotechnol.* (2025).
https://doi.org/10.1038/s41587-025-02812-8

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Problem: BLAST-style search against **millions** of bacterial genomes.
LexicMap indexes probe/seed structure for fast, lower-memory alignment of
moderate-length queries. Use for gene/plasmid/long-read queries against large
genome warehouses (`progenomes`, AllTheBacteria, GTDB reps).

| Task | Prefer |
|------|--------|
| Illumina reads → contigs (binning coverage) | `strobealign` / `bowtie2` |
| Gene/plasmid vs million genomes | `lexicmap` |
| Phylogeny-compressed 661k on a laptop | `phylign` |
| Protein remote homology | `diamond` / `mmseqs2` / `erast` |
| Species ANI between MAGs | `skani` / `fastani` |

## How to run

```bash
# Build one immutable index, record its manifest, then query it repeatedly.
lexicmap index -d genomes_dir -o db/lexicmap_idx
lexicmap search -d db/lexicmap_idx -q query.fa -o temp/lexicmap/hits.tsv
```

## Related skills

`homology-search` · `phylign` · `minimap2` · `diamond` · `mmseqs2` · `erast` ·
`progenomes` · `gtdb` · `plasmaag` ·
`tool-selection`
