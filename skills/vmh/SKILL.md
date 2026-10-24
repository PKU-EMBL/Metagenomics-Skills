---
name: vmh
description: >
  Virtual Metabolic Human (VMH) database — human and gut microbiome metabolism
  integrated with nutrition and disease knowledge for GEM interpretation. Use when: (1)
  Contextualizing gapseq / AGORA-style models, (2) Linking metabolites, microbes, and
  nutrition, (3) Browsing human–microbiome metabolic resources. Pair with gapseq for
  reconstruction; do not treat VMH entries as measured fluxes in your sample.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "VMH, GEMs, metabolism, database, gut"
  metagenomics.upstream: "https://www.vmh.life"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "public metabolite API template smoke-tested with glc_D and a no-hit query on 2026-10-24"
---

# Virtual Metabolic Human (VMH)

Portal: https://www.vmh.life

## Citation

Noronha, A. *et al.* The Virtual Metabolic Human database: integrating human and
gut microbiome metabolism with nutrition and disease. *Nucleic Acids Res.*
**47**, D614–D624 (2019). https://doi.org/10.1093/nar/gky992

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

VMH is a **knowledge/integration database** (human + gut microbial metabolism,
nutrition, disease links), not a shotgun profiler. Use it to interpret
genome-scale models and metabolites after `gapseq` (or related GEM tools).

| Resource | Role |
|----------|------|
| `gapseq` | Build/fill models from your genomes/MAGs |
| `vmh` | Browse/integrate human–microbiome metabolic knowledge |
| `kegg` / `dram` | Pathway annotation alternatives |

## Targeted API access

The public API is rate-limited (currently 100 requests/hour/IP without a key).
Prefer downloads or SPARQL for whole-dataset work. This targeted metabolite query
archives the live OpenAPI document and preserves a 404 as no-hit:

```bash
set -euo pipefail
metabolite=${1:?usage: vmh-metabolite.sh VMH_ID FRESH_OUTPUT_DIR}
out=${2:?usage: vmh-metabolite.sh VMH_ID FRESH_OUTPUT_DIR}
[[ "$metabolite" =~ ^[A-Za-z0-9_.-]+$ ]] || exit 2
[[ ! -e "$out" ]] || { echo "refusing to overwrite: $out" >&2; exit 3; }
mkdir -p "$out/logs" "$out/provenance"
curl --fail --silent --show-error --location --retry 3 \
  'https://www.vmh.life/api/docs/openapi.yaml' \
  -o "$out/provenance/openapi.yaml" 2>"$out/logs/curl.log"
http=$(curl --silent --show-error --location --retry 3 --get \
  'https://www.vmh.life/api/public/getMetHandler' \
  --data-urlencode "id=$metabolite" \
  --dump-header "$out/provenance/response.headers" \
  --output "$out/response.json" --write-out '%{http_code}' \
  2>>"$out/logs/curl.log")
printf 'query\thttp_status\tretrieved_utc\n%s\t%s\t%s\n' \
  "$metabolite" "$http" "$(date -u +%FT%TZ)" \
  >"$out/provenance/request.tsv"
if [[ "$http" == 404 ]]; then
  printf 'query\tstatus\n%s\tno_hit\n' "$metabolite" >"$out/no-hit.tsv"
elif [[ "$http" == 200 ]]; then
  python3 - "$out/response.json" "$out/provenance/schema.txt" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
key = "metData" if "metData" in data else "metaboliteData"
rows = data.get(key)
if not isinstance(rows, list) or not rows:
    raise SystemExit("missing non-empty metabolite result list")
open(sys.argv[2], "w").write(f"result_key\t{key}\nrecords\t{len(rows)}\n")
PY
  sha256sum "$out/response.json" >"$out/provenance/response.sha256"
else
  echo "unexpected HTTP status: $http" >&2; exit 4
fi
```

Never place API keys in command history or logs. VMH flux/capability fields are
model/database outputs, not metabolomics measurements from the study.

## Decision tree

```text
Metabolic modeling need?
├─ Reconstruct model from MAG → gapseq
├─ Interpret vs human/gut/nutrition knowledge → vmh
├─ Distill annotations without full GEM → dram
└─ KO maps → kegg (license)
```

## Validation, recovery, and provenance

Validate namespaces, aliases, compartments, formulas/charges and cross-references
before joining VMH to GEM, metabolomics or taxonomic tables. Preserve ambiguous
and no-hit mappings. For model comparisons, check mass/charge balance, exchange
bounds, medium/objective, blocked reactions, gap filling and sensitivity; compare
predictions with measured metabolites or phenotypes separately.

Retry an identical request only after transient/429 failures and honor rate-limit
headers; use a fresh directory when query, API schema, model release or mapping
changes. Archive OpenAPI/schema snapshot, endpoint/query/status/retrieval time,
response checksum, VMH/model/database release or download identity, license/terms,
input mappings, software, commands/logs and all model assumptions. A database
association or in-silico flux is a hypothesis until independently validated.

## Related skills

`gapseq` · `dram` · `kegg` · `public-databases` · `microbial-mining`
