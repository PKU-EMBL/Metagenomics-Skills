# BASALT CLI cheatsheet (Conda)

```bash
# Short + ONT/CLR
BASALT -a asm.fa -s R1.fq,R2.fq -l ont.fq -t 64 -m 256 --mode new -o hybrid

# HiFi only
BASALT -a asm.fa -hf hifi.fq -t 32 -m 128 --mode new -o hifi

# Fast pilot
BASALT -a asm.fa -s R1.fq,R2.fq --sensitive quick --refinepara quick \
  -t 32 -m 128 --mode new -o pilot

# Resume
BASALT --mode continue
```

Retain: `BASALT_command.txt`, `Basalt_log.txt`, `Basalt_checkpoint.txt`, input checksums,
env export, model checksums.
