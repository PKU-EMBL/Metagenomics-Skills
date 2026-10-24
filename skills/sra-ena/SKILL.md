---
name: sra-ena
description: >
  Fetch and cite public shotgun metagenomic reads from NCBI SRA and EBI ENA. Use this
  skill when: (1) Downloading public metagenomes by SRR/ERR/DRR, (2) Resolving
  BioProject/Study accessions, (3) Choosing fasterq-dump vs ena-ftp / Aspera, (4)
  Building manifests for reanalysis. For analysed microbiome studies and MAG catalogues,
  use mgnify. For database routing, use public-databases.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, SRA, ENA, download, reanalysis"
  metagenomics.upstream: "https://github.com/ncbi/sra-tools"
  metagenomics.stage: "utilities"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "SRA Toolkit 3.4.1; ENA Portal API"
  metagenomics.command-status: "ENA template smoke-tested on one single- and one paired-end run; SRA Toolkit path statically reviewed, not executed here"
---

# NCBI SRA / EBI ENA

Upstream: [ncbi/sra-tools](https://github.com/ncbi/sra-tools) ·
ENA: https://www.ebi.ac.uk/ena ·
NCBI SRA: https://www.ncbi.nlm.nih.gov/sra

## Analytical thinking

SRA/ENA hold **raw (or submitted) sequencing data**, not polished community
tables. Reanalysis still requires your own QC (`fastp`, `kneaddata`) — public
“clean” claims are not transferable without provenance.

Prefer ENA FTP/Aspera for large European-hosted studies when NCBI is slow;
prefer `fasterq-dump` when you already live in the SRA Toolkit ecosystem.
Always map **Study / BioProject → Sample → Run** before bulk download so PE
pairs and metadata stay aligned.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Accession | SRR/ERR/DRR or BioProject | Manifest TSV with sample IDs |
| Tooling | `prefetch` + `fasterq-dump` **or** `wget`/`curl` ENA FTP | `ascp` for large cohorts |
| Disk | Check run size before download | ~8–10× compressed size for `fasterq-dump` scratch |

## How to run (SRA Toolkit)

Resolve run layout/metadata first. The SRA path below uses `fasterq-dump`'s
default split-3 behavior, preserving paired mates as `_1`/`_2` and any unpaired
reads in the unsuffixed FASTQ.

```bash
set -euo pipefail
run=${1:?usage: sra-download.sh SRR_OR_ERR_OR_DRR FRESH_RUN_DIR}
root=${2:?usage: sra-download.sh SRR_OR_ERR_OR_DRR FRESH_RUN_DIR}
[[ "$run" =~ ^(SRR|ERR|DRR)[0-9]+$ ]] || exit 2
[[ ! -e "$root" ]] || { echo "refusing to overwrite: $root" >&2; exit 3; }
mkdir -p "$root/sra" "$root/fastq" "$root/tmp" "$root/logs" "$root/provenance"
root=$(cd "$root" && pwd)
prefetch --version >"$root/provenance/sra-tools.version.txt" 2>&1
printf 'run\tmax_size\tretrieved_utc\n%s\t%s\t%s\n' \
  "$run" "${SRA_MAX_SIZE:-100g}" "$(date -u +%FT%TZ)" \
  >"$root/provenance/request.tsv"
prefetch "$run" -O "$root/sra/$run" --max-size "${SRA_MAX_SIZE:-100g}" \
  >"$root/logs/prefetch.stdout.log" 2>"$root/logs/prefetch.stderr.log"
vdb-validate "$root/sra/$run" \
  >"$root/logs/vdb-validate.stdout.log" 2>"$root/logs/vdb-validate.stderr.log"
(
  cd "$root/sra"
  fasterq-dump "$run" --threads 8 --outdir "$root/fastq" --temp "$root/tmp"
) >"$root/logs/fasterq.stdout.log" 2>"$root/logs/fasterq.stderr.log"
shopt -s nullglob
fastqs=("$root"/fastq/*.fastq)
((${#fastqs[@]} > 0)) || exit 4
gzip -n "${fastqs[@]}"
python3 - "$root/fastq" "$root/provenance/read-counts.tsv" <<'PY'
import gzip, pathlib, sys
folder, report = pathlib.Path(sys.argv[1]), sys.argv[2]
counts = {}
for path in sorted(folder.glob("*.fastq.gz")):
    with gzip.open(path, "rb") as handle:
        lines = sum(1 for _ in handle)
    if lines == 0 or lines % 4:
        raise SystemExit(f"invalid FASTQ line count: {path}")
    counts[path.name] = lines // 4
r1 = [n for n in counts if n.endswith("_1.fastq.gz")]
r2 = [n for n in counts if n.endswith("_2.fastq.gz")]
if bool(r1) != bool(r2) or len(r1) > 1 or len(r2) > 1:
    raise SystemExit("incomplete or ambiguous mate files")
if r1 and counts[r1[0]] != counts[r2[0]]:
    raise SystemExit("R1/R2 read counts differ")
with open(report, "w") as out:
    out.write("file\treads\n")
    for name, count in counts.items(): out.write(f"{name}\t{count}\n")
PY
sha256sum "$root"/fastq/*.fastq.gz >"$root/provenance/fastq.sha256"
```

Plan scratch space before conversion; `fasterq-dump` can require much more than
the final compressed FASTQ size. Compare observed files with the declared library
layout and retain the unsuffixed singleton file rather than silently discarding it.

## How to run (ENA-resolved links)

This path downloads the ENA `fastq_ftp` representation. Audit whether the study
requires original submitted files instead, and do not mix representations within
a comparison without labeling them.

```bash
set -euo pipefail
run=${1:?usage: ena-download.sh SRR_OR_ERR_OR_DRR FRESH_RUN_DIR}
root=${2:?usage: ena-download.sh SRR_OR_ERR_OR_DRR FRESH_RUN_DIR}
[[ "$run" =~ ^(SRR|ERR|DRR)[0-9]+$ ]] || exit 2
[[ ! -e "$root" ]] || { echo "refusing to overwrite: $root" >&2; exit 3; }
mkdir -p "$root/metadata" "$root/fastq" "$root/logs" "$root/provenance"
api='https://www.ebi.ac.uk/ena/portal/api/filereport'
curl --fail --silent --show-error --location --retry 3 --get "$api" \
  --data-urlencode "accession=$run" --data-urlencode 'result=read_run' \
  --data-urlencode 'fields=run_accession,sample_accession,study_accession,library_layout,instrument_platform,instrument_model,fastq_ftp,fastq_md5,fastq_bytes' \
  --data-urlencode 'format=tsv' --data-urlencode 'download=true' \
  --dump-header "$root/provenance/ena.headers" \
  -o "$root/metadata/${run}.ena.tsv" 2>"$root/logs/ena-api.log"
[[ $(wc -l < "$root/metadata/${run}.ena.tsv") -eq 2 ]] || exit 4
python3 - "$root/metadata/${run}.ena.tsv" "$root/metadata/files.tsv" \
  "$root/metadata/run.tsv" <<'PY'
import csv, pathlib, sys, urllib.parse
source, files_out, run_out = sys.argv[1:]
with open(source, newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
if len(rows) != 1:
    raise SystemExit("expected exactly one ENA run row")
r = rows[0]
urls = [x for x in r["fastq_ftp"].split(";") if x]
md5s = [x for x in r["fastq_md5"].split(";") if x]
sizes = [x for x in r["fastq_bytes"].split(";") if x]
if not urls or len(urls) != len(md5s) or len(urls) != len(sizes):
    raise SystemExit("missing or non-position-matched ENA FASTQ metadata")
with open(files_out, "w", newline="") as out:
    w = csv.writer(out, delimiter="\t", lineterminator="\n")
    w.writerow(["remote", "md5", "bytes", "filename"])
    for url, md5, size in zip(urls, md5s, sizes):
        parsed = urllib.parse.urlsplit(url if "://" in url else "https://" + url)
        name = pathlib.PurePosixPath(parsed.path).name
        if not name or "/" in name: raise SystemExit("unsafe filename")
        w.writerow([url, md5, size, name])
with open(run_out, "w", newline="") as out:
    keys = ["run_accession", "sample_accession", "study_accession", "library_layout", "instrument_platform", "instrument_model"]
    w = csv.writer(out, delimiter="\t", lineterminator="\n")
    w.writerow(keys); w.writerow([r.get(k, "") for k in keys])
PY
while IFS=$'\t' read -r remote expected_md5 expected_bytes filename; do
  [[ "$remote" == remote ]] && continue
  case "$remote" in
    ftp://*) url="https://${remote#ftp://}" ;;
    https://*) url="$remote" ;;
    *) url="https://$remote" ;;
  esac
  curl --fail --location --retry 3 --continue-at - "$url" \
    --output "$root/fastq/$filename" 2>>"$root/logs/download.log"
  [[ $(wc -c < "$root/fastq/$filename") -eq "$expected_bytes" ]]
  printf '%s  %s\n' "$expected_md5" "$root/fastq/$filename" | \
    md5sum -c - >>"$root/logs/md5.log"
  gzip -t "$root/fastq/$filename"
done <"$root/metadata/files.tsv"
python3 - "$root/metadata/files.tsv" "$root/metadata/run.tsv" \
  "$root/fastq" "$root/provenance/read-counts.tsv" <<'PY'
import csv, gzip, pathlib, sys
files_tsv, run_tsv, folder, report = sys.argv[1:]
files = list(csv.DictReader(open(files_tsv), delimiter="\t"))
run = next(csv.DictReader(open(run_tsv), delimiter="\t"))
counts = {}
for row in files:
    path = pathlib.Path(folder) / row["filename"]
    with gzip.open(path, "rb") as handle: lines = sum(1 for _ in handle)
    if lines == 0 or lines % 4: raise SystemExit(f"invalid FASTQ: {path}")
    counts[path.name] = lines // 4
if run["library_layout"] == "PAIRED":
    r1 = [n for n in counts if n.endswith("_1.fastq.gz")]
    r2 = [n for n in counts if n.endswith("_2.fastq.gz")]
    if len(r1) != 1 or len(r2) != 1 or counts[r1[0]] != counts[r2[0]]:
        raise SystemExit("ENA paired files missing, ambiguous, or count-mismatched")
with open(report, "w") as out:
    out.write("file\treads\n")
    for name, count in counts.items(): out.write(f"{name}\t{count}\n")
PY
sha256sum "$root/metadata/${run}.ena.tsv" "$root"/fastq/* \
  >"$root/provenance/local.sha256"
```

The ENA template requires GNU `md5sum`; use the platform-equivalent checker if
needed. It position-matches URL, MD5 and byte-count lists before download. An HTTP
success or locally computed SHA-256 alone is not publisher-integrity evidence.

## Key metadata to archive

| Field | Why |
|-------|-----|
| Run accession | Primary download key |
| BioSample / Sample | Biological unit |
| BioProject / Study | Cohort identity |
| Instrument / layout | PE vs SE; chemistry |
| Spot/bases | Depth sanity check |
| Download date + MD5 | Provenance |

## Decision tree

```text
Public data needed?
├─ Raw reads for reanalysis → sra-ena
├─ Pre-analysed MGnify study / biome MAG catalogue → mgnify
└─ Reference taxonomy genomes → gtdb
```

## Validation, recovery, and provenance

Before cohort download, freeze the Study→Sample→Run table and audit consent/data
use, assay, layout, instrument, insert size, spot/base counts, controls, biological
replicates and duplicate samples. After download, verify publisher MD5/bytes,
compression, FASTQ structure, expected layout, matched mate counts and one output
manifest row per run. Preserve failed, withdrawn, single-end, singleton and
technical-read states explicitly; do not coerce them into paired samples.

`prefetch` and `curl --continue-at -` may resume only the same accession/file;
after completion repeat VDB or MD5 validation. If conversion fails, retain the
validated SRA source, remove partial FASTQ/temp files and rerun conversion. Use a
fresh run directory when toolkit options or source files change. Archive query
response and date, run/sample/study mapping, submitted/generated FASTQ choice,
SRA Toolkit version/config or ENA endpoint, publisher MD5/bytes, local hashes,
commands/logs, observed counts/layout and downstream sample-name mapping.

## Related skills

`public-databases` · `mgnify` · `study-design` · `fastp` · `kneaddata` · `setup`
