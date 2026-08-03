# Metagenomics Skills

Agent Skills for shotgun metagenomics, organized by scientific stage:

**QC → assembly → mapping → binning → taxonomy → function → microbial mining**

One skill per core tool (mappers, assemblers, binners, profilers, miners such as
antiSMASH / geNomad / DRAM, …) plus databases, orchestration, and visualization.

[Getting started](docs/getting-started.md) ·
[Skills](docs/skills.md) ·
[Pipeline](docs/standard-pipeline.md) ·
[Public databases](docs/public-databases.md) ·
[References](docs/references.md) ·
[Platforms](docs/multi-platform.md)

---

## Install

### Claude Code

```text
/plugin marketplace add PKU-EMBL/Metagenomics-Skills
/plugin install metagenomics@metagenomics-skills
```

### Codex / Cursor / Kimi / Grok

```bash
git clone https://github.com/PKU-EMBL/Metagenomics-Skills.git
cd Metagenomics-Skills
./scripts/install-platforms.sh --user all
```

→ [docs/multi-platform.md](docs/multi-platform.md)

---

## Layout

```text
skills/<tool>/SKILL.md     # per-software / per-database + analytical thinking
skills/<tool>/references/  # optional deep detail inside that skill only
docs/                      # stage catalogs and pipelines
.claude-plugin/ .codex-plugin/ .cursor-plugin/
scripts/install-platforms.sh
```

---

## Quick start

> Full genome-resolved path

`study-design` → **QC** → **assembly** → **mapping** → **binning** (`basalt`
recommended) → (± `anvio` / `deepurify`) → **taxonomy** / **function** →
`visualization`

> Community composition only (no assembly)

**QC** → **taxonomy** (`metaphlan`, `singlem`, or `kraken2`) → `visualization`

> Genome-resolved + interactive polish

Auto-bins → `anvio` refine → `checkm2` / `gunc` / `mag-qc` → `gtdbtk`

> Viral / plasmid mining

Contigs → `genomad` / `virsorter2` → `checkv` → `vcontact` · plasmids:
`plasmaag`

> Microbial mining (BGCs / AMR / metabolism)

After MAGs: `microbial-mining` → `antismash` / `rgi` / `dram` / …

> Homology search (sequence · structure · vector DB · compressed genomes)

`homology-search` → `mmseqs2` / `foldseek` / `erast` / `phylign` / `lexicmap` / …

> Phylogenomics / trees

`phylogenomics` → `gtdbtk` / `phylophlan` / `iqtree` / `fasttree` / `lucaphylo`

> AI / LMs & structure search (MMseqs2 · Foldseek · Folddisco · PLMs)

`metagenomics-llm` → `mmseqs2` / `foldseek` / `folddisco` / `omg` /
`plmsearch` / `deepblast` / `spacedust` / …

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New skills go under `skills/<name>/`
with upstream links and an “Analytical thinking” section.

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