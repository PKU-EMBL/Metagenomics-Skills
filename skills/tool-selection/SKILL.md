---
name: tool-selection
description: >
  Choose shotgun tools by stage: QC, assembly, mapping, binning, taxonomic
  annotation, functional annotation, and microbial mining. Use when deciding
  which skill to load — mappers, assemblers, ensemble binning (BASALT
  recommended), profilers, or miners (antiSMASH, geNomad, DRAM, RGI, …).
  For stage order use metagenomics-workflow. For mining goals use microbial-mining.
license: MIT
category: orchestration
tags: [guidance, tool-selection, mapping, binning, mining, workflow]
---

# Tool Selection

Start from the **stage**, then the deliverable.

## By stage

```text
1 QC       fastp · kneaddata · fastqc · cutadapt · trimmomatic
2 Assembly megahit · metaspades · metaflye · metamdbg  (+ quast)
           polish: racon (long) · pilon (short)
           coassembly planning: binchicken (low-abundance / novelty)
3 Mapping  strobealign | bowtie2 | bwa-mem2 | bwa | minimap2 · lexicmap · phylign · samtools · diamond
4 Binning  metabat2 · maxbin2 · concoct · semibin2 · vamb · aamb · taxvamb · comebin · metabinner · lorbin
           → basalt ★ · metawrap · dastool → anvio / deepurify → drep · skani · fastani · coverm · checkm2 · gunc
5 Taxonomy metaphlan · singlem · kraken2+bracken · motus · sylph · metabuli · kaiju · gtdbtk
           phylogenomics → phylophlan · iqtree · fasttree · lucaphylo
6 Function humann · prodigal · bakta · prokka · cd-hit · mmseqs2 · salmon
           · eggnog-mapper · rgi · homology-search
7 Mining   microbial-mining → antismash · bigscape · genomad · virsorter2 · checkv · vcontact
           · plasmaag · macrel · dram · dbcan · gapseq · vmh · deeparg · defensefinder
```

## Mapping head-to-head

| Need | Prefer |
|------|--------|
| Fast Illumina → large contigs | `strobealign` |
| Lab Bowtie2 / KneadData ecosystem | `bowtie2` |
| BWA-MEM compatible + speed | `bwa-mem2` |
| Long reads | `minimap2` |
| Gene/plasmid vs millions of genomes | `lexicmap` |
| Phylogeny-compressed 661k-style search | `phylign` |

## Taxonomy head-to-head

| Need | Prefer |
|------|--------|
| Marker SGBs / pathways with HUMAnN | `metaphlan` |
| Unknowns / environments lacking genomes | `singlem` |
| Fast DNA k-mer + abundance | `kraken2` + `bracken` |
| Joint DNA+AA classification | `metabuli` |
| Protein-level sensitivity | `kaiju` |
| Sketch containment / coverage-adjusted ANI | `sylph` |
| MAG taxonomy | `gtdbtk` |

## ANI head-to-head

| Need | Prefer |
|------|--------|
| Large MAG catalogues / incomplete genomes | `skani` |
| Literature-compatible FastANI Methods | `fastani` |
| Dereplication workflow | `drep` (± ANI backend) |

## Mining head-to-head

| Goal | Prefer |
|------|--------|
| BGCs / natural products | `antismash` → `bigscape` |
| Resistome | `rgi` (± `deeparg`) |
| Plasmids / viruses / MGEs | `genomad` (± `virsorter2` → `checkv` → `vcontact`) |
| Plasmid genome recovery | `plasmaag` |
| AMPs | `macrel` |
| Distilled metabolism | `dram` |
| CAZymes | `dbcan` |
| Metabolic models | `gapseq` |
| Defense systems | `defensefinder` |

## Ensemble binning

| Skill | When |
|-------|------|
| `basalt` | **Recommended** multi-assembly refinement |
| `metawrap` | Packaged multi-binner suite |
| `dastool` | Aggregate contig2bin tables |

