# Module D — Assembly and gene catalogue

Construct contigs and a non-redundant gene catalogue with functional annotation.

## Recommended sequence

| Step | Default tools / parameters | Typical output |
|---|---|---|
| Assemble | MEGAHIT (default); metaSPAdes optional (higher RAM/time) | `final.contigs.fa` |
| Evaluate | QUAST; metaQUAST optional | assembly report |
| Predict genes | Prodigal `-p meta` | gene nucleotide FASTA + GFF |
| Optional filter | retain `partial=00` full-length genes | reduced ORF set |
| Cluster | `cd-hit-est -aS 0.9 -c 0.95 -G 0 -g 0` | NR nucleotide FASTA |
| Translate | `seqkit translate --trim` | NR protein FASTA |
| Quantify | salmon index + `salmon quant --meta` | gene TPM and count tables |
| Function | eggNOG-mapper (DIAMOND) → COG / KO / CAZy | annotation abundance tables |
| AMR | RGI / CARD on proteins (± nucleotides/contigs) | resistance annotations |
| Gene taxonomy | Kraken2 on NR genes | gene-level taxonomic table |

## Assembly notes

- Prefer sample-specific or stratum-matched assembly when the contrast is
  biological; whole-cohort co-assembly is a computational convenience, not a
  default scientific choice ([study-design.md](study-design.md)).
- Length-filter very large contig sets before gene prediction when required.
- Hybrid short- and long-read assembly (e.g. metaSPAdes hybrid routes) must
  record which reads contributed to assembly versus coverage.

## Assembler defaults by read type

| Read type | Common assemblers |
|---|---|
| Illumina PE | MEGAHIT, metaSPAdes |
| ONT / CLR | metaFlye or equivalent |
| HiFi | hifiasm-meta / Flye variants |

BASALT consumes assemblies; it does not replace this module.

## Provenance

Record assembler version and command, clustering thresholds, quantification
units, and annotation database releases with every catalogue claim.
