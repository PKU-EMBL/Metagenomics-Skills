---
name: kegg
description: >
  KEGG as a reference for gene/protein annotation — KO orthologs, pathways, modules,
  BRITE (BlastKOALA / GhostKOALA and related assignment). Use when: (1) Mapping
  genes/MAGs to KEGG Orthology, (2) Reconstructing pathways/modules, (3) Choosing KEGG
  vs eggNOG / MetaCyc / DRAM distillation, (4) Citing KEGG releases in Methods.
  Licensing/access constraints apply for bulk use — verify institutional rights. For
  eggNOG use eggnog-mapper. For pathway abundance from reads use humann.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, KEGG, KO, pathway, annotation"
  metagenomics.upstream: "https://www.kegg.jp/"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "targeted REST template smoke-tested with K00001 and a no-hit query; bulk assets and KO assignment remain access-dependent"
---

# KEGG (Kyoto Encyclopedia of Genes and Genomes)

Portal: https://www.kegg.jp/ · https://www.genome.jp/kegg/

## Citation

Kanehisa, M., Sato, Y., Kawashima, M., Furumichi, M. & Tanabe, M. KEGG as a
reference resource for gene and protein annotation. *Nucleic Acids Res.* **44**,
D457–D462 (2016). https://doi.org/10.1093/nar/gkv1070

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

KEGG links genes to **high-level functions** via KO (K numbers) → PATHWAY /
MODULE / BRITE networks. In shotgun workflows it appears as:

| Path | Typical tools |
|------|----------------|
| Gene → KO assignment | BlastKOALA / GhostKOALA / KofamKOALA; or via eggNOG-mapper KEGG fields |
| Pathway abundance from reads | Often MetaCyc via `humann` (not raw KEGG API) |
| Distilled metabolism tables | `dram` (multi-DB including KEGG-related sources) |

Hard rules:

1. **License / redistributability** — KEGG is not a free-for-all dump; confirm
   access rights before bulk downloads or redistributing KO databases.
2. Pin KEGG / KOALA DB versions next to software versions.
3. Pathway presence from incomplete MAGs ≠ organism capability proof.
4. Do not merge HUMAnN MetaCyc pathway names with KEGG map IDs unlabeled.

## Targeted REST retrieval

Use the REST API for small, identified queries, not as a substitute for licensed
bulk assets. This template preserves a no-hit response:

```bash
set -euo pipefail
ko=${1:?usage: kegg-ko.sh K00001 FRESH_OUTPUT_DIR}
out=${2:?usage: kegg-ko.sh K00001 FRESH_OUTPUT_DIR}
[[ "$ko" =~ ^K[0-9]{5}$ ]] || exit 2
[[ ! -e "$out" ]] || { echo "refusing to overwrite: $out" >&2; exit 3; }
mkdir -p "$out/logs" "$out/provenance"
curl --fail --silent --show-error --location --retry 3 \
  'https://rest.kegg.jp/info/kegg' -o "$out/provenance/kegg-info.txt" \
  2>"$out/logs/curl.log"
http=$(curl --silent --show-error --location --retry 3 \
  --dump-header "$out/provenance/response.headers" \
  --output "$out/${ko}.txt" --write-out '%{http_code}' \
  "https://rest.kegg.jp/get/$ko" 2>>"$out/logs/curl.log")
printf 'ko\thttp_status\tretrieved_utc\n%s\t%s\t%s\n' \
  "$ko" "$http" "$(date -u +%FT%TZ)" >"$out/provenance/request.tsv"
if [[ "$http" == 404 ]]; then
  printf 'query\tstatus\n%s\tno_hit\n' "$ko" >"$out/no-hit.tsv"
elif [[ "$http" == 200 ]]; then
  grep -Eq "^ENTRY +${ko}([[:space:]]|$)" "$out/${ko}.txt"
  sha256sum "$out/${ko}.txt" >"$out/provenance/response.sha256"
else
  echo "unexpected HTTP status: $http" >&2; exit 4
fi
```

For KO assignment, retain query-to-KO scores, thresholds, coverage, alternative
hits and no-hit genes before reconstructing modules. A pathway map reference is
not evidence that every reaction is encoded or active.

## Decision tree

```text
Functional reference need?
├─ KO / KEGG pathway maps with institutional access → kegg
├─ Orthology + multi-DB (COG/KEGG/CAZy fields) → eggnog-mapper
├─ Read-level gene families / MetaCyc pathways → humann + biobakery-databases
├─ Curated MAG metabolism distillate → dram
└─ CAZymes specifically → dbcan
```

## Validation, recovery, and provenance

Check identifier namespaces and release compatibility; reconcile every input gene
to one or more assignments, an explicit no-hit, or a failure. Validate module
completeness using required/optional blocks rather than KO counts alone, inspect
multi-domain proteins and conflicting annotations, and separate genomic
potential, abundance, expression, flux and experimental phenotype.

Retry only identical targeted requests after transient failures; preserve 404 as
no-hit. Rerun derived tables after any KEGG release, mapper, threshold or gene-set
change. Record KEGG `info` output/retrieval date, service or licensed database,
KOALA/mapping software and version, access/license basis, input checksums, all
thresholds, commands/logs and raw assignment/module tables. Do not redistribute
restricted KEGG content.

## Related skills

`public-databases` · `eggnog-mapper` · `humann` · `dram` · `gapseq` ·
`progenomes` · `biobakery-databases`
