# Metagenomics Skills

[简体中文](README.zh-CN.md)

A comprehensive collection of **226 portable Agent Skills** for reproducible
shotgun metagenomics, organized by scientific stage and usable from Claude Code,
Codex, Cursor, Kimi Code, ZCode, Qwen Code, and other compatible coding agents:

**QC → assembly → mapping → binning → taxonomy → function → microbial mining → research analysis**

Current release: **v1.25.0**. It adds publication-grade execution, validation,
recovery, provenance, and evidence-boundary contracts across 101 existing Skills.

One skill per core tool (mappers, assemblers, binners, profilers, miners such as
antiSMASH / geNomad / DRAM, …) plus databases, language-model hubs, homology /
phylogenomics routing, and paper-facing stats/figures (`research-analysis`).

[Getting started](docs/getting-started.md) ·
[Skills](docs/skills.md) ·
[Pipeline](docs/standard-pipeline.md) ·
[Public databases](docs/public-databases.md) ·
[Agent playbook](docs/agent-playbook.md) ·
[ARG–MGE–host–strain evidence](docs/arg-mge-host-strain.md) ·
[References](docs/references.md) ·
[Platforms](docs/multi-platform.md)

---

## Install

### Claude Code

```text
/plugin marketplace add PKU-EMBL/Metagenomics-Skills
/plugin install metagenomics@metagenomics-skills
```

### Codex plugin

```bash
codex plugin marketplace add PKU-EMBL/Metagenomics-Skills
codex plugin add metagenomics@metagenomics-skills
```

### Directory install: Codex / Cursor / Kimi / ZCode / Qwen / Grok / custom agents

```bash
git clone https://github.com/PKU-EMBL/Metagenomics-Skills.git
cd Metagenomics-Skills

# Recommended: compact high-use catalog for Kimi Code, ZCode, and Qwen Code
./scripts/install-platforms.sh --user --profile core kimi zcode qwen

# Shared path for Codex + Kimi + ZCode, plus Qwen native path
./scripts/install-platforms.sh --user --profile core agents qwen

# Or install every skill for every known platform
./scripts/install-platforms.sh --user --profile full all
```

Use `--target PATH` for a new client, `--mode copy` when symlinks are not
supported, `--dry-run` to preview, and `--prune` when switching an existing
destination to a smaller profile. The comprehensive library stays available via
`full`; compact `routing`/`core` and task profiles (`contamination`, `long-read`,
`virome`, `strain-resolved`, `eukaryotic`, `pangenome`,
`metatranscriptomics`, `metabolic-modeling`, `resistome-mobilome`,
`transmission`, and `workflows`) limit loaded
context. See
[the complete platform matrix](docs/multi-platform.md).

---

## Layout

```text
skills/<tool>/SKILL.md       # canonical portable skill
skills/<tool>/references/    # optional progressive detail, kept in-bundle
config/skill-profiles.json   # low-context and task-focused install sets
docs/                        # catalogs, pipeline, agent execution contract
plugin.json                  # portable Agent Plugins v1 package
qwen-extension.json          # Qwen Code extension
.claude-plugin/ .codex-plugin/ .cursor-plugin/ .zcode-plugin/
scripts/install-skills.py    # safe link/copy/custom-target installer
scripts/validate-skills.py   # spec/manifests/profiles/links validator
```

---

## Quick start

Tell the agent whether to **advise**, **plan**, **prepare**, **execute**, or
**review**. It should inspect inputs, preflight tools/databases/resources, pilot,
validate every stage boundary, and report what was actually run. See the
[coding-agent playbook](docs/agent-playbook.md).

> Full genome-resolved path

`study-design` → **QC** (± `multiqc`) → **assembly** → **mapping** →
**binning** (`basalt` recommended) → (± `anvio` / `deepurify`) →
**taxonomy** / **function** → `research-analysis` (`microeco` / `maaslin2` / …)

> Community composition only (no assembly)

**QC** → **taxonomy** (`metaphlan`, `singlem`, or `kraken2`) →
`research-analysis`

> Research stats & figures

`research-analysis` → `multiqc` / `microeco` / `phyloseq` / `visualization` /
`maaslin2` / `ancombc` / `lefse` / `stamp` / `sparcc` / `spieceasi`

> Workflow managers

`nextflow` (± nf-core) · `snakemake`

> Genome-resolved + interactive polish

Auto-bins → `anvio` refine → `checkm2` / `gunc` / `mag-qc` → `gtdbtk`

> Resistome / mobilome / host linkage / HGT

