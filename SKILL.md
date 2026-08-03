---
name: metagenomics-analysis
description: >-
  Protocols for shotgun metagenomic analysis spanning community profiling
  (EasyMetagenome: fastp, KneadData, HUMAnN4, MetaPhlAn4, Kraken2, MEGAHIT,
  MetaWRAP, dRep, CoverM, GTDB-Tk) and genome-resolved MAG recovery (PKU-EMBL
  BASALT/BASALT-Air, LorBin, multi-assembly refinement). Apply for metagenomics
  study design, read-based taxonomy and function, gene catalogues, MAG binning,
  co-assembly decisions, CheckM2 quality control, and reproducible Methods
  reporting.
---

# Shotgun Metagenomics Analysis Protocol

## Scope

This skill specifies an operational protocol for **shotgun metagenomics**, from
study design and preprocessing through community profiling, gene-catalogue
construction, and metagenome-assembled genome (MAG) recovery. Recommendations
must be driven by the scientific deliverable and must preserve a clear boundary
between computational products and biological claims.

Two complementary analytical stacks are supported:

| Stack | Primary outputs | Canonical reference |
|---|---|---|
| **EasyMetagenome** | Taxonomic/functional tables, non-redundant gene catalogues, MetaWRAP-based MAG catalogues | Bai et al., *iMeta* (2025) |
| **PKU-EMBL BASALT / BASALT-Air** | Multi-binner, cross-assembly refined MAG sets | Qiu et al. / BASALT, *Nat. Commun.* (2024); BASALT-Air repository |

Select the stack according to the required deliverable. Do not present MetaWRAP
defaults as equivalent to BASALT refinement, or marker-/k-mer-based profiles as
equivalent to MAG taxonomy.

## Authoritative sources

Prefer primary documentation over recalled flags or paths:

1. EasyMetagenome — https://github.com/YongxinLiu/EasyMetagenome  
   Citation: Bai et al. (2025) *iMeta* 4:e70001. https://doi.org/10.1002/imt2.70001
2. BASALT guide — https://basalt-guide.readthedocs.io/en/latest/  
   Citation: https://doi.org/10.1038/s41467-024-46539-7  
   BASALT-Air — https://github.com/PKU-EMBL/BASALT-Air
3. Local BASALT documentation when available (`BASALT_Guide/docs/`)
4. Progressive detail in [references/](references/)

## Analytical workflow

1. Classify the request (profiling, gene catalogue, classical MAGs, refined MAGs,
   visualization, installation, or Methods/provenance).
2. Finalize study design before co-assembly or pooling
   ([study-design.md](references/study-design.md)).
3. Construct a sample manifest linking identifiers, strata, host references,
   assemblies, and coverage evidence.
4. Preprocess reads (quality control and host depletion).
5. Execute the branch matched to the deliverable.
6. Validate on a pilot subset before scaling.
7. Apply **predeclared** acceptance criteria; do not optimize for maximum bin or
   taxon counts.
8. Archive software, database, parameter, and checksum provenance with results.

## Analytical constraints

The following constraints are mandatory. Violations frequently yield runnable
outputs that are scientifically invalid.

1. Do not pool biologically unrelated samples solely to increase sequencing depth.
2. Do not use reads or coverage matrices that lack a documented relationship to
   the target assembly.
3. Do not combine MetaPhlAn, Kraken2, and MAG-derived taxonomy into a single
   unlabeled abundance table.
4. Do not interpret additional binners, `more-sensitive` presets, or CONCOCT
   inclusion as guaranteed MAG improvement.
5. Do not describe BASALT multilayer-perceptron contig screening as experimental
   proof of contamination removal; report model identity and checksums when
   refinement underpins claims.
6. Do not resume a BASALT run after changes to inputs, code, models, or quality
   databases; start a new run directory instead.
7. Do not interchange Conda `BASALT` and BASALT-Air `basalt` commands or
   checkpoints.
8. Do not select a workflow solely because it maximizes recovered bins or taxa.
9. Do not invent command-line options; verify against EasyMetagenome scripts,
   `BASALT --help`, or local documentation.
10. Do not proceed to KneadData, MetaWRAP, or BASALT mapping without confirming
    paired-end identifier concordance.

### Interpretation of computational products

