# Module B — Preprocessing

Quality control and host depletion for shotgun paired-end libraries.

## Project layout

```text
$wd/
├── seq/                 # SampleID_1.fq.gz, SampleID_2.fq.gz
├── temp/                # intermediates
└── result/
    └── metadata.txt     # tab-delimited; SampleID in column 1
```

Convert Windows metadata newlines: `sed -i 's/\r//' result/metadata.txt`.

Confirm Phred33 versus Phred64 encoding and resolve paired-end identifier
collisions before host removal or binning.

## fastp quality control

```bash
fastp -i seq/${i}_1.fq.gz -I seq/${i}_2.fq.gz \
  -j temp/qc/${i}_fastp.json -h temp/qc/${i}_fastp.html \
  -o temp/qc/${i}_1.fastq -O temp/qc/${i}_2.fastq
```

Batch over metadata sample IDs. Temporary storage is commonly ~5× raw input.

## KneadData host removal

```bash
kneaddata -i1 temp/qc/${i}_1.fastq -i2 temp/qc/${i}_2.fastq \
  -o temp/hr --bypass-trim --bypass-trf --reorder \
  --bowtie2-options '--very-sensitive --dovetail' \
  -db ${db}/kneaddata/human/hg_39 \
  --remove-intermediate-output -v -t 3
```

- Use `--reorder` to maintain mate concordance.
- For non-human hosts, build a Bowtie2 index for the relevant genome and record
  its identity in the manifest.
- Prefer public release of dehosted reads for human-associated studies.
- After verification, remove contamination and unmatched intermediates to reclaim
  space (high-host libraries can exceed 90% reduction).

## Outputs for downstream modules

- Host-depleted pairs: `temp/hr/${SampleID}_1.fastq`, `_2.fastq`
- QC summary tables under `result/qc/`
- Manifest fields: `host_reference`, checksums of retained reads
