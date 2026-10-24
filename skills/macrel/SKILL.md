---
name: macrel
description: >
  Screen genomes and metagenomes for antimicrobial peptides (AMPs). Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "AMP, antimicrobial-peptide, genome-mining"
  metagenomics.upstream: "https://github.com/BigDataBiology/macrel"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "current peptides/contigs subcommands checked against upstream usage; not executed here"
---

# Macrel

Upstream: [Macrel](https://github.com/BigDataBiology/macrel)

## Citation

Santos-Júnior, C. D., Pan, S., Zhao, X. & Coelho, L. P. Macrel: antimicrobial peptide screening in genomes and metagenomes. *PeerJ* **8**, e10555 (2020). https://doi.org/10.7717/peerj.10555

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Macrel mines **small AMP-like peptides**. High false-discovery risk without experimental validation — report as computational candidates. Complementary to antiSMASH (BGCs) and RGI (AMR genes).

## How to run

Use `contigs` for nucleotide assemblies and `peptides` only for an existing
amino-acid FASTA. The older `get-smorfs` workflow is not the current public CLI.

```bash
set -Eeuo pipefail
contigs="${1:?usage: run-macrel.sh CONTIGS_FASTA OUTPUT_DIR}"
out="${2:?usage: run-macrel.sh CONTIGS_FASTA OUTPUT_DIR}"
test -s "$contigs" || exit 2
test ! -e "$out" && test ! -e "${out}.stdout.log" && \
  test ! -e "${out}.stderr.log" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")"

macrel contigs --fasta "$contigs" --output "$out" \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
find "$out" -type f -name '*.prediction' -size +0c -print -quit | grep -q .
```

## Key parameters

| smORFs first | short ORFs | |
| peptides | AMP classifier | |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Validation, recovery, and provenance

Require the prediction table, smORF sequence/coordinate outputs for contig mode,
and logs; retain zero-candidate samples. Inspect peptide length/composition,
AMP and hemolysis probabilities, duplicate peptides, partial ORFs, contig-edge
status, and overlap with annotated proteins. Rank candidates across thresholds
instead of treating the default probability boundary as biological proof.

Use fresh outputs after changing input, mode, model, or release. Record Macrel
and model/dependency versions, input checksum, mode, command, logs, prediction
and sequence checksums, thresholds, and downstream deduplication. AMP and
hemolysis scores are computational hypotheses requiring synthesis and assays.

## Related skills

`antismash` · `rgi` · `prodigal` · `dram` · `microbial-mining` ·
`tool-selection` · `metagenomics-workflow`
