# Module I — BASALT operational diagnostics

For Modules B–E, consult the corresponding module reference and the official
manuals of the failing tool before introducing ad hoc fixes.

Preserve diagnostic evidence before modifying files or re-running stages:

- complete command line;
- stdout / stderr;
- `Basalt_log.txt` and `Basalt_checkpoint.txt` (Conda edition);
- software versions and environment export;
- input checksums;
- `BASALT_WEIGHT` and CheckM2 database identity.

## Fast diagnostic sequence (Conda)

```bash
eval "$(micromamba shell hook --shell bash)"
micromamba activate basalt

pwd
command -v BASALT checkm2 metabat2 SemiBin2 bowtie2 samtools spades.py
test -n "$BASALT_WEIGHT" && \
  find "$BASALT_WEIGHT" -maxdepth 1 -name '*_ensemble.csv' | wc -l
checkm2 database --current
tail -n 30 Basalt_checkpoint.txt
tail -n 100 Basalt_log.txt
grep -Ei 'error|failed|warning|traceback' *.log 2>/dev/null || true
```

Without activation, prefix with `micromamba run -n basalt`.

## Common failures

### `BASALT: command not found`

Environment not active or installer not run. Re-activate; verify
`$CONDA_PREFIX/bin/BASALT`. From the clone: `micromamba run -n basalt bash install.sh`.

### Permission denied / urge to `chmod 777`

Do **not** use `chmod 777` or `sudo` on the repo, env, weights, or DB. Run
`bash install.sh` (source need not be executable). Fix ownership of a
user-writable Micromamba/Conda env instead.

### Model / refinement failures

Confirm `BASALT_WEIGHT` points to the extracted directory and that five
`*_ensemble.csv` files exist. Keep a single authoritative export in the shell
init file used by interactive and batch jobs. Hash models for the record.

### CheckM2 database missing

```bash
checkm2 database --download
checkm2 database --current
# only if discovery fails:
export CHECKM2DB=/absolute/path/to/CheckM2_database/uniref100.KO.1.dmnd
```

### Path / sample delimiter problems

- Prefer dedicated CWD + symlinked local names (Conda edition).
- Quote `-s` when `/` is special to the scheduler.
- Do not put HiFi under `-l`.
- Avoid spaces and shell metacharacters in filenames.
- If absolute paths are required operationally, move to **BASALT-Air**.

### Wrong biology, successful exit

Symptoms: many bins, high contamination, incoherent taxonomy, or MAGs that
mirror a dominant sample’s depth.

Checks:

1. Design manifest: did an unrelated assembly enter the run?
2. Coverage reads: do they match the assemblies?
3. Pooling: did a high-depth sample dominate?
4. Acceptance criteria: were filters applied, or is “success” just FASTA count?

### Resume loops or checkpoint confusion

- Only `BASALT --mode continue` in the **same** directory with unchanged
  inputs/code/models/DBs.
- Do not copy mixed intermediates from another run.
- If provenance changed → new directory + `--mode new`.
- Do not run two BASALT processes in one directory.

### Out of memory / disk

- Lower `--sensitive` for pilots (`quick`).
- Request more RAM/temp for `more-sensitive`, many samples, or large assemblies.
- `-m` informs scheduling; the scheduler must enforce hard limits.

### Optional binner (`-e`) failures

Validate each adapter env separately. For LorBin, confirm the
**LorBin-BASALT-Extrabinner** fork commit and BASALT-compatible install—not an
arbitrary upstream LorBin.

### Air vs Conda confusion

If commands use `basalt` lowercase, Pixi, `--workdir`, or `--outdir`, follow
BASALT-Air docs. Conda checkpoints and Air checkpoints are not portable.

## Decision after diagnosis

| Finding | Action |
|---|---|
| Env/tool/DB missing | Fix install; rerun preflight; new or continue as appropriate |
| Mid-run crash, provenance intact | `--mode continue` |
| Bad inputs or design | Stop; fix manifest; new run directory |
| Need absolute paths / isolated outdirs | Switch edition to BASALT-Air for new work |
| Scientific overclaim risk | Keep computational success; revise interpretation and filters |

## What not to recommend

- `chmod -R 777`
- Deleting checkpoints to “force progress” without a new provenance record
- Mixing QC databases across design comparisons
- Claiming `more-sensitive` or extra binners as universally better
- Inventing CLI flags not present in `--help` or the guide
