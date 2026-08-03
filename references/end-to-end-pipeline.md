# End-to-end shotgun pathway

This document describes stages shared by EasyMetagenome community analyses and
BASALT MAG recovery. Prefer **BASALT or BASALT-Air** for refined multi-assembly
genome recovery; prefer **EasyMetagenome** for read-based tables, gene catalogues,
and classical MetaWRAP catalogues ([easymetagenome.md](easymetagenome.md)).

## Canonical stage order

```text
raw reads + metadata
  → quality control (fastp) and host depletion (KneadData or equivalent)
  → [optional] read-based taxonomy and function (HUMAnN4 / MetaPhlAn4 / Kraken2)
  → assembly (MEGAHIT default; metaSPAdes optional; sample-specific ± matched pool)
  → gene catalogue (Prodigal → cd-hit → salmon → eggNOG/CARD) or proceed to genomes
  → coverage estimation from designated evidence reads
  → binning: MetaWRAP (classical) or BASALT (refined multi-assembly)
  → quality assessment (CheckM2 preferred)
  → dereplication (dRep / ANI) when constructing a non-redundant catalogue
  → taxonomy (GTDB-Tk) and genome abundance (CoverM)
  → visualization and comparative statistics
```

Every composition or MAG claim requires documented reads, databases, parameters,
and quality-control resources.

## Read QC defaults

- Prefer **fastp** (EasyMetagenome default); record JSON/HTML and raw vs clean counts.
- Host depletion with **KneadData** + Bowtie2 host index; use `--reorder`; verify
  PE headers. Record host genome (e.g. hg39).
- Keep raw and cleaned checksums when storage allows; publish dehosted human data.
- Pair consistency matters: R1/R2 swaps break MetaWRAP, salmon, and BASALT
  PE-connectivity refinement.

## Assembly defaults

| Read type | Common assemblers | Notes |
|---|---|---|
| Illumina PE | MEGAHIT, metaSPAdes | Start sample-specific; add matched pool only if justified |
| ONT / CLR | metaFlye, other LR assemblers | Hybrid strategies need explicit read roles |
| HiFi | hifiasm-meta / Flye variants | Keep HiFi separate from CLR/ONT in BASALT (`-hf` vs `-l`) |

Record: assembler name, version, command line, threads/memory, and which reads
entered each assembly. BASALT does not assemble the metagenome for you; it
consumes assemblies plus coverage reads.

## Classical binning (when not using BASALT)

### EasyMetagenome / MetaWRAP default

1. Assemble (often MEGAHIT co-assembly or per-sample / subgroup).
2. `metawrap binning --metabat2 --maxbin2` (± CONCOCT; costly).
3. `metawrap bin_refinement -c 50 -x 10`.
4. Collect bins (`Mx_` / `Sg_` / `Gp_` prefixes) → **dRep** (`-sa 0.95` or `0.99`,
   `-nc 0.30`, `-comp 50`, `-con 10`).
5. Optional CheckM2 refresh; **CoverM** quantify; **GTDB-Tk** classify + tree.

### Minimal manual stack

1. Map reads → BAM; depth via `jgi_summarize_bam_contig_depths` or equivalent.
2. Bin with MetaBAT 2 / SemiBin 2 / CONCOCT / MaxBin / VAMB.
3. Aggregate (DAS Tool, etc.) if combining manually; CheckM2 filter.

These paths lack BASALT’s cross-assembly selection, MLP contig screening,
connectivity-based retrieval, and bin reassembly unless added explicitly.

## Coverage rules shared with BASALT

- Coverage files must come from the reads intended as evidence for that assembly.
- Multi-sample depth matrices are powerful for differential abundance fingerprints
  only when samples are biologically related.
- Contig ID identity must be preserved when importing external binsets into
  BASALT data-feeding routes.

## Quality and catalogue construction

1. Prefer **CheckM2** for high-throughput bacterial/archaeal estimates; record DB
   path and version. CheckM remains acceptable when required for legacy
   comparison—do not mix databases silently across design comparisons.
2. Publication filters are often stricter than BASALT’s refinement entry gates
   (`--min-cpn` / `--max-ctn`). State both.
3. Dereplicate catalogues with an explicit ANI/alignment tool and threshold.
4. Taxonomy (e.g. GTDB-Tk) is a separate claim layer; do not treat binner labels
   as taxonomy.
5. Functional annotation (DRAM, eggNOG, etc.) should use the final dereplicated
   MAG set unless the question is about discarded candidates.

## Extreme environments and host systems (PKU-EMBL context)

When advising PKU-EMBL-style projects (extreme environments, host-associated
microbiomes, AI + microbiome methods):

- Preserve stratum labels that define the scientific contrast.
- Expect uneven depth and high novelty; marker-based completeness can be
  conservative for unusual lineages—report the limitation.
- For AI method papers, keep the boundary between **learned models**,
  **classical optimization/binning**, and **manual curation** explicit.

## Gene catalogue defaults (EasyMetagenome)

| Step | Default |
|---|---|
| Genes | Prodigal `-p meta` |
| Cluster | `cd-hit-est -c 0.95 -aS 0.9 -G 0 -g 0` |
| Quant | salmon `--meta` → TPM and NumReads tables |
| Function | eggNOG-mapper (DIAMOND); optional RGI/CARD |

## Deliverables checklist

- Design / metadata manifest (TSV)
- Dehosted reads or regenerable KneadData command + host DB ID
- Read-based tables with profiler + DB version (if claimed)
- Assembly FASTA + assembler command
- Gene NR FASTA + salmon + annotation tables (if claimed)
- MAG FASTA set + CheckM2/CheckM + dRep + GTDB (+ CoverM)
- Software versions + checksums for key inputs, DBs, and BASALT models
- Citations: EasyMetagenome and/or BASALT as used
