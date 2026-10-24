---
name: tool-selection
description: >
  Choose shotgun tools by stage: QC, assembly, mapping, binning, taxonomic annotation,
  functional annotation, microbial mining, and research analysis (stats/figures). Use
  when deciding which skill to load — mappers, assemblers, ensemble binning (BASALT
  recommended), profilers, miners, or DA/plotting tools. For mining use
  microbial-mining; for stats/figures use research-analysis.
license: MIT
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "guidance, tool-selection, mapping, binning, mining, research-analysis, workflow"
  metagenomics.stage: "utilities"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "routing matrix reviewed; selected tools must be executed through their own skills"
---

# Tool Selection

Start from the **stage**, then the deliverable.

## Selection contract

Before naming a tool, state the scientific claim, input unit/technology, sample
count and pairing, expected deliverable, database/license constraints, compute,
and whether the request is exploratory or publication-bound. Return a primary
choice, justified alternatives, incompatibilities, validation gate, and the
specific child skill to load. Tool popularity or benchmark rank alone is not a
selection criterion.

Never combine outputs merely because tools address the same broad stage. Define
how identifiers, taxonomies, scores, abundance units, database releases, and
failure/no-hit states will be reconciled before proposing an ensemble.

## By stage

```text
1 QC       contamination-control · fastp · kneaddata · hostile · fastqc · cutadapt · trimmomatic
           long-read-qc → nanoplot · chopper · filtlong · hifiadapterfilt
2 Assembly megahit · metaspades · metaflye · metamdbg  (+ quast)
           polish: racon (long) · pilon (short)
           coassembly planning: binchicken (low-abundance / novelty)
3 Mapping  strobealign | bowtie2 | bwa-mem2 | bwa | minimap2 · lexicmap · phylign · samtools · diamond
4 Binning  metabat2 · maxbin2 · concoct · semibin2 · vamb · aamb · taxvamb · comebin · metabinner · lorbin · metacoag
           → basalt ★ · metawrap · dastool → anvio / deepurify → drep · skani · fastani · coverm · checkm2 · gunc
5 Taxonomy metaphlan · singlem · kraken2+bracken · motus · sylph · sourmash · metabuli · kaiju · gtdbtk
           eukaryotes → eukaryotic-metagenomics · tiara · whokaryote · eukcc
           phylogenomics → phylophlan · iqtree · fasttree · lucaphylo
6 Function humann · prodigal · bakta · prokka · cd-hit · mmseqs2 · salmon
           · eggnog-mapper · rgi · homology-search
           RNA → metatranscriptomics · sortmerna; pangenome → pangenome-analysis · panaroo · ppanggolin
           models → community-metabolic-modeling · carveme · micom
7 Mining   microbial-mining → resistome-analysis · mobilome-analysis · arg-mge-host-linkage
           · horizontal-gene-transfer · antismash · bigscape · genomad · virsorter2 · checkv · vcontact
           · mobileog · isescan · integronfinder · mob-suite · plasx · mobmess · plasmaag · macrel
           · cge-finders · plasmidfinder · resfinder · pointfinder
           · disinfinder · virulencefinder · mobileelementfinder
           · pmlst · mlst · staramr · abricate
           · amrfinderplus · args-oap · pathofact · deeparg
           · metachip · waafle · hgtector · metator · hicbin · viralcc · spacepharer
           · element-cycling · metabolic · mebs · fegenie · dom-biosurfactant
           · hadeg · biosurfdb · dram · dbcan · gapseq · vmh
           · defensefinder · padloc · qsap
8 Strain   strain-resolved-analysis → midas2 · strainge · strainfacts · instrain · strainphlan · metasnv
           → strain-transmission → poppunk · gubbins · transphylo
9 Report   research-analysis → multiqc · microeco · phyloseq · visualization
           · maaslin2 · ancombc · aldex2 · corncob · lefse · stamp
           · permanova · netcomi · sparcc · spieceasi · absolute-abundance
           · source-tracking · feast · sourcetracker2 · transfer-network-analysis
           · nextflow · snakemake · nf-core-mag · nf-core-taxprofiler
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
| Resistome | `resistome-analysis` → `rgi` / `amrfinderplus` / `args-oap` / `deeparg` / `pathofact` |
| ARG–MGE–host physical/host evidence | `arg-mge-host-linkage` |
| HGT candidates by evolutionary scale | `horizontal-gene-transfer` → `metachip` / `waafle` / `hgtector` / `gubbins` |
| Viruses / vOTUs / hosts | `virome-analysis` → `genomad`/`virsorter2`/`vibrant` → `checkv` → `votu-workflow` → `vcontact`/`iphop`/`spacepharer` |
| Plasmids / MGEs | `mobilome-analysis` → `genomad` / `plasx` / `mobmess` plus context-specific MGE tools |
| MGE proteins / IS / integrons | `mobileog` / `isescan` / `integronfinder` |
| CGE Finders (+ pMLST / mlst / ABRicate) | `cge-finders` |
| Plasmid MOB / replicon typing | `mob-suite` / `plasmidfinder` (± `pmlst`) |
| Plasmid genome recovery | `plasmaag` |
| AMPs | `macrel` |
| Element cycling (C/N/S/Fe/P/…) | `element-cycling` |
| DOM / biosurfactant / HC biodegradation | `dom-biosurfactant` |
| Distilled metabolism | `dram` |
| CAZymes / glycan DOM substrates | `dbcan` |
| Metabolic models | `community-metabolic-modeling` → `carveme` / `gapseq` / `micom` |
| Defense systems | `defensefinder` / `padloc` |
| Quorum sensing | `qsap` |

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

## Research analysis (stats · figures · reports · workflows)

| Need | Prefer |
|------|--------|
| Route stats / figures / QC / workflows | `research-analysis` |
| Diversity + composition R workflow | `microeco` |
| phyloseq data class / classic plots | `phyloseq` |
| Multivariable differential abundance | `maaslin2` |
| Compositional bias-corrected DA | `ancombc`; Monte Carlo CLR effects → `aldex2` |
| Count mean and dispersion effects | `corncob` |
| Community-level distance test | `permanova` (with dispersion and restricted permutations) |
| Classic LDA biomarkers | `lefse` |
| GUI exploratory profile stats | `stamp` |
| SparCC correlations | `sparcc` |
| Network construction/comparison | `netcomi` (or focused `sparcc` / `spieceasi`) |
| Source contribution estimates | `source-tracking` → `feast` / `sourcetracker2` |
| Evidence-typed ARG/MGE/host/strain graphs | `transfer-network-analysis` |
| Shared strains versus transmission | `strain-transmission` after `strain-resolved-analysis` |
| Load-aware quantities | `absolute-abundance` with measured calibration |
| Aggregated QC HTML | `multiqc` |
| Figure checklist by stage | `visualization` |
| Nextflow / nf-core pipelines | `nextflow` → `nf-core-mag` / `nf-core-taxprofiler` |
| Snakemake rule DAGs | `snakemake` |

## Never

- Skip mapping when binning needs coverage
- Merge taxonomy methods unlabeled
- Treat mining hits as validated products/phenotypes
- Call bins MAGs before QC filters
- Run group statistics before inspecting batch / library-size structure

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

`metagenomics-workflow` · `microbial-mining` · `resistome-analysis` ·
`mobilome-analysis` · `arg-mge-host-linkage` · `horizontal-gene-transfer` ·
`strain-resolved-analysis` · `strain-transmission` · `transfer-network-analysis` ·
`homology-search` · `phylogenomics` ·
`genome-language-model` · `protein-language-model` · `metagenomics-llm` ·
`element-cycling` · `dom-biosurfactant` · `cge-finders` · `research-analysis` ·
`study-design` ·
`public-databases`