| Product | Appropriate interpretation | Inappropriate interpretation |
|---|---|---|
| MetaPhlAn / HUMAnN profiles | Marker- or homology-supported composition | Absolute cellular load or metabolic flux |
| Kraken2 + Bracken | Database-dependent k-mer classification | Exhaustive species inventory |
| cd-hit gene catalogue | Clustered predicted open reading frames | Complete community pangenome |
| MetaWRAP refined bins | Multi-binner, quality-gated draft genomes | BASALT-style cross-assembly refinement |
| BASALT refined MAGs | Feature- and connectivity-supported genomes | Strain definition without an ANI criterion |
| Increased N50 after reassembly | Improved contiguity | Demonstrated base-level accuracy |

## Procedure

### 0. Request triage

| Required deliverable | Recommended route | Reference |
|---|---|---|
| Species and pathway tables from reads | EasyMetagenome read-based profiling | [read-based.md](references/read-based.md), [easymetagenome.md](references/easymetagenome.md) |
| Quality control and host depletion | EasyMetagenome preprocessing | [easymetagenome.md](references/easymetagenome.md) |
| Gene catalogue with functional annotation | EasyMetagenome assembly branch | [easymetagenome.md](references/easymetagenome.md) |
| Classical MAG catalogue | MetaWRAP → dRep → CoverM → GTDB-Tk | [easymetagenome.md](references/easymetagenome.md) |
| Refined multi-assembly MAGs | BASALT or BASALT-Air | [basalt-cli.md](references/basalt-cli.md) |
| Co-assembly versus stratified assembly | Study-design assessment | [study-design.md](references/study-design.md) |
| Diversity and comparative graphics | EasyMetagenome statistical plotting | [easymetagenome.md](references/easymetagenome.md) |
| Environment and database deployment | EasyMetagenome installation patterns | [easymetagenome.md](references/easymetagenome.md) |
| Interrupted BASALT run | Diagnostic and resume protocol | [troubleshooting.md](references/troubleshooting.md) |

Request only those decisions that materially alter the analysis. Recover paths,
versions, and parameters from existing project files when available.

### 1. Study-design manifest

Required fields prior to assembly or genome recovery:

| Field | Purpose |
|---|---|
| `sample_id` | Stable identifier matching sequence filenames and metadata |
| `stratum` / `Group` | Biological partition (time, treatment, habitat, host) |
| `host_reference` | Host genome used for depletion |
| `assembly` | Contig FASTA for genome-resolved analyses |
| `assembly_type` | `individual`, `pool`, or `subgroup` |
| `assembly_reads` / `coverage_reads` | Exact read provenance |
| `run_directory` | Dedicated working directory for the analysis |

EasyMetagenome tutorials frequently co-assemble all samples for gene and MAG
modules. Replace that default with per-sample or subgroup assembly when the
primary contrast is defined by stratum membership, or when sample counts exceed
approximately 30 or total data volume exceeds approximately 300 Gb.

For BASALT, include sample-specific assemblies and a matched co-assembly in one
run only when joint coverage remains biologically interpretable.

### 2. Shared preprocessing defaults

1. Project layout: `seq/`, `temp/`, `result/metadata.txt` (Unix line endings).
2. Paired-end quality control with **fastp**; retain summary metrics.
3. Host depletion with **KneadData** using `--reorder`; verify read-header pairing.
4. Prefer deposition of dehosted reads for human-associated studies.
5. Empirical depth guidance for MAG recovery (EasyMetagenome authors): typically
   ≥6 Gb per sample; complex soils often ≥30 Gb.

See [end-to-end-pipeline.md](references/end-to-end-pipeline.md) and
[easymetagenome.md](references/easymetagenome.md).

### 3. Route selection

| Objective | Protocol |
|---|---|
| Taxonomic and pathway profiling from reads | HUMAnN4 + MetaPhlAn4 (± Kraken2/Bracken, LEfSe) |
| Non-redundant gene catalogue and annotation | MEGAHIT → Prodigal → cd-hit (95%) → salmon → eggNOG/CARD |
| Classical MAG catalogue | MetaWRAP (MetaBAT2 + MaxBin2; refinement c50/x10) → dRep (95%/99%) → CoverM → GTDB-Tk |
| New refined multi-assembly MAG analysis | BASALT-Air (`basalt`) |
| Reproduction of an existing Conda BASALT run | Conda BASALT (`BASALT`) |
| Controlled single-binner comparison | MetaBAT2 or SemiBin2 alone, with stated limitations |