`resistome-analysis` → `rgi` / `amrfinderplus` / `args-oap` / `deeparg` /
`pathofact` · `mobilome-analysis` → `genomad` / `plasx` / `mobmess` ·
`arg-mge-host-linkage` → long-read / Hi-C / CRISPR evidence ·
`horizontal-gene-transfer` → `metachip` / `waafle` / `hgtector` / `gubbins`

> Viral / plasmid / MGE mining

`virome-analysis` → `genomad` / `virsorter2` / `vibrant` → `checkv` →
`votu-workflow` → `vcontact` / `iphop` / `spacepharer` · `mobileog` /
`isescan` / `integronfinder` / `mob-suite` · plasmids: `plasx` / `mobmess` /
`plasmaag` · isolates: `cge-finders` (`staramr` / `abricate` /
`plasmidfinder` → `pmlst` / `mlst`)

> Additional task routes

Contamination: `contamination-control` · long reads: `long-read-qc` · strains:
`strain-resolved-analysis` → `strain-transmission` · typed propagation graphs:
`transfer-network-analysis` · microbial eukaryotes: `eukaryotic-metagenomics` ·
pangenomes: `pangenome-analysis` · RNA: `metatranscriptomics` · community
models: `community-metabolic-modeling` · source attribution: `source-tracking`

> Microbial mining (BGCs / AMR / element cycling / DOM / defense / QS)

After MAGs: `microbial-mining` → `antismash` / `rgi` / `cge-finders` /
`element-cycling` / `dom-biosurfactant` / `dram` / `defensefinder` / `padloc` /
`qsap` / …

> Homology search (Steinegger/Söding · vector DB · compressed genomes)

`homology-search` → `mmseqs2` / `hh-suite` / `foldseek` / `foldmason` /
`plass` / `petasearch` / `erast` / `phylign` / …

> Phylogenomics / trees

`phylogenomics` → `gtdbtk` / `phylophlan` / `unicore` / `iqtree` / `fasttree` /
`lucaphylo`

> Genome language models

`genome-language-model` → `omg` / `nucleotide-transformer` (NTv3) /
`dnabert2` / `caduceus` / `evo2`

> Protein language models

`protein-language-model` → `esm` / `esmc` / `saprot` / `prostt5` /
`plmsearch` / `deepblast`

> AI / LMs & structure search (Foldseek · PLMs)

`metagenomics-llm` → `genome-language-model` / `protein-language-model` /
`foldseek` / `spacedust` / …

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New skills go under `skills/<name>/`
with upstream links and an “Analytical thinking” section. Validate changes with
`python3 scripts/validate-skills.py`.

## License

MIT

## References

Primary literature (Nature-style). Full numbered list:
[docs/references.md](docs/references.md).

1. Qiu, Z. *et al.* BASALT refines binning from metagenomic data and increases resolution of genome-resolved metagenomic analysis. *Nat. Commun.* **15**, 2179 (2024). https://doi.org/10.1038/s41467-024-46539-7

2. Uritskiy, G. V., DiRuggiero, J. & Taylor, J. MetaWRAP—a flexible pipeline for genome-resolved metagenomic data analysis. *Microbiome* **6**, 158 (2018). https://doi.org/10.1186/s40168-018-0541-1

3. Sieber, C. M. K. *et al.* Recovery of genomes from metagenomes via a dereplication, aggregation and scoring strategy. *Nat. Microbiol.* **3**, 836–843 (2018). https://doi.org/10.1038/s41564-018-0171-1

4. Blanco-Míguez, A. *et al.* Extending and improving metagenomic taxonomic profiling with uncharacterized species using MetaPhlAn 4. *Nat. Biotechnol.* **41**, 1633–1644 (2023). https://doi.org/10.1038/s41587-023-01688-w

5. Beghini, F. *et al.* Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife* **10**, e65088 (2021). https://doi.org/10.7554/eLife.65088

6. Almeida, A. *et al.* A unified catalog of 204,938 reference genomes from the human gut microbiome. *Nat. Biotechnol.* **39**, 105–114 (2021). https://doi.org/10.1038/s41587-020-0603-3

7. Parks, D. H. *et al.* A complete domain-to-species taxonomy for Bacteria and Archaea. *Nat. Biotechnol.* **38**, 1079–1086 (2020). https://doi.org/10.1038/s41587-020-0501-8

8. Richardson, L. *et al.* MGnify: the microbiome sequence data analysis resource in 2023. *Nucleic Acids Res.* **51**, D753–D759 (2023). https://doi.org/10.1093/nar/gkac1080

Software repositories and Agent Skills packaging links are listed in
[docs/references.md](docs/references.md) only as implementation pointers; cite the
papers above (plus versions/releases) in manuscripts.