Single-binner diversity for ensembles: `metabat2` · `semibin2` · `vamb` · `aamb` ·
`taxvamb` · `comebin` · `metabinner` · `lorbin` (long-read).

Post-bin polish: `anvio` (interactive) · `deepurify` (decontaminate) → re-QC.

## Coverage for binning

| Practice | Prefer |
|----------|--------|
| Related samples available | **Multi-coverage** BAMs into binners |
| Only one sample | Single-coverage (acknowledge hidden contamination risk) |
| Huge public cohorts / rare taxa | `binchicken` targeted coassembly → then bin |

## Homology search (all paradigms)

| Need | Prefer |
|------|--------|
| Route any homology search | `homology-search` |
| Sequence / NR / contig tax | `mmseqs2` · `diamond` |
| Profile HMM remote homology | `hh-suite` |
| Protein-level assembly from reads | `plass` |
| Eukaryotic gene call | `metaeuk` |
| Structure / motif / MSA | `foldseek` · `folddisco` · `foldmason` |
| Structure archive | `foldcomp` |
| Peta-scale protein search | `petasearch` |
| Vector DB + embeddings | `erast` |
| Phylogeny-compressed genomes | `phylign` |
| Gene vs million genomes | `lexicmap` |

## Phylogenomics / trees

| Need | Prefer |
|------|--------|
| Route trees / evolution | `phylogenomics` |
| MAG taxonomy placement | `gtdbtk` |
| MAG/genome phylogeny workflow | `phylophlan` |
| Structural core-gene phylogeny | `unicore` |
| Publication ML tree | `iqtree` |
| Fast draft tree | `fasttree` |
| Alignment-free PLM phylogeny | `lucaphylo` |

## Genome language models

| Need | Prefer |
|------|--------|
| Route genome language models | `genome-language-model` |
| Metagenomic corpus + gLM2 | `omg` |
| Nucleotide Transformer / NTv3 | `nucleotide-transformer` |
| Multi-species efficient gLM (GUE) | `dnabert2` |
| Long-range RC-aware DNA LM | `caduceus` |
| Generative long-context DNA (Evo 2) | `evo2` |

## Protein language models

| Need | Prefer |
|------|--------|
| Route protein language models | `protein-language-model` |
| ESM-2 embeddings (pinned / Atlas-era) | `esm` |
| ESM C / Cambrian embeddings | `esmc` |
| Structure-aware AA+3Di PLM (Westlake) | `saprot` |
| AA ↔ 3Di / Foldseek from FASTA | `prostt5` (± `foldseek`) |
| Remote protein homology (PLM search) | `plmsearch` / `deepblast` |
| Alignment-free PLM phylogeny | `lucaphylo` |

## AI / LM & structure search (Steinegger + PLMs)

| Need | Prefer |
|------|--------|
| Route LM / Foldseek stack | `metagenomics-llm` |
| Protein LM detail menu | `protein-language-model` |
| Conserved gene clusters (structure-aware) | `spacedust` |
| GEM + structure/dark metabolism | `alphagem` |

## Never

- Skip mapping when binning needs coverage
- Merge taxonomy methods unlabeled
- Treat mining hits as validated products/phenotypes
- Call bins MAGs before QC filters

## Public data (short)

| Need | Skill |
|------|-------|
| Raw reads | `sra-ena` |
| Biome MAG catalogues | `mgnify` |
| GTDB taxonomy | `gtdb` / `gtdbtk` |
| Annotated genome warehouse | `progenomes` |
| Gold-standard benchmarks | `cami` (± `insilicoseq`) |
| Marker profiling (unknowns) | `singlem` |
| Gene vs million genomes | `lexicmap` |
| KEGG KO (licensed) | `kegg` |
| Full map | `public-databases` |

## Related skills

`metagenomics-workflow` · `microbial-mining` · `homology-search` · `phylogenomics` ·
`genome-language-model` · `protein-language-model` · `metagenomics-llm` ·
`study-design` · `public-databases`
