# Sample design manifest template

| sample_id | stratum | host_reference | assembly | assembly_type | assembly_reads | coverage_reads | assembler | run_directory |
|-----------|---------|----------------|----------|---------------|----------------|----------------|-----------|---------------|
| S1 | habitat_A | hg38 | S1.fa | individual | S1_R1/R2 | S1_R1/R2 | MEGAHIT x.y | /runs/A_s1 |
| S2 | habitat_A | hg38 | S2.fa | individual | S2_R1/R2 | S2_R1/R2 | MEGAHIT x.y | /runs/A_s2 |
| poolA | habitat_A | hg38 | poolA.fa | pool | S1+S2 | S1+S2 | MEGAHIT x.y | /runs/A_pool |
