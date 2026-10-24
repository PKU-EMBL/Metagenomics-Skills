---
name: cami
description: >
  CAMI / CAMI II metagenome benchmarking datasets and evaluation stack (CAMISIM, AMBER,
  OPAL, CAMI Benchmarking Portal). Use when: (1) Downloading CAMI challenge data / gold
  standards, (2) Choosing marine, plant-associated, strain-madness, mouse-gut, or human
  toy sets, (3) Evaluating binners with AMBER or profilers with OPAL, (4) Simulating
  communities with CAMISIM, (5) Citing CAMI results in Methods without over-generalizing
  to new biomes. For real-world public reads use sra-ena; for biome MAG catalogues use
  mgnify.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "CAMI, CAMI2, benchmark, AMBER, OPAL, CAMISIM, gold-standard"
  metagenomics.upstream: "https://cami-challenge.org/"
  metagenomics.stage: "assessment"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "AMBER 2.0.8; OPAL 1.0.14; CAMISIM 2.0.1"
  metagenomics.command-status: "download and current AMBER/OPAL interfaces statically reviewed; benchmark runs not executed here"
---

# CAMI (Critical Assessment of Metagenome Interpretation)

Portal: https://cami-challenge.org/ ·
Data: https://data.cami-challenge.org/ ·
GitHub org: [CAMI-challenge](https://github.com/CAMI-challenge) ·
Benchmarking portal paper / server: see References

## Citation

Sczyrba, A. *et al.* Critical Assessment of Metagenome Interpretation—a benchmark
of metagenomics software. *Nat. Methods* **14**, 1063–1071 (2017).
https://doi.org/10.1038/nmeth.4458

Meyer, F. *et al.* Critical Assessment of Metagenome Interpretation: the second
round of challenges. *Nat. Methods* **19**, 429–440 (2022).
https://doi.org/10.1038/s41592-022-01431-4

Fritz, A. *et al.* CAMISIM: simulating metagenomes and microbial communities.
*Microbiome* **7**, 17 (2019). https://doi.org/10.1186/s40168-019-0633-6

Meyer, F. *et al.* AMBER: Assessment of Metagenome BinnERs. *GigaScience* **7**,
giy069 (2018). https://doi.org/10.1093/gigascience/giy069

Meyer, F. *et al.* Assessing taxonomic metagenome profilers with OPAL.
*Genome Biol.* **20**, 51 (2019). https://doi.org/10.1186/s13059-019-1646-y

Meyer, F. *et al.* CAMI Benchmarking Portal: online evaluation and ranking of
metagenomic software. *Nucleic Acids Res.* **53**, W102–W109 (2025).
https://doi.org/10.1093/nar/gkaf369

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md) and
[docs/public-databases.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/public-databases.md).

## Analytical thinking

CAMI is a **community benchmarking initiative**, not a natural biome catalogue.
Datasets are computationally constructed (often via CAMISIM) with **gold
standards** for assembly, genome binning, taxonomic binning, and profiling.

Use CAMI when you need:

| Goal | Resource |
|------|----------|
| Compare assemblers / binners / profilers under controlled truth | CAMI / CAMI II challenge data |
| Generate custom gold-standard simulations | `CAMISIM` |
| Lightweight Illumina read simulation | `insilicoseq` |
| Score genome bins vs gold | `AMBER` |
| Score taxonomic profiles vs gold | `OPAL` |
| Submit / browse rankings | CAMI Benchmarking Portal |

Do **not** treat CAMI rankings as a universal ordering for your soil/gut/reactor
study — CAMI II still found related strains hard for assembly/binning, and
viruses/Archaea underperformed for many profilers/binners. Cite the **dataset
name** (e.g. plant-associated, strain-madness, marine, mouse gut) you actually ran.

Abundance caveat (Sun *et al.*, *Nat. Methods* 2021): profilers report
**sequence abundance** vs **taxonomic abundance** — do not mix them when
scoring with OPAL or comparing MetaPhlAn vs Kraken.

## Dataset layers

```text
CAMISIM / community design
        ↓
short- and/or long-read metagenomes (+ multi-sample designs)
        ↓
gold standards (assembly / genome binning / tax. binning / profiling)
        ↓
your tool outputs (bioboxes / CAMI formats)
        ↓
AMBER (bins) · OPAL (profiles) · portal rankings
```

CAMI II scale (paper): ~1,700 genomes + ~600 plasmids/viruses; short + long
reads; thousands of submitted results across dozens of program versions.

## How to obtain data

Prefer the live portal paths over inventing FTP URLs:

```text
https://cami-challenge.org/
https://data.cami-challenge.org/participate
```

CAMI II challenge / exemplary datasets were also deposited with PUBLISSO DOIs
(marine, strain-madness, plant-associated, mouse gut, human) — resolve from the
CAMI II paper Data availability / portal, then pin the DOI + download date.

Resolve the immutable archive URL and dataset identifier from the portal/DOI before running:

```bash
set -euo pipefail
dataset_id=${CAMI_DATASET_ID:?set the portal/DOI dataset identifier}
source_url=${CAMI_SOURCE_URL:?set an immutable portal or DOI archive URL}
root=${CAMI_DOWNLOAD_DIR:-db/cami/$dataset_id}
[[ "$dataset_id" =~ ^[A-Za-z0-9._-]+$ ]] || exit 2
[[ ! -e "$root" ]] || { echo "refusing to overwrite: $root" >&2; exit 3; }
mkdir -p "$root/source" "$root/logs" "$root/provenance"
curl --fail --location --retry 3 --dump-header "$root/provenance/headers.txt" \
  "$source_url" --output "$root/source/source.archive" \
  2>"$root/logs/download.log"
test -s "$root/source/source.archive"
file "$root/source/source.archive" >"$root/provenance/file-type.txt"
sha256sum "$root/source/source.archive" >"$root/provenance/source.sha256"
printf 'dataset_id\turl\tretrieved_utc\n%s\t%s\t%s\n' \
  "$dataset_id" "$source_url" "$(date -u +%FT%TZ)" \
  >"$root/provenance/download.tsv"
```

