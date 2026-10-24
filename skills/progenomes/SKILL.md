---
name: progenomes
description: >
  proGenomes4 — nearly 2 million consistently QC'd and annotated high-quality
  prokaryotic genomes with habitat metadata, pan-genomes, MGE/BGC annotations. Use when:
  (1) Building large microbial genome reference sets, (2) Comparative genomics /
  pan-genome analyses, (3) Selecting habitat-filtered genome cohorts, (4) Distinguishing
  proGenomes from GTDB reps or MGnify biome catalogues. For taxonomy releases use gtdb.
  For biome MAG catalogues use mgnify.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, proGenomes, genomes, pan-genome, EMBL"
  metagenomics.upstream: "https://progenomes.embl.de/"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "proGenomes4"
  metagenomics.command-status: "metadata download template smoke-tested with the pg4 consensus GTDB taxonomy asset; large sequence assets not downloaded"
---

# proGenomes

Portal: https://progenomes.embl.de/

## Citation

Fullam, A. *et al.* proGenomes4: providing 2 million accurately and consistently
annotated high-quality prokaryotic genomes. *Nucleic Acids Res.* (2025).
https://doi.org/10.1093/nar/gkaf1208

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

proGenomes is a **genome warehouse** with uniform QC and multi-workflow
functional annotation (including MGE and BGC calls), habitat metadata, and
precomputed pan-genomes — ~2M genomes / >7B genes / ~33k species in v4.

| Resource | Primary question |
|----------|------------------|
| `progenomes` | Large consistently annotated prokaryotic genome set |
| `gtdb` | Rank-normalized taxonomy + species clusters / reps |
| `mgnify` | Biome-specific MAG/protein catalogues + analysed studies |
| `sra-ena` | Raw sequencing runs |

Do not assume proGenomes species IDs == GTDB species clusters without mapping.
For MAG novelty in a biome, still use the matching MGnify catalogue + GTDB-Tk.

## How to access

Browse the v4 download page and estimate storage before choosing an asset; the
all-representative genome FASTA is tens of GB compressed. A small metadata asset
can be acquired reproducibly as follows:

```bash
set -euo pipefail
asset=pg4_consensus_gtdb_taxonomy_per_ani_cluster.tsv.gz
url="https://progenomes.embl.de/data/$asset"
out=${PROGENOMES_DIR:?set a fresh proGenomes4 output directory}
[[ ! -e "$out" ]] || { echo "refusing to overwrite: $out" >&2; exit 2; }
mkdir -p "$out/logs" "$out/provenance" "$out/data"
curl --fail --location --retry 3 --dump-header "$out/provenance/headers.txt" \
  "$url" --output "$out/data/$asset" 2>"$out/logs/download.log"
gzip -t "$out/data/$asset"
python3 - "$out/data/$asset" "$out/provenance/content-stats.tsv" <<'PY'
import gzip, sys
path, report = sys.argv[1:]
with gzip.open(path, "rt") as handle:
    header = handle.readline().rstrip("\n")
    if "\t" not in header:
        raise SystemExit("expected a tabular header")
    rows = sum(1 for line in handle if line.strip())
if rows == 0:
    raise SystemExit("empty table")
open(report, "w").write(f"header\t{header}\nrecords\t{rows}\n")
PY
sha256sum "$out/data/$asset" >"$out/provenance/local.sha256"
printf 'release\tasset\turl\tretrieved_utc\nproGenomes4\t%s\t%s\t%s\n' \
  "$asset" "$url" "$(date -u +%FT%TZ)" >"$out/provenance/download.tsv"
```

Archive release ID, exact asset URL and HTTP headers, genome filters (quality,
habitat, representative/all), annotation workflow names and retrieval date. A
local SHA-256 is a rerun fingerprint, not an upstream integrity guarantee.

## Decision tree

```text
Need many annotated prokaryotic genomes?
├─ Habitat-aware / pan-genome / consistent annotation → progenomes
├─ Taxonomy placement of *my* MAGs → gtdbtk + gtdb
├─ Human-gut (or other biome) species catalogue → mgnify
└─ Benchmark with gold standards → cami
```

## Validation, recovery, and provenance

For FASTA assets, test compression, unique IDs, sequence alphabet, record counts
and metadata joins. For cohort construction, retain included and excluded genome
IDs with reasons, QC fields, habitat ontology, ANI-cluster membership and one-to-
one/many taxonomy mappings. Check for isolate/MAG duplication, sampling bias and
train/test overlap before comparative or ML work. Do not equate habitat labels,
annotation calls or cluster representatives with observations in your sample.

Resume only the same URL into the same partial file, then repeat compression and
content checks. Use a fresh directory when release, asset, filter or annotation
version changes. Record release/paper, URL/headers/date, local and publisher
checksums when available, selection script/parameters, taxonomy mappings,
software/container versions and resulting cohort manifests.

## Related skills

`public-databases` · `gtdb` · `mgnify` · `gtdbtk` · `antismash` · `genomad` ·
`eggnog-mapper` · `kegg`
