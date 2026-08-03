---
name: metagenomics-analysis
description: >-
  Protocols for shotgun metagenomic analysis across study design, read
  preprocessing, read-based taxonomy and function (HUMAnN, MetaPhlAn, Kraken2),
  assembly and gene catalogues, classical MAG recovery (MetaWRAP, dRep, CoverM,
  GTDB-Tk), and PKU-EMBL BASALT/BASALT-Air refined multi-assembly MAG recovery.
  Apply for metagenomics routing, co-assembly decisions, CheckM2 quality control,
  comparative statistics, and reproducible Methods reporting.
---

# Shotgun Metagenomics Analysis Protocol

## Scope

Operational protocol for **shotgun metagenomics**, from study design through
preprocessing, community profiling, gene-catalogue construction, and
metagenome-assembled genome (MAG) recovery. Route every request to a
**metagenomics module** defined by the scientific deliverable. Preserve a clear
boundary between computational products and biological claims.

## Authoritative sources

Prefer primary documentation over recalled flags or paths:

1. BASALT guide — https://basalt-guide.readthedocs.io/en/latest/  
   Publication: https://doi.org/10.1038/s41467-024-46539-7  
   BASALT-Air — https://github.com/PKU-EMBL/BASALT-Air
2. Local BASALT documentation when available (`BASALT_Guide/docs/`)
3. Module detail under [references/](references/)
4. Official manuals for named tools (fastp, KneadData, HUMAnN, MetaPhlAn,
   Kraken2, MEGAHIT, MetaWRAP, dRep, CoverM, GTDB-Tk, CheckM2)

## Analytical workflow

1. Triage into a metagenomics module (table below).
2. Finalize study design before co-assembly or pooling
   ([study-design.md](references/study-design.md)).
3. Build a sample manifest (identifiers, strata, host reference, assemblies,
   coverage evidence).
4. Complete preprocessing before branching.
5. Execute only the modules required by the deliverable.
6. Validate on a pilot subset before scaling.
7. Apply **predeclared** acceptance criteria.
8. Archive software, database, parameter, and checksum provenance.

## Analytical constraints

1. Do not pool biologically unrelated samples solely to increase depth.
2. Do not use reads or coverage lacking a documented link to the target assembly.
3. Do not merge MetaPhlAn, Kraken2, and MAG taxonomy into one unlabeled table.
4. Do not treat additional binners or higher-sensitivity presets as guaranteed
   MAG improvement.
5. Do not describe BASALT contig screening as experimental proof of contamination
   removal; report model identity and checksums when refinement supports claims.
6. Do not resume BASALT after changes to inputs, code, models, or quality
   databases; open a new run directory.
7. Do not interchange Conda `BASALT` and BASALT-Air `basalt` commands or
   checkpoints.
8. Do not select a workflow solely to maximize recovered bins or taxa.
9. Do not invent command-line options; verify against tool help or local docs.
10. Do not proceed to mapping or binning without paired-end identifier checks.

### Interpretation of products

| Product | Appropriate claim | Inappropriate claim |
|---|---|---|
| MetaPhlAn / HUMAnN profiles | Marker- or homology-supported composition | Absolute load or metabolic flux |
| Kraken2 + Bracken | Database-dependent k-mer classification | Exhaustive species inventory |
| cd-hit gene catalogue | Clustered predicted ORFs | Complete community pangenome |
| MetaWRAP refined bins | Multi-binner, quality-gated draft genomes | BASALT cross-assembly refinement |
| BASALT refined MAGs | Feature- and connectivity-supported genomes | Strain definition without ANI |
| Higher N50 after reassembly | Improved contiguity | Demonstrated base accuracy |

---

## Metagenomics modules (routing)

Route by deliverable. Load only the referenced module files needed for the task.

| Module | Deliverable | Reference |
|---|---|---|
| **A. Study design** | Assembly/pooling plan, strata, manifests | [study-design.md](references/study-design.md) |
| **B. Preprocessing** | QC metrics, host-depleted paired-end reads | [preprocessing.md](references/preprocessing.md) |
| **C. Read-based profiling** | Taxonomic and pathway tables from reads | [read-based.md](references/read-based.md) |
| **D. Assembly & gene catalogue** | Contigs, NR genes, functional tables | [gene-catalogue.md](references/gene-catalogue.md) |
| **E. Classical MAG recovery** | MetaWRAP → dRep → CoverM → GTDB-Tk catalogue | [mag-classical.md](references/mag-classical.md) |
| **F. Refined MAG recovery** | BASALT / BASALT-Air multi-assembly MAGs | [basalt-cli.md](references/basalt-cli.md) |
| **G. Comparative statistics & figures** | Alpha/beta, biomarkers, MAG plots | [visualization.md](references/visualization.md) |
| **H. End-to-end integration** | Full pathway and shared defaults | [end-to-end-pipeline.md](references/end-to-end-pipeline.md) |
| **I. Diagnostics** | Install/runtime failures (BASALT focus) | [troubleshooting.md](references/troubleshooting.md) |

