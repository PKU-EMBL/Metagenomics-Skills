# Sample and analysis manifest template

Use one row per sequencing library. Keep `sample_id` as the biological sample and
`library_id` as the technical library so technical replicates do not become
false biological replication.

## Minimum sample sheet

```tsv
sample_id	library_id	subject_id	group	timepoint	control_type	extraction_batch	library_batch	sequencing_run	lane	platform	layout	read1	read2	long_reads	host_reference
S01	S01_L1	P01	control	T0	biological	E1	L1	RUN1	1	Illumina	PE	seq/S01_R1.fastq.gz	seq/S01_R2.fastq.gz		GRCh38.p14
S02	S02_L1	P02	treatment	T0	biological	E1	L1	RUN1	2	Illumina	PE	seq/S02_R1.fastq.gz	seq/S02_R2.fastq.gz		GRCh38.p14
BLK01	BLK01_L1		blank		kit_blank	E1	L1	RUN1	3	Illumina	PE	seq/BLK01_R1.fastq.gz	seq/BLK01_R2.fastq.gz		GRCh38.p14
```

Use empty fields, not invented values. Add measured covariates as explicit
columns; do not encode several variables into `sample_id`.

## Assembly and coverage plan

```tsv
assembly_id	stratum	assembly_type	assembly_fasta	assembly_read_ids	coverage_read_ids	assembler	assembler_version	run_directory
S01_asm	cohort_A	individual	result/assembly/S01.fa	S01_L1	S01_L1,S02_L1	MEGAHIT	x.y.z	runs/S01_asm
S02_asm	cohort_A	individual	result/assembly/S02.fa	S02_L1	S01_L1,S02_L1	MEGAHIT	x.y.z	runs/S02_asm
A_pool	cohort_A	pool	result/assembly/A_pool.fa	S01_L1,S02_L1	S01_L1,S02_L1	MEGAHIT	x.y.z	runs/A_pool
```

`assembly_read_ids` records which libraries created the contigs;
`coverage_read_ids` records every library mapped back for abundance/binning.
Preserve this distinction.

## Validation before execution

- `sample_id` and `library_id` are non-empty; `library_id` is unique.
- Every declared read exists and PE mates are both present.
- Group, control, and batch labels use a documented vocabulary.
- The primary group is not perfectly confounded with extraction/library/run.
- Every assembly/read ID resolves to the sample sheet.
- Unrelated strata are not pooled only to increase depth.
- Paths are relative to a declared project root or are absolute; never a mix of
  unexplained working-directory assumptions.
