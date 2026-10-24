---
name: cd-hit
description: >
  Cluster genes/proteins to build non-redundant catalogues. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "clustering, dereplication"
  metagenomics.upstream: "https://github.com/weizhongli/cdhit"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "CD-HIT-EST catalogue template statically reviewed; not executed here"
---

# CD-HIT

Upstream: [weizhongli/cdhit](https://github.com/weizhongli/cdhit)

## Citation

Fu, L., Niu, B., Zhu, Z., Wu, S. & Li, W. CD-HIT: accelerated for clustering the next-generation sequencing data. *Bioinformatics* **28**, 3150–3152 (2012). https://doi.org/10.1093/bioinformatics/bts565

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

`cd-hit-est` collapses redundant nucleotide ORFs into a non-redundant catalogue.
Defaults used widely in shotgun catalogues: identity **0.95**, alignment coverage
**0.9** (`-c 0.95 -aS 0.9`). Changing thresholds changes biological interpretation
of “a gene”—report them.

## How to run

```bash
set -Eeuo pipefail
genes="${1:?usage: cluster-genes.sh GENES_FNA OUTPUT_DIR}"
out="${2:?usage: cluster-genes.sh GENES_FNA OUTPUT_DIR}"
threads="${THREADS:-8}"
memory_mb="${MEMORY_MB:-0}"
test -s "$genes" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

cd-hit-est -i "$genes" -o "$out/nucleotide.fa" \
  -aS 0.9 -c 0.95 -G 0 -g 0 -T "$threads" -M "$memory_mb" \
  >"$out/cd-hit.stdout.log" 2>"$out/cd-hit.stderr.log"
test -s "$out/nucleotide.fa"
test -s "$out/nucleotide.fa.clstr"
seqkit translate --trim "$out/nucleotide.fa" \
  >"$out/protein.fa" 2>"$out/translate.stderr.log"
```

## Validation, recovery, and provenance

Verify unique representative IDs, cluster membership coverage, sequence counts
before/after, length/partial-gene distributions, and nucleotide-to-protein ID
mapping. Test threshold sensitivity when catalogue richness is a result. The
common 95% identity/90% shorter-sequence coverage policy defines an operational
gene family; it is not a universal orthology boundary.

Use a new output after changing input order or clustering thresholds. Record
CD-HIT/SeqKit versions, input checksum, identity/coverage/global-local settings,
threads/memory, commands, logs, representative and `.clstr` checksums, and
cluster statistics.

## Related skills

`prodigal` · `salmon` · `eggnog-mapper` · `mmseqs2`

