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
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "API and UHGG v2.0.2 archive paths verified live; no catalogue-scale download executed"
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
set -Eeuo pipefail
catalogue="${MGNIFY_CATALOGUE:-human-gut-v2-0-2}"
out="metadata/mgnify/$catalogue"
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
url="https://www.ebi.ac.uk/metagenomics/api/v1/genome-catalogues/$catalogue"
curl --fail --location --retry 3 "$url" -o "$out/api.json" \
  2>"$out/curl.stderr.log"
python3 -m json.tool "$out/api.json" >"$out/api.pretty.json"
python3 - "$out/api.json" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)["data"]
assert data["id"] and data["attributes"]["name"]
print(data["id"], data["attributes"]["name"])
PY
```

Prefer the live catalogue ID/version from the website or API, then freeze it in
the analysis manifest.

## How to download genome catalogues (FTP)

```bash
set -Eeuo pipefail
version="${MGNIFY_VERSION:-v2.0.2}"
out="db/mgnify/human-gut/$version"
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
base="https://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_genomes/human-gut/$version"
for file in "README_${version#v}.txt" genomes-all_metadata.tsv; do
  curl --fail --location --retry 3 "$base/$file" -o "$out/$file" \
    2>>"$out/download.stderr.log"
done
sha256sum "$out"/* >"$out/SHA256SUMS.local"
```

Inspect the live directory before large transfers. `species_catalogue/`,
`protein_catalogue/`, Sourmash, and Kraken2 assets can be much larger and have
separate semantics.

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

## Validation, recovery, and provenance

Validate API type/ID, catalogue README, metadata header and unique genome IDs,
file sizes/checksums, biome/version, taxonomy release, species-representative
mapping, and published QC/dereplication rules. Reconcile every downloaded asset
to the directory listing; do not treat a partial transfer as a complete catalogue.

Archive catalogue ID/name/version, API response, FTP URLs, access date, README,
checksums, parsing code, and selected reference manifest. Report whether matches
are genome similarity, protein-family similarity, or read recruitment. A
catalogue match contextualizes novelty; it does not prove presence in the study
sample.

## Related skills

`public-databases` · `sra-ena` · `gtdb` · `progenomes` · `cami` · `drep` ·
`coverm` · `gtdbtk` · `mag-qc` · `visualization`