**EasyMetagenome backbone**

```text
metadata + paired-end reads
  → fastp → KneadData
  → [A] HUMAnN4 / MetaPhlAn4 / Kraken2 (± LEfSe, GraPhlAn)
  → [B] MEGAHIT → Prodigal → cd-hit → salmon → eggNOG / CARD
  → [C] MetaWRAP binning and refinement → dRep → CoverM → GTDB-Tk
  → statistical visualization
```

**BASALT backbone**

```text
assemblies + reads
  → coverage and connectivity estimation
  → multi-binner candidate generation
  → within- and cross-assembly selection
  → contig screening, retrieval, and overlap–layout–consensus
  → reassembly when short reads are available
  → final MAG directory and quality report
```

Parameter detail: [easymetagenome.md](references/easymetagenome.md),
[basalt-cli.md](references/basalt-cli.md).

### 4. Execution standards

**EasyMetagenome.** Define `soft`, `db`, and `wd` each session; place EasyMicrobiome
utilities on `PATH`; execute installation, analysis, and plotting scripts in
order; activate stage-specific Conda environments; prefer packed environments
from institutional mirrors when dependency resolution is unreliable; delete bulky
intermediates only after verifying critical outputs.

**BASALT (Conda edition).** Use one dedicated run directory with simple local
filenames or symbolic links; separate paired-end mates with `,` and samples with
`/`; supply HiFi reads exclusively via `-hf`; set `--sensitive`, `--refinepara`,
`--min-cpn`, `--max-ctn`, `-q`, and `--mode` explicitly; never run concurrent
processes in the same directory; resume only under unchanged provenance; verify
external tools, five `BASALT_WEIGHT` ensemble descriptors, and the CheckM2
database before production runs.

```bash
BASALT \
  -a assembly.fasta \
  -s sample_R1.fastq,sample_R2.fastq \
  -t 32 -m 128 \
  --sensitive sensitive \
  --refinepara quick \
  --min-cpn 35 \
  --max-ctn 20 \
  -q checkm2 \
  --mode new \
  -o study_01_basalt
```

### 5. Evaluation and reporting

Declare acceptance criteria before inspecting results:

- **Read-based analyses:** profiler, database release, rarity filters, and grouping
  factors for comparative tests.
- **Gene catalogues:** clustering thresholds (default cd-hit identity 0.95,
  alignment coverage 0.9) and quantification units (TPM versus counts).
- **MAG catalogues:** completeness and contamination thresholds; dRep ANI
  (0.95 species-level / 0.99 strain-level in EasyMetagenome defaults); GTDB release.
- **BASALT:** distinguish refinement entry gates from stricter publication filters;
  record model checksums when refinement supports primary claims.

Methods sections must state software versions, database identities, assembly
mode, binning and dereplication thresholds, and whether genomes originated from
MetaWRAP or BASALT. Cite EasyMetagenome and/or BASALT as used.

## Diagnostics

1. EasyMetagenome failures — consult upstream script appendices and
   [easymetagenome.md](references/easymetagenome.md).
2. BASALT failures — follow [troubleshooting.md](references/troubleshooting.md).
3. Preserve logs and checksums before removing temporary directories.
4. Do not recommend insecure permission changes (`chmod 777`) or unnecessary
   privilege escalation for installation.

## Response standards

- Identify the analytical stack used in every recommendation.
- Prefer a pilot–evaluate–scale progression.
- Distinguish software-documented behaviour, mechanistically inferred explanation,
  and analyst recommendations.
- When local EasyMetagenome or BASALT sources are present, prefer them over
  recalled command syntax.

## Reference index

- [references/easymetagenome.md](references/easymetagenome.md) — EasyMetagenome protocol distillation
- [references/read-based.md](references/read-based.md) — profiler selection
- [references/study-design.md](references/study-design.md) — assembly and pooling design
- [references/end-to-end-pipeline.md](references/end-to-end-pipeline.md) — shared end-to-end pathway
- [references/basalt-cli.md](references/basalt-cli.md) — BASALT and BASALT-Air interfaces
- [references/troubleshooting.md](references/troubleshooting.md) — BASALT operational diagnostics
