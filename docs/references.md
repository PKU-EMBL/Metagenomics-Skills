# References

Primary literature for tools and databases used in Metagenomics Skills.
Citation style follows *Nature* journal format (author–year / *et al.*, italic journal,
bold volume, DOI). Cite the version you actually ran in Methods; these entries are
the canonical papers to reference.

---

## Quality control

1. Chen, S., Zhou, Y., Chen, Y. & Gu, J. fastp: an ultra-fast all-in-one FASTQ preprocessor. *Bioinformatics* **34**, i884–i890 (2018). https://doi.org/10.1093/bioinformatics/bty560

2. Beghini, F. *et al.* Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife* **10**, e65088 (2021). https://doi.org/10.7554/eLife.65088  
   *(KneadData / MetaPhlAn / HUMAnN ecosystem)*

## Assembly

3. Li, D., Liu, C.-M., Luo, R., Sadakane, K. & Lam, T.-W. MEGAHIT: an ultra-fast single-node solution for large and complex metagenomics assembly via succinct de Bruijn graph. *Bioinformatics* **31**, 1674–1676 (2015). https://doi.org/10.1093/bioinformatics/btv033

4. Nurk, S., Meleshko, D., Korobeynikov, A. & Pevzner, P. A. metaSPAdes: a new versatile metagenomic assembler. *Genome Res.* **27**, 824–834 (2017). https://doi.org/10.1101/gr.213959.116

## Binning

5. Qiu, Z. *et al.* BASALT refines binning from metagenomic data and increases resolution of genome-resolved metagenomic analysis. *Nat. Commun.* **15**, 2179 (2024). https://doi.org/10.1038/s41467-024-46539-7

6. Uritskiy, G. V., DiRuggiero, J. & Taylor, J. MetaWRAP—a flexible pipeline for genome-resolved metagenomic data analysis. *Microbiome* **6**, 158 (2018). https://doi.org/10.1186/s40168-018-0541-1

7. Sieber, C. M. K. *et al.* Recovery of genomes from metagenomes via a dereplication, aggregation and scoring strategy. *Nat. Microbiol.* **3**, 836–843 (2018). https://doi.org/10.1038/s41564-018-0171-1

8. Olm, M. R., Brown, C. T., Brooks, B. & Banfield, J. F. dRep: a tool for fast and accurate genomic comparisons that enables improved genome recovery from metagenomes through de-replication. *ISME J.* **11**, 2864–2868 (2017). https://doi.org/10.1038/ismej.2017.126

9. Aroney, S. T. N. *et al.* CoverM: read alignment statistics for metagenomics. *Bioinformatics* **41**, btaf147 (2025). https://doi.org/10.1093/bioinformatics/btaf147

10. Chklovski, A., Parks, D. H., Woodcroft, B. J. & Tyson, G. W. CheckM2: a rapid, scalable and accurate tool for assessing microbial genome quality using machine learning. *Nat. Methods* **20**, 1203–1212 (2023). https://doi.org/10.1038/s41592-023-01940-w

## Taxonomic annotation

11. Blanco-Míguez, A. *et al.* Extending and improving metagenomic taxonomic profiling with uncharacterized species using MetaPhlAn 4. *Nat. Biotechnol.* **41**, 1633–1644 (2023). https://doi.org/10.1038/s41587-023-01688-w

12. Wood, D. E., Lu, J. & Langmead, B. Improved metagenomic analysis with Kraken 2. *Genome Biol.* **20**, 257 (2019). https://doi.org/10.1186/s13059-019-1891-0

13. Chaumeil, P.-A., Mussig, A. J., Hugenholtz, P. & Parks, D. H. GTDB-Tk v2: memory friendly classification with the Genome Taxonomy Database. *Bioinformatics* **38**, 5315–5316 (2022). https://doi.org/10.1093/bioinformatics/btac672

14. Parks, D. H. *et al.* A complete domain-to-species taxonomy for Bacteria and Archaea. *Nat. Biotechnol.* **38**, 1079–1086 (2020). https://doi.org/10.1038/s41587-020-0501-8

15. Almeida, A. *et al.* A unified catalog of 204,938 reference genomes from the human gut microbiome. *Nat. Biotechnol.* **39**, 105–114 (2021). https://doi.org/10.1038/s41587-020-0603-3  
   *(UHGG; available via MGnify genome catalogues)*

16. Richardson, L. *et al.* MGnify: the microbiome sequence data analysis resource in 2023. *Nucleic Acids Res.* **51**, D753–D759 (2023). https://doi.org/10.1093/nar/gkac1080

## Functional annotation

17. Hyatt, D. *et al.* Prodigal: prokaryotic gene recognition and translation initiation site identification. *BMC Bioinformatics* **11**, 119 (2010). https://doi.org/10.1186/1471-2105-11-119

18. Fu, L., Niu, B., Zhu, Z., Wu, S. & Li, W. CD-HIT: accelerated for clustering the next-generation sequencing data. *Bioinformatics* **28**, 3150–3152 (2012). https://doi.org/10.1093/bioinformatics/bts565

19. Patro, R., Duggal, G., Love, M. I., Irizarry, R. A. & Kingsford, C. Salmon provides fast and bias-aware quantification of transcript expression. *Nat. Methods* **14**, 417–419 (2017). https://doi.org/10.1038/nmeth.4197

