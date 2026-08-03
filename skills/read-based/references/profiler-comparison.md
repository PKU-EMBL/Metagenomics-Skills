# Profiler comparison notes

| Method | Unit | Strength | Failure mode |
|--------|------|----------|--------------|
| MetaPhlAn4 | Clade markers | Low false positives | Misses taxa without markers |
| HUMAnN4 | UniRef/gene families, pathways | Function + taxonomy | Pathway ≠ activity |
| Kraken2 | k-mers | Speed, custom DBs | DB contamination / over-classification |
| Bracken | Re-estimated species | Abundance smoothing | Fragile rare taxa |
