---
name: alphagem
description: >
  AlphaGEM — genome-scale metabolic modelling aided by protein structure alignment and
  deep-learning dark-metabolism mining. Use when: (1) Building or refining GEMs beyond
  sequence-only gap filling, (2) Integrating structure signals into metabolic networks,
  (3) Comparing to gapseq / VMH workflows. Route via metagenomics-llm; pair with gapseq
  / vmh for classical GEM context.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "AlphaGEM, GEM, metabolism, structure, deep-learning"
  metagenomics.upstream: "https://github.com/hongzhonglu/AlphaGEM"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "snapshot 956b584"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream source; not executed here"
---

# AlphaGEM

Upstream: [hongzhonglu/AlphaGEM](https://github.com/hongzhonglu/AlphaGEM)

## Citation

Han, W. *et al.* AlphaGEM enables precise genome-scale metabolic modelling by
integrating protein structure alignment with deep-learning-based dark
metabolism mining. *Nat. Commun.* (2026).
https://doi.org/10.1038/s41467-026-75549-w

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Sequence-only GEM reconstruction misses “dark” metabolism. AlphaGEM combines
**structure alignment** with DL mining to improve genome-scale models. Use on
high-quality genomes/MAGs after `mag-qc`; interpret human/gut context with
`vmh` when relevant.

Models remain computational — not measured fluxes. Pin AlphaGEM version,
structure sources (e.g. AFDB), and gap-filling rules.

## Inputs and run

Require one high-quality, uniquely named genome FASTA, an appropriate reference-model choice (`ecoli`, `yeast`, `strco`, `human`, or `synechocystis`), AlphaGEM's Figshare resources, both supplied environments, and a licensed/configured optimizer. Structure mode additionally requires per-gene structures and a mapping table whose IDs exactly match the FASTA.

```bash
set -euo pipefail
id=candidate01
genome=genomes/candidate01.fna
[[ -s "$genome" ]] || exit 2
python AlphaGEM.py --help >/dev/null
# Sequence/PLM route; use structure_alignment only when its structure inputs exist.
python AlphaGEM.py --name "$id" --mode plmsearch --fasta "$genome" \
  --refname ecoli --grothmedium min \
  >"${id}.alphagem.stdout.log" 2>"${id}.alphagem.stderr.log"
test -d "working/$id"
```

For structure evidence, use `--mode structure_alignment --structure DIR --maplist TABLE` and preflight mapping-table coverage. Do not mix reference species, medium, structure thresholds, or resource snapshots across models.

## Decision tree

```text
Metabolic modelling need?
├─ Classical pathway/GEM from MAG → gapseq
├─ Structure + dark metabolism mining → alphagem
├─ Human/gut knowledge integration → vmh
└─ Annotation distillate only → dram
```

## Validation, recovery, and provenance

Require completed logs and a non-empty model/result set under `working/<name>`; reconcile input genes, annotations, added reactions, gap-filled reactions, medium and objective. Run mass/charge consistency, blocked-reaction, growth/no-growth and biologically justified phenotype checks with the produced model format. Compare new dark-metabolism reactions to gene/structure evidence; do not accept growth alone as validation.

AlphaGEM writes a named working directory: archive it or rerun under a fresh name after changing parameters. Record repository commit, Figshare-resource checksums, AlphaGEM/DeepEC/ESM/Foldseek/optimizer versions, reference model, medium, thresholds, input checksum, full command, logs and model checksum. Predicted reactions and fluxes remain computational hypotheses.

## Related skills

`metagenomics-llm` · `gapseq` · `vmh` · `dram` · `deepblast` · `mag-qc` ·
`microbial-mining` · `tool-selection`
