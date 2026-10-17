---
name: foldseek
description: >
  Foldseek — ultrafast protein structure search and clustering via the 3Di structural
  alphabet (Steinegger / Söding labs). Use when: (1) Searching MAG or predicted
  structures against AFDB/PDB/ESM Atlas, (2) Foldseek-Multimer complex search for
  distant systems (e.g. CRISPR–Cas), (3) Structure clustering at AFDB scale, (4)
  Sequence→structure search with ProstT5. Route via homology-search / metagenomics-llm;
  pairs with mmseqs2 (sequence) and folddisco (motifs).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Foldseek, 3Di, structure-search, AFDB, multimer, ProstT5, homology"
  metagenomics.upstream: "https://github.com/steineggerlab/foldseek"
  metagenomics.stage: "function"
---

# Foldseek

Upstream: [steineggerlab/foldseek](https://github.com/steineggerlab/foldseek) ·
Web: https://search.foldseek.com

## Citation

van Kempen, M. *et al.* Fast and accurate protein structure search with Foldseek.
*Nat. Biotechnol.* **42**, 243–246 (2024). https://doi.org/10.1038/s41587-023-01773-0

Kim, W. *et al.* Rapid and sensitive protein complex alignment with
Foldseek-Multimer. *Nat. Methods* **22**, 469–472 (2025).
https://doi.org/10.1038/s41592-025-02593-7

Barrio-Hernandez, I. *et al.* Clustering predicted structures at the scale of
the known protein universe. *Nature* **622**, 637–645 (2023).
https://doi.org/10.1038/s41586-023-06510-w

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Sequence search (`mmseqs2` / `diamond`) fails for many remote homologs. Foldseek
turns tertiary geometry into a **3Di** letter sequence and reuses MMseqs2-style
prefilters — roughly **10⁴–10⁵×** faster than TM-align/Dali/CE with comparable
sensitivity. Metagenomics use cases: AFDB/ESMAtlas annotation of dark MAG
proteins, structural NR clustering, and complex-level mining
(`easy-multimersearch`).

Martin Steinegger “AI and evolution” stack (conservation level → tool):

| Level | Prefer |
|-------|--------|
| Sequence / single-chain structure | `mmseqs2` · `foldseek` |
| Multimer / interface | Foldseek-Multimer (`easy-multimersearch`) |
| Local structural motif | `folddisco` |
| Conserved gene neighborhoods | `spacedust` (uses Foldseek) |

| vs | Prefer Foldseek when |
|----|----------------------|
| `mmseqs2` / `diamond` | Structures or ProstT5 path available; twilight-zone homology |
| `plmsearch` / `deepblast` | Real/predicted structures exist (or AFDB targets) |
| `folddisco` | Need whole-chain / complex fold match, not a short motif |
| TM-align / US-align | Database-scale search (not gold-standard pairwise polish) |

Hard rules:

1. Structural hits ≠ experimental function — pin AFDB/PDB release + Foldseek version
2. Low-confidence AF models (pLDDT) inflate false positives — filter inputs
3. Multimer claims need chain pairing / complex TM reporting, not monomer E-values alone
4. Do not merge Foldseek tables with BLAST/MMseqs unlabeled

## How to run

```bash
# databases (examples)
foldseek databases Alphafold/Proteome afdb tmp
foldseek databases PDB pdb tmp

# monomer structure search
foldseek easy-search query.pdb afdb aln.m8 tmp

# FASTA without structures → ProstT5 3Di
foldseek databases ProstT5 weights tmp
foldseek easy-search QUERY.faa pdb res.m8 tmp --prostt5-model weights

# structural clustering
foldseek easy-cluster structures/ clu tmp -c 0.9

# complexes (Foldseek-Multimer)
foldseek easy-multimersearch query_complex.pdb.gz pdb mm_result tmp
```

Webserver for interactive queries: https://search.foldseek.com

## Key parameters

| Setting | Notes |
|---------|-------|
| Input | PDB/mmCIF structures, or FASTA + `--prostt5-model` |
| Target DBs | AFDB proteomes, PDB100, ESMAtlas clusters — pin release |
| `--alignment-type` | 3Di/AA vs TM-align-style rescoring when needed |
| `--cluster-search` | Clustered DBs (AFDB50): reps-only vs expand members |
| `--gpu` | Optional GPU prefilter (Ampere+ preferred) |
| Multimer report | Use `_report` for chain pairing, TM, transforms |

## Decision tree

```text
Homology / structure need?
├─ Close sequence homologs → mmseqs2 / diamond
├─ Dark proteins, have/ predict structures → foldseek easy-search
├─ Sequence-only, no GPU structures → foldseek+ProstT5 or plmsearch / deepblast
├─ Multi-chain complexes / interfaces → foldseek easy-multimersearch
├─ Short active-site / motif geometry → folddisco
├─ Conserved neighborhoods → spacedust
└─ Structure NR catalogue → foldseek easy-cluster
```

## Related skills

`homology-search` · `protein-language-model` · `prostt5` · `esm` ·
`foldcomp` · `folddisco` · `foldmason` · `unicore` · `mmseqs2` · `hh-suite` ·
`petasearch` · `spacedust` · `plmsearch` · `deepblast` · `eggnog-mapper` ·
`microbial-mining` · `tool-selection`
