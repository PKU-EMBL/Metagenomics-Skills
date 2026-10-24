---
name: bigscape
description: >
  Cluster and compare biosynthetic gene clusters across genomes with BiG-SCAPE
  (similarity networks of antiSMASH regions). Use after batch antiSMASH for BGC family
  discovery.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "BGC, network, genome-mining, antiSMASH"
  metagenomics.upstream: "https://github.com/medema-group/BiG-SCAPE"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "2.0 interface"
  metagenomics.command-status: "BiG-SCAPE 2 cluster CLI checked against v2.0.3 source; not executed here"
---

# BiG-SCAPE

Upstream: [medema-group/BiG-SCAPE](https://github.com/medema-group/BiG-SCAPE)

## Citation

Navarro-Muñoz, J. C. *et al.* A computational framework to explore large-scale
biosynthetic diversity. *Nat. Chem. Biol.* **16**, 60–68 (2020).
https://doi.org/10.1038/s41589-019-0400-9

Draisma, A. *et al.* BiG-SCAPE 2.0 and BiG-SLiCE 2.0: scalable, accurate
and interactive sequence clustering of metabolic gene clusters. *Nat. Commun.*
(2026). https://doi.org/10.1038/s41467-026-68733-5

## Analytical thinking

BiG-SCAPE groups antiSMASH regions into **BGC families** via similarity
networks. Requires consistent antiSMASH outputs. Family membership ≠ identical
chemistry — use for prioritization and diversity plots.

## How to run

BiG-SCAPE 2 uses subcommands. Supply a curated directory of compatible
antiSMASH region GenBanks; do not point it at mixed whole-genome and region GBKs.

```bash
set -Eeuo pipefail
input="${1:?usage: cluster-bigscape.sh ANTISMASH_GBK_DIR OUTPUT_DIR}"
out="${2:?usage: cluster-bigscape.sh ANTISMASH_GBK_DIR OUTPUT_DIR}"
threads="${THREADS:-16}"
test -d "$input" || exit 2
find "$input" -type f -name '*.gbk' -print -quit | grep -q . || exit 2
log_dir="${out}.logs"
test ! -e "$out" && test ! -e "$log_dir" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")" "$log_dir"

bigscape cluster --input-dir "$input" --output-dir "$out" \
  --cores "$threads" --label study --include-singletons \
  >"$log_dir/bigscape.stdout.log" 2>"$log_dir/bigscape.stderr.log"
find "$out" -type f -name '*.db' -print -quit | grep -q .
find "$out" -type f \( -name '*.tsv' -o -name '*.csv' \) -print -quit | grep -q .
```

MIBiG or custom references must be provided through the version-matched v2
reference options and recorded as a frozen release. BiG-SCAPE 1 flags such as
`-i/-o/-c` are not interchangeable with this interface.

## Validation, recovery, and provenance

Require the SQLite database, logs, network/GCF tables, and HTML or configured
machine-readable outputs. Reconcile every input region as included, excluded, or
failed; inspect antiSMASH version compatibility, duplicate regions, singleton
policy, distance/GCF cutoffs, class partitioning, and reference handling. Test
cutoff robustness for conclusions based on family counts or novelty.

Use fresh outputs after changing inputs, references, config, or release. Record
BiG-SCAPE/Pfam versions, config and cutoff set, antiSMASH and MIBiG releases,
input manifest/checksums, command, logs, database/output checksums, and exported
network schema. A GCF is a computational similarity cluster, not identical
chemistry or activity.

## Related skills

`antismash` · `microbial-mining` · `bakta` · `visualization`
