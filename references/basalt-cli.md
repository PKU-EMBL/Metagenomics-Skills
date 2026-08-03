# BASALT and BASALT-Air command reference

Primary documentation: https://basalt-guide.readthedocs.io/en/latest/  
Primary publication: https://doi.org/10.1038/s41467-024-46539-7  
BASALT-Air repository: https://github.com/PKU-EMBL/BASALT-Air

## Edition selection

| Capability | Conda BASALT (`BASALT`) | BASALT-Air (`basalt`) |
|---|---|---|
| Environment | Conda or Micromamba with installer | Pixi with lockfile |
| Path handling | Dedicated working directory; local or relative names preferred | First-class absolute paths |
| Work and output locations | Intermediates in the working directory; `-o` names the final directory | Separate `--workdir` and `--outdir` |
| Provenance artefacts | Command record, logs, checkpoints | Structured run manifest and timestamped logs |
| Checkpoint compatibility | Not interchangeable with Air | Not interchangeable with Conda |
| Recommended use | Reproduction or resumption of existing Conda analyses | New deployments |

State the target edition in every command example. Do not transpose Conda syntax
into Air projects without translating path and delimiter conventions.

## What BASALT does

1. **Autobinning** — MetaBAT 2 + SemiBin 2; `sensitive` adds CONCOCT;
   `more-sensitive` also adds MaxBin 2.0. Optional MetaBinner / VAMB / LorBin.
2. **Bin selection** — within assembly, then across assemblies.
3. **Refinement** — five-MLP ensemble on composition + coverage features; then
   read-connectivity retrieval; OLC where applicable.
4. **Reassembly** — SPAdes-related / hybrid paths when required reads exist.

## Supported input designs (Conda)

Every run needs ≥1 assembly and ≥1 coverage source:

| Design | Assembly | Short PE | ONT/CLR (`-l`) | HiFi (`-hf`) |
|---|---|---|---|---|
| Short-read only | yes | yes | no | no |
| Long-read only | yes | no | yes | no |
| HiFi only | yes | no | no | yes |
| Short + ONT/CLR | yes | yes | yes | no |
| Short + HiFi | yes | yes | no | yes |

Conda short-read syntax:

```text
-s R1_a.fastq,R2_a.fastq/R1_b.fastq,R2_b.fastq
```

Assemblies: comma-separated `.fa` / `.fna` / `.fasta`. Contigs < 1000 bp filtered
in preprocessing.

## Recommended Conda invocation

```bash
BASALT \
  -a assembly.fasta \
  -s sample_R1.fastq,sample_R2.fastq \
  -t 32 -m 128 \
  --sensitive sensitive \
  --refinepara quick \
  --min-cpn 35 \
  --max-ctn 20 \
  -q checkm2 \
  --mode new \
  -o study_01_basalt
```

| Option | Role |
|---|---|
| `-t` | Requested threads |
| `-m` | Available RAM (GB) for internal scheduling — not a hard OS cap |
| `--sensitive` | `quick` / `sensitive` / `more-sensitive` |
| `--refinepara` | `quick` / `deep` retrieval depth |
| `--min-cpn` / `--max-ctn` | Completeness/contamination gates into refinement |
| `-q` | `checkm2` (default) or `checkm` |
| `--mode` | `new` or `continue` |
| `--module` | `all` (default), or `autobinning` / `refinement` / `reassembly` |
| `-e` | Optional `m`, `v`, `l` (comma-combinable) |
| `-o` | Final directory **name** in CWD (not a portable absolute out path) |

### Multi-assembly short-read example

```bash
BASALT \
  -a a1.fa,a2.fa,pool.fa \
  -s s1_R1.fastq,s1_R2.fastq/s2_R1.fastq,s2_R2.fastq \
  -t 64 -m 256 \
  --mode new -o habitat_A_basalt
```

### Hybrid short + ONT/CLR

```bash
BASALT \
  -a assembly.fasta \
  -s sample_R1.fastq,sample_R2.fastq \
  -l nanopore.fastq \
  -t 64 -m 256 --mode new -o study_hybrid
```

### HiFi

```bash
BASALT \
  -a assembly.fasta \
  -hf hifi.fastq \
  -t 32 -m 128 --mode new -o study_hifi
```

## Installation cues (Conda)

Prefer a release tag for production:

```bash
git clone --branch V1.2.2 --depth 1 \
  https://github.com/PKU-EMBL/BASALT.git BASALT
cd BASALT
micromamba create -n basalt -f basalt_environment.yml \
  --strict-channel-priority --yes
micromamba run -n basalt bash install.sh
```

Then download models into a persistent directory and export `BASALT_WEIGHT`.
Expect **5** `*_ensemble.csv` descriptors after a successful model install.
Configure CheckM2 database separately.

Mainland-China route: `BASALT_setup_China_mainland.py` with `--dry-run` first.
Do not use `sudo` or `chmod 777`.

## LorBin adapter

`-e l` targets **PKU-EMBL/LorBin-BASALT-Extrabinner**, an in-house fork adapted
to BASALT’s Python environment. Install and validate separately. Record:

```bash
git -C /path/to/LorBin-BASALT-Extrabinner rev-parse HEAD \
  > lorbin-basalt-git-commit.txt
```

Package version alone does not uniquely identify fork changes.

## Advanced routes (do not casual-recommend)

- `-d` data feeding of external binsets
- `-r` standalone refinement binset
- `-c` / `-b` coverage or binset lists for dereplication-style stages
- `--module` partial pipelines

These require BASALT-compatible contig IDs, coverage provenance, and often prior
intermediate state. Prefer a full `--module all` pilot first.

## Resume semantics

```bash
# same CWD, same code, models, DBs, inputs
BASALT --mode continue
```

`--mode new` initializes checkpoint state but is not a full cleanup or
provenance firewall—use a **new directory** when anything material changes.

## Output contract

After a successful full run, expect:

- final MAG directory named by `-o` (FASTA, ideally `.fa`);
- final CheckM2 report when the CheckM2 path completed;
- in CWD: `BASALT_command.txt`, `Basalt_log.txt`, `Basalt_checkpoint.txt`,
  plus intermediates.

Presence of FASTA files proves the workflow wrote bins—not that every bin meets
study-specific publication criteria.

## Reproducibility checklist

Capture from the analysis directory:

```bash
git -C /path/to/BASALT rev-parse HEAD > basalt-git-commit.txt
micromamba env export -n basalt > basalt-environment.yml
sha256sum assembly.fasta sample_R1.fastq sample_R2.fastq > input.sha256
(
  cd "$BASALT_WEIGHT"
  find . -type f \( -name '*.pth' -o -name '*_ensemble.csv' \) -print0 \
    | sort -z | xargs -0 sha256sum
) > basalt-models.sha256
```

Also record: complete command, `--sensitive` / `--refinepara` / QC thresholds,
optional binner commits, CheckM2 DB identity, whether the run was resumed,
post-BASALT filters, and final output checksums.

### Methods bullets (minimum)

- BASALT release or Git commit (and Air version if used)
- Assemblies, read sets, and preprocessing
- Sensitivity, refinement, completeness/contamination gates, QC backend
- Optional binners and fork commits
- Compute environment and key external tool versions
- Downstream dereplication, taxonomy, and MAG acceptance criteria