20. Cantalapiedra, C. P., Hernández-Plaza, A., Letunic, I., Bork, P. & Huerta-Cepas, J. eggNOG-mapper v2: functional annotation, orthology assignments, and domain prediction at the metagenomic scale. *Mol. Biol. Evol.* **38**, 5825–5829 (2021). https://doi.org/10.1093/molbev/msab293

21. Alcock, B. P. *et al.* CARD 2023: expanded curation, support for machine learning, and resistome prediction at the Comprehensive Antibiotic Resistance Database. *Nucleic Acids Res.* **51**, D690–D699 (2023). https://doi.org/10.1093/nar/gkac920

## Mapping

22. Langmead, B. & Salzberg, S. L. Fast gapped-read alignment with Bowtie 2. *Nat. Methods* **9**, 357–359 (2012). https://doi.org/10.1038/nmeth.1923

23. Li, H. Minimap2: pairwise alignment for nucleotide sequences. *Bioinformatics* **34**, 3094–3100 (2018). https://doi.org/10.1093/bioinformatics/bty191

24. Sahlin, K. Strobealign: flexible seed size enables ultra-fast and accurate read alignment. *Genome Biol.* **23**, 260 (2022). https://doi.org/10.1186/s13059-022-02831-7

## Microbial mining

25. Blin, K. *et al.* antiSMASH 7.0: new and improved predictions for detection, regulation, chemical structures and visualisation. *Nucleic Acids Res.* **51**, W46–W50 (2023). https://doi.org/10.1093/nar/gkad344

26. Camargo, A. P. *et al.* Identification of mobile genetic elements with geNomad. *Nat. Biotechnol.* **42**, 1303–1312 (2024). https://doi.org/10.1038/s41587-023-01953-y

27. Guo, J. *et al.* VirSorter2: a multi-classifier, expert-guided approach to detect diverse DNA and RNA viruses. *Microbiome* **9**, 37 (2021). https://doi.org/10.1186/s40168-020-00990-y

28. Nayfach, S. *et al.* CheckV assesses the quality and completeness of metagenome-assembled viral genomes. *Nat. Biotechnol.* **39**, 578–585 (2021). https://doi.org/10.1038/s41587-020-00774-7

29. Shaffer, M. *et al.* DRAM for distilling microbial metabolism to automate the curation of microbiome function. *Nucleic Acids Res.* **48**, 8883–8900 (2020). https://doi.org/10.1093/nar/gkaa621

30. Santos-Júnior, C. D., Pan, S., Zhao, X. & Coelho, L. P. Macrel: antimicrobial peptide screening in genomes and metagenomes. *PeerJ* **8**, e10555 (2020). https://doi.org/10.7717/peerj.10555

31. Arango-Argoty, G. *et al.* DeepARG: a deep learning approach for predicting antibiotic resistance genes from metagenomic data. *Microbiome* **6**, 23 (2018). https://doi.org/10.1186/s40168-018-0401-z

32. Zimmermann, J., Kaleta, C. & Waschina, S. gapseq: informed prediction of bacterial metabolic pathways and reconstruction of accurate metabolic models. *Genome Biol.* **22**, 81 (2021). https://doi.org/10.1186/s13059-021-02295-1

33. Tesson, F. *et al.* Systematic and quantitative view of the antiviral arsenal of prokaryotes. *Nat. Commun.* **13**, 2561 (2022). https://doi.org/10.1038/s41467-022-30269-9

34. Kang, D. D. *et al.* MetaBAT 2: an adaptive binning algorithm for robust and efficient genome reconstruction from metagenome assemblies. *PeerJ* **7**, e7359 (2019). https://doi.org/10.7717/peerj.7359

35. Vaser, R., Sović, I., Nagarajan, N. & Šikić, M. Fast and accurate de novo genome assembly from long uncorrected reads. *Genome Res.* **27**, 737–746 (2017). https://doi.org/10.1101/gr.214270.116

36. Walker, B. J. *et al.* Pilon: an integrated tool for comprehensive microbial variant detection and genome assembly improvement. *PLoS ONE* **9**, e112963 (2014). https://doi.org/10.1371/journal.pone.0112963

37. Shaw, J. & Yu, Y. W. Fast and robust metagenomic sequence comparison through sparse chaining with skani. *Nat. Methods* **20**, 1661–1665 (2023). https://doi.org/10.1038/s41592-023-02018-3

38. Navarro-Muñoz, J. C. *et al.* A computational framework to explore large-scale biosynthetic diversity. *Nat. Chem. Biol.* **16**, 60–68 (2020). https://doi.org/10.1038/s41589-019-0400-9

---

## How to cite in Methods (example)

> Clean reads were produced with fastp¹ and KneadData². Contigs were assembled
> with MEGAHIT³, mapped with Bowtie 2²², and binned with BASALT⁵. Genome
> taxonomy was assigned with GTDB-Tk¹³. BGCs were mined with antiSMASH²⁵;
> MGEs with geNomad²⁶.

Always add **software version** and **database release** next to the citation.

## See also

- [Standard pipeline](standard-pipeline.md)
- [Skills catalog](skills.md)
- [Public databases](public-databases.md)
