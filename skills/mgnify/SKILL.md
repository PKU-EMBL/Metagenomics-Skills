---
name: mgnify
description: >
  Use EMBL-EBI MGnify for analysed microbiome studies and biome genome catalogues
  (including UHGG / human-gut and other biomes). Use this skill when: (1) Browsing or
  citing MGnify analyses, (2) Downloading UHGG or other MGnify Genomes catalogues, (3)
  Searching genes/MAGs against catalogues, (4) Building comparison sets for MAG novelty.
  For raw reads use sra-ena. For taxonomy releases use gtdb.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, MGnify, UHGG, genome-catalogue, EBI"
  metagenomics.upstream: "https://github.com/EBI-Metagenomics"
  metagenomics.stage: "taxonomy"
---

# MGnify (incl. UHGG / biome catalogues)

Upstream: https://www.ebi.ac.uk/metagenomics/ ·
Docs: https://docs.mgnify.org/ ·
API: https://www.ebi.ac.uk/metagenomics/api/v1/ ·
Genomes FTP: https://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_genomes/ ·
Org: [EBI-Metagenomics](https://github.com/EBI-Metagenomics)

## Citation

Richardson, L. *et al.* MGnify: the microbiome sequence data analysis resource in 2023. *Nucleic Acids Res.* **51**, D753–D759 (2023). https://doi.org/10.1093/nar/gkac1080

Almeida, A. *et al.* A unified catalog of 204,938 reference genomes from the human gut microbiome. *Nat. Biotechnol.* **39**, 105–114 (2021). https://doi.org/10.1038/s41587-020-0603-3

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

MGnify is **not** a replacement for your pipeline. It is:

1. An archive of **analysed** microbiome runs (taxonomy/function under MGnify’s
   pipeline versions)
2. A set of **biome-specific genome catalogues** (species representatives +
   protein catalogues), e.g. human-gut / UHGG

Use catalogues to **contextualize** your MAGs (novelty, species clusters,
protein families). Do not treat “found in UHGG” as proof of presence in *your*
sample without mapping/abundance evidence (`coverm`, profilers).

Catalogue QC/dereplication rules (CheckM thresholds, dRep ANI) are **theirs** —
state both their criteria and yours (`mag-qc`) when comparing.

## Catalogue family (thinking)

MGnify **Genomes** publishes multiple biome catalogues (human-gut / UHGG is the
most cited; others cover e.g. oceans, various hosts/environments — check the
live FTP/API list). Each catalogue version has its own:

- species-representative set + all-genome metadata
- protein catalogues at several AA identity cutoffs
- sometimes prebuilt search indexes (Kraken2, etc.)

Cross-catalogue rules:

| Claim | Do |
|-------|-----|
| Novelty in human gut | Compare to current UHGG / human-gut catalogue version |
| Non-gut biome | Use the matching biome catalogue, not UHGG alone |
| Global taxonomy | Still run `gtdbtk` on your MAGs; catalogue labels are secondary |
| Presence in *my* sample | Map/profile (`coverm`, MetaPhlAn, …) — catalogue hit ≠ local detection |

MGnify analyses of public studies use **MGnify pipeline versions** — their
taxonomy/function tables are not interchangeable with your MetaPhlAn/HUMAnN
run unless you intentionally reanalyse the same ENA runs.

## Prerequisites

| Need | Resource |
|------|----------|
| Browse studies | MGnify web / API |
| Download MAG catalogue | FTP under `mgnify_genomes/<biome>/<version>/` |
| Gene fragment search | MGnify COBS gene search |
| Whole-MAG similarity | MGnify Sourmash MAG search (`-k 31 --scaled 1000`) |

## How to browse / API

```bash
# List human-gut catalogue metadata (example)
curl -s "https://www.ebi.ac.uk/metagenomics/api/v1/genome-catalogues/human-gut-v2-0-2" \
  | python -m json.tool | head
```

Prefer the live catalogue ID/version from the website or API — do not hardcode
obsolete versions into Methods without checking.

## How to download genome catalogues (FTP)

```bash
# Example layout (pin the version you actually use):
# https://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_genomes/human-gut/<version>/

mkdir -p db/mgnify/human-gut && cd db/mgnify/human-gut
wget -c https://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_genomes/human-gut/v2.0.2/genomes-all_metadata.tsv
# species_catalogue/, protein_catalogue/, optional kraken2_db_* when published
```

Typical contents: species representatives, all-genomes metadata, protein
catalogues (100/95/90/50% AA), sometimes prebuilt Kraken2 indexes.

## Key thinking for MAG studies

| Task | Approach |
|------|----------|
| Is my MAG a known gut species? | Sourmash/Mash vs UHGG reps; or GTDB + literature |
| Cross-biome claim | Search the matching MGnify biome catalogue, not only human-gut |
| Functional comparison | Use protein catalogues carefully — AAI cutoffs change interpretation |
| Cite correctly | Catalogue name + version + FTP path + download date |

## Decision tree

```text
MGnify vs other public resources?
├─ Need raw FASTQ → sra-ena (MGnify often links ENA accessions)
├─ Need biome MAG / protein catalogue → mgnify
├─ Need global prokaryotic taxonomy release → gtdb
└─ Need marker/pathway indexes for profiling → biobakery-databases
```

## Related skills

`public-databases` · `sra-ena` · `gtdb` · `progenomes` · `cami` · `drep` · `coverm` · `gtdbtk` · `mag-qc` · `visualization`