Extract into a new directory and inventory reads, assemblies, gold standards, taxonomy snapshot and expected checksums; never overwrite the source archive.

## Evaluation tools

| Tool | Upstream | Use |
|------|----------|-----|
| CAMISIM | https://github.com/CAMI-challenge/CAMISIM | Simulate communities + gold standards |
| AMBER | https://github.com/CAMI-challenge/AMBER | Assess genome binners |
| OPAL | https://github.com/CAMI-challenge/OPAL | Assess taxonomic profilers |
| Portal | https://cami-challenge.org/ | Online evaluation / ranking |

AMBER genome-binning assessment:

```bash
set -euo pipefail
gold=${CAMI_GOLD_BINNING:?set gold-standard Bioboxes mapping}
pred=${CAMI_PRED_BINNING:?set candidate Bioboxes mapping}
run=${CAMI_AMBER_RUN:?set a fresh result directory}
[[ -s "$gold" && -s "$pred" ]] || exit 2
[[ ! -e "$run" ]] || { echo "refusing to overwrite: $run" >&2; exit 3; }
mkdir -p "$run/logs" "$run/provenance"
grep -q '^@SampleID:' "$gold"; grep -q '^@SampleID:' "$pred"
amber.py --version >"$run/provenance/amber.version.txt" 2>&1
sha256sum "$gold" "$pred" >"$run/provenance/inputs.sha256"
amber.py -g "$gold" -l "candidate" "$pred" -o "$run/amber" --stdout \
  >"$run/logs/stdout.log" 2>"$run/logs/stderr.log"
find "$run/amber" -type f -size +0c -print -quit | grep -q .
! grep -Rqi 'traceback' "$run/logs"
```

OPAL taxonomic-profile assessment:

```bash
set -euo pipefail
gold=${CAMI_GOLD_PROFILE:?set gold-standard CAMI profile}
pred=${CAMI_PRED_PROFILE:?set candidate CAMI profile}
run=${CAMI_OPAL_RUN:?set a fresh result directory}
[[ -s "$gold" && -s "$pred" ]] || exit 2
[[ ! -e "$run" ]] || { echo "refusing to overwrite: $run" >&2; exit 3; }
mkdir -p "$run/logs" "$run/provenance"
grep -q '^@SampleID:' "$gold"; grep -q '^@SampleID:' "$pred"
opal.py --version >"$run/provenance/opal.version.txt" 2>&1
sha256sum "$gold" "$pred" >"$run/provenance/inputs.sha256"
opal.py -g "$gold" -l "candidate" "$pred" -o "$run/opal" \
  >"$run/logs/stdout.log" 2>"$run/logs/stderr.log"
find "$run/opal" -type f -size +0c -print -quit | grep -q .
! grep -Rqi 'traceback' "$run/logs"
```

Inputs must use the correct CAMI Bioboxes format and SampleID. For taxonomic binning, also pin the NCBI taxonomy dump passed with `--ncbi_dir`; do not use it for genome-binning metrics.

Use CAMI **bioboxes / profiling formats** when possible so AMBER/OPAL/portal
can ingest outputs without custom parsers.

## Decision tree

```text
Need public metagenome *data*?
├─ Controlled benchmark with gold standards → cami (this skill)
├─ Simulate custom communities → CAMISIM (this skill)
├─ Real environmental/clinical reads → sra-ena (± mgnify analysed studies)
├─ Biome MAG / protein catalogues → mgnify
└─ Rank-normalized prokaryotic taxonomy release → gtdb
```

## Methods caveats

1. Report CAMI challenge round + dataset ID + gold-standard version
2. Separate short-read vs long-read vs hybrid results
3. Do not equate CAMI “best tool” with production defaults for all biomes
4. Keep sequence- vs taxonomic-abundance definitions explicit in profiler benchmarks
5. Reference DBs frozen for a challenge (e.g. RefSeq snapshot dates) ≠ today’s GTDB/MGnify

## Validation, recovery, and provenance

Before scoring, reconcile sequence IDs and SampleIDs, confirm the challenge task,
read technology, taxonomy snapshot, abundance definition and any filtering. Report
all native metrics, not only a composite rank; retain unassigned sequences/taxa,
zero predictions and tool failures. Compare methods on identical gold-standard
units and resources, and use biological replicates or multiple simulations when
making general performance claims.

A failed archive download may be resumed only against the same immutable URL;
verify the completed digest. Rerun AMBER/OPAL into a fresh directory after any
input, taxonomy, label, filter or version change. Archive challenge/dataset and
gold-standard IDs, DOI/URL, retrieval headers/date/checksum, software/container
versions, taxonomy dump, exact commands/logs, resource use and complete outputs.
A locally calculated hash is a fingerprint, not a publisher checksum.

## Related skills

`insilicoseq` · `public-databases` · `sra-ena` · `mgnify` · `gtdb` · `quast` · `metabat2` ·
`basalt` · `metaphlan` · `kraken2` · `tool-selection` · `study-design`