### Module dependency sketch

```text
A Study design
  └─ B Preprocessing
        ├─ C Read-based profiling ──────────────┐
        ├─ D Assembly & gene catalogue ─────────┤
        │     └─ E Classical MAG recovery ──────┤→ G Statistics & figures
        └─ (assemblies + reads) → F BASALT ─────┘
```

Use **C** alone for composition tables; **D** for gene/function catalogues; **E**
or **F** for genomes. Prefer **F** when the goal is PKU-EMBL-style multi-assembly
refinement; use **E** for classical multi-binner catalogues and baselines.

---

## Shared procedure

### 1. Study-design manifest

| Field | Purpose |
|---|---|
| `sample_id` | Matches sequence filenames and metadata |
| `stratum` / `Group` | Time, treatment, habitat, host |
| `host_reference` | Host genome for depletion |
| `assembly` | Contig FASTA for genome-resolved work |
| `assembly_type` | `individual`, `pool`, or `subgroup` |
| `assembly_reads` / `coverage_reads` | Exact provenance |
| `run_directory` | Dedicated working directory |

Replace whole-cohort co-assembly with per-sample or subgroup assembly when the
primary contrast is stratum-defined, or when sample counts exceed ~30 or total
data exceed ~300 Gb. For BASALT, combine sample-specific and matched pooled
assemblies only when joint coverage remains biologically interpretable.

### 2. Preprocessing defaults

1. Layout: `seq/`, `temp/`, `result/metadata.txt` (Unix newlines).
2. Paired-end QC with **fastp**; retain summary metrics.
3. Host depletion with **KneadData** (`--reorder`); verify PE header pairing.
4. Prefer deposition of dehosted reads for human-associated studies.
5. MAG depth guidance: typically ≥6 Gb/sample; complex soils often ≥30 Gb.

### 3. Module-specific backbones

**C — Read-based**

```text
host-depleted PE → HUMAnN4 / MetaPhlAn4 (± Kraken2/Bracken, LEfSe)
```

**D — Gene catalogue**

```text
PE → MEGAHIT → Prodigal → cd-hit (c 0.95, aS 0.9) → salmon → eggNOG / CARD
```

**E — Classical MAGs**

```text
contigs + PE → MetaWRAP (MetaBAT2+MaxBin2, refine c50/x10)
  → dRep (ANI 0.95 or 0.99) → CoverM → GTDB-Tk
```

**F — Refined MAGs (BASALT)**

```text
assemblies + reads → coverage/connectivity → multi-binner candidates
  → within-/cross-assembly selection → contig screening/retrieval
  → reassembly → final MAG directory + QC report
```

### 4. BASALT execution standards (module F)

One dedicated run directory; local or symlink filenames for Conda BASALT; `,`
within pairs and `/` between samples; HiFi only via `-hf`; set `--sensitive`,
`--refinepara`, `--min-cpn`, `--max-ctn`, `-q`, `--mode` explicitly; no concurrent
processes in one directory; resume only under unchanged provenance.

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

Declare criteria before inspecting results:

- **C:** profiler, database release, rarity filters, grouping factors.
- **D:** clustering thresholds and quantification units (TPM vs counts).
- **E/F:** completeness/contamination; dRep ANI; GTDB release; for BASALT,
  refinement gates versus publication filters and model checksums.

Methods must state software versions, database identities, assembly mode,
binning/dereplication thresholds, and whether genomes came from classical
binning or BASALT. Cite BASALT when used.

## Diagnostics

1. Module B–E operational issues — see the corresponding reference file.
2. Module F — [troubleshooting.md](references/troubleshooting.md).
3. Preserve logs and checksums before deleting temporary data.
4. Do not recommend `chmod 777` or unnecessary privilege escalation.

## Response standards

- Name the active module(s) in every recommendation.
- Prefer pilot → evaluate → scale.
- Distinguish documented tool behaviour, mechanistic inference, and analyst advice.
- Prefer local BASALT documentation over recalled syntax when available.

## Reference index

- [references/study-design.md](references/study-design.md)
- [references/preprocessing.md](references/preprocessing.md)
- [references/read-based.md](references/read-based.md)
- [references/gene-catalogue.md](references/gene-catalogue.md)
- [references/mag-classical.md](references/mag-classical.md)
- [references/basalt-cli.md](references/basalt-cli.md)
- [references/visualization.md](references/visualization.md)
- [references/end-to-end-pipeline.md](references/end-to-end-pipeline.md)
- [references/troubleshooting.md](references/troubleshooting.md)
