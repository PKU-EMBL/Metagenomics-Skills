---
name: mobilome-analysis
description: >-
  Design and audit plasmid, phage, integron, insertion-sequence, transposon, ICE/IME,
  and other mobile-element analyses from assemblies, long reads, and proximity data.
  Use to choose element classifiers, boundary and typing tools, plasmid-system networks,
  host linkage, or ARG-context analysis without treating every MGE marker as a complete mobile element.
license: MIT
compatibility: Requires assemblies or long reads with stable sequence IDs; complete-element and host claims need boundary or linkage evidence.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "mobilome,MGE,plasmid,phage,integron,ICE,transposon"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Mobilome analysis

“Mobile genetic element” is an umbrella term, not a single sequence class.
Preserve element type, boundary confidence, completeness, mobility machinery,
and host evidence independently.

## Routing

| Deliverable | Prefer | Important boundary |
|---|---|---|
| Broad plasmid/virus contig screen | `$genomad` | class score is not circular completeness |
| Plasmid architecture classifier | `$plasx` | trained feature space and contig length matter |
| Plasmid similarity/systems network | `$mobmess` | network is sequence architecture, not transfer |
| Plasmid reconstruction/typing | `$mob-suite` / `$plasmaag` | fragmented metagenomes limit replicon recovery |
| Replicon or pMLST typing | `$plasmidfinder` / `$pmlst` | best for isolates or near-complete plasmids |
| MGE life-cycle proteins | `$mobileog` | protein hit is not an element boundary |
| Insertion sequences | `$isescan` | IS presence is not conjugation |
| Integrons/cassettes | `$integronfinder` | integron is not necessarily mobile itself |
| Named IS/Tn/ICE/IME library | `$mobileelementfinder` | supported taxa/library coverage apply |
| Viruses/vOTUs | `$virome-analysis` | quality gate with `$checkv` |
| Host assignment | `$arg-mge-host-linkage` | use orthogonal links and controls |
| Historical/recent transfer candidates | `$horizontal-gene-transfer` | discordance is a hypothesis |

## Input contract

- assembly strategy, read technology, contig-length filter, and assembler graph if retained;
- stable contig/gene IDs and coordinate-bearing GFF;
- circularity/terminal-repeat evidence and raw-read junction support;
- software/model/database versions and checksums;
- sample, time, habitat, and batch metadata;
- host MAG catalogue with CheckM2/GUNC quality where host attribution is planned;
- long-read or Hi-C library metadata, including restriction enzyme for Hi-C.

Run broad MGE discovery on the unbinned assembly as well as selected bins: mobile
contigs are commonly excluded from MAGs because composition and coverage differ.

## Evidence-aware workflow

1. Screen sequence classes with geNomad and element-specific tools.
2. Delineate boundaries; classify complete circular elements separately from fragments.
3. Annotate genes and mobility modules (replication, integration, transfer, stability).
4. Type only elements that satisfy the input assumptions of the typing scheme.
5. Cluster plasmid/viral sequences under declared identity and coverage rules.
6. Join cargo genes by exact coordinates; do not infer carriage from sample co-occurrence.
7. Assign hosts through integration boundaries, long-read junctions, Hi-C, CRISPR, or
   sequence homology; retain method-specific confidence.
8. Build typed evidence networks with `$transfer-network-analysis`.

## Minimum outputs

- `elements.tsv`: sequence ID, element class, coordinates, boundary/completeness,
  circularity evidence, classifier scores, and conflict flags;
- `mobility_modules.tsv`: element/gene IDs, module category, coordinates, and database;
- `cargo.tsv`: ARG/VF/function coordinates and containment relation;
- `host_links.tsv`: host candidate, method, score, controls, ambiguity, and evidence tier;
- cluster/network tables with the exact identity/coverage and edge semantics;
- no-call and conflict tables, logs, versions, database manifests, and checksums.

## Quality gates

Reject or qualify conclusions when element boundaries cross low-support assembly
junctions, circularity is asserted only from assembler labels, host bins are
contaminated, Hi-C contacts track abundance/restriction density, or classifiers
conflict. Deduplicate sequences without erasing sample occurrence. Inspect ARGs
near contig ends because the element boundary may be truncated.

## Interpretation

A plasmid-like contig is not necessarily an autonomous plasmid; an integrase or
relaxase does not prove transfer competence; a shared plasmid system does not
identify donor, recipient, time, or route. “Mobilizable potential” and “observed
horizontal transfer” are different claims.

See the repository’s
[evidence guide](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/arg-mge-host-strain.md).

## Related skills

`genomad` · `plasx` · `mobmess` · `mob-suite` · `plasmaag` · `mobileog` ·
`isescan` · `integronfinder` · `mobileelementfinder` · `plasmidfinder` · `pmlst` ·
`virome-analysis` · `arg-mge-host-linkage` · `horizontal-gene-transfer` ·
`transfer-network-analysis`
