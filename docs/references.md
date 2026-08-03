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

39. Xue, W. *et al.* LorBin: efficient binning of long-read metagenomes by multiscale adaptive clustering and evaluation. *Nat. Commun.* **16**, 9353 (2025). https://doi.org/10.1038/s41467-025-64916-8

40. Wang, Z. *et al.* Effective binning of metagenomic contigs using contrastive multi-view representation learning. *Nat. Commun.* **15**, 585 (2024). https://doi.org/10.1038/s41467-023-44290-z

41. Aroney, S. T. N., Newell, R. J. P., Tyson, G. W. & Woodcroft, B. J. Bin Chicken: targeted metagenomic coassembly for the efficient recovery of novel genomes. *Nat. Methods* (2025). https://doi.org/10.1038/s41592-025-02901-1

42. Kim, J. & Steinegger, M. Metabuli: sensitive and specific metagenomic classification via joint analysis of amino acid and DNA. *Nat. Methods* **21**, 971–973 (2024). https://doi.org/10.1038/s41592-024-02273-y

43. Mattock, J. & Watson, M. A comparison of single-coverage and multi-coverage metagenomic binning reveals extensive hidden contamination. *Nat. Methods* **20**, 1170–1173 (2023). https://doi.org/10.1038/s41592-023-01934-8

44. Pan, S., Zhao, X.-M. & Coelho, L. P. SemiBin2: self-supervised contrastive learning leads to better MAGs for short- and long-read sequencing. *Bioinformatics* **39**, i21–i29 (2023). https://doi.org/10.1093/bioinformatics/btad209

45. Nissen, J. N. *et al.* Improved metagenome binning and assembly using deep variational autoencoders. *Nat. Biotechnol.* **39**, 555–560 (2021). https://doi.org/10.1038/s41587-020-00777-4

46. Orakov, A. *et al.* GUNC: detection of chimerism and contamination in prokaryotic genomes. *Genome Biol.* **22**, 178 (2021). https://doi.org/10.1186/s13059-021-02393-0

47. Olm, M. R. *et al.* inStrain profiles population microdiversity from metagenomic data and sensitively detects shared microbial strains. *Nat. Biotechnol.* **39**, 727–736 (2021). https://doi.org/10.1038/s41587-020-00797-0

48. Shaw, J. & Yu, Y. W. Rapid species-level metagenome profiling and containment estimation with sylph. *Nat. Biotechnol.* **43**, 1348–1359 (2025). https://doi.org/10.1038/s41587-024-02412-y

49. Ruscheweyh, H.-J. *et al.* Cultivation-independent genomes greatly expand taxonomic-profiling capabilities of mOTUs across various environments. *Microbiome* **10**, 212 (2022). https://doi.org/10.1186/s40168-022-01410-z

50. Lu, J., Breitwieser, F. P., Thielen, P. & Salzberg, S. L. Bracken: estimating species abundance in metagenomics data. *PeerJ Comput. Sci.* **3**, e104 (2017). https://doi.org/10.7717/peerj-cs.104


## Public data & benchmarks

51. Sczyrba, A. *et al.* Critical Assessment of Metagenome Interpretation—a benchmark of metagenomics software. *Nat. Methods* **14**, 1063–1071 (2017). https://doi.org/10.1038/nmeth.4458

52. Meyer, F. *et al.* Critical Assessment of Metagenome Interpretation: the second round of challenges. *Nat. Methods* **19**, 429–440 (2022). https://doi.org/10.1038/s41592-022-01431-4

53. Fritz, A. *et al.* CAMISIM: simulating metagenomes and microbial communities. *Microbiome* **7**, 17 (2019). https://doi.org/10.1186/s40168-019-0633-6

54. Meyer, F. *et al.* AMBER: Assessment of Metagenome BinnERs. *GigaScience* **7**, giy069 (2018). https://doi.org/10.1093/gigascience/giy069

55. Meyer, F. *et al.* Assessing taxonomic metagenome profilers with OPAL. *Genome Biol.* **20**, 51 (2019). https://doi.org/10.1186/s13059-019-1646-y

56. Meyer, F. *et al.* CAMI Benchmarking Portal: online evaluation and ranking of metagenomic software. *Nucleic Acids Res.* **53**, W102–W109 (2025). https://doi.org/10.1093/nar/gkaf369

57. Parks, D. H. *et al.* GTDB release 10: a complete and systematic taxonomy for 715 230 bacterial and 17 245 archaeal genomes. *Nucleic Acids Res.* **54**, D743–D754 (2026). https://doi.org/10.1093/nar/gkaf1040

58. Fullam, A. *et al.* proGenomes4: providing 2 million accurately and consistently annotated high-quality prokaryotic genomes. *Nucleic Acids Res.* (2025). https://doi.org/10.1093/nar/gkaf1208

59. Kanehisa, M., Sato, Y., Kawashima, M., Furumichi, M. & Tanabe, M. KEGG as a reference resource for gene and protein annotation. *Nucleic Acids Res.* **44**, D457–D462 (2016). https://doi.org/10.1093/nar/gkv1070

60. Sun, Z. *et al.* Challenges in benchmarking metagenomic profilers. *Nat. Methods* **18**, 618–626 (2021). https://doi.org/10.1038/s41592-021-01141-3


## Platforms, ANI, viruses, plasmids, simulation & DL binning

61. Eren, A. M. *et al.* Anvi'o: an advanced analysis and visualization platform for 'omics data. *PeerJ* **3**, e1319 (2015). https://doi.org/10.7717/peerj.1319

62. Woodcroft, B. J. *et al.* Comprehensive taxonomic identification of microbial species in metagenomic data using SingleM and Sandpiper. *Nat. Biotechnol.* (2025). https://doi.org/10.1038/s41587-025-02738-1

63. Jang, H. B. *et al.* Taxonomic assignment of uncultivated prokaryotic virus genomes is enabled by gene-sharing networks. *Nat. Biotechnol.* **37**, 632–639 (2019). https://doi.org/10.1038/s41587-019-0100-8

64. Bolduc, B. *et al.* Machine learning enables scalable and systematic hierarchical virus taxonomy. *Nat. Biotechnol.* (2025). https://doi.org/10.1038/s41587-025-02946-9

65. Zou, B. *et al.* A multi-modal deep language model for contaminant removal from metagenome-assembled genomes. *Nat. Mach. Intell.* **6**, 1245–1255 (2024). https://doi.org/10.1038/s42256-024-00908-5

66. Jain, C., Rodriguez-R, L. M., Phillippy, A. M., Konstantinidis, K. T. & Aluru, S. High throughput ANI analysis of 90K prokaryotic genomes reveals clear species boundaries. *Nat. Commun.* **9**, 5114 (2018). https://doi.org/10.1038/s41467-018-07641-9

67. Noronha, A. *et al.* The Virtual Metabolic Human database: integrating human and gut microbiome metabolism with nutrition and disease. *Nucleic Acids Res.* **47**, D614–D624 (2019). https://doi.org/10.1093/nar/gky992

68. Gourlé, H., Karlsson-Lindsjö, O., Hayer, J. & Bongcam-Rudloff, E. Simulating Illumina metagenomic data with InSilicoSeq. *Bioinformatics* **35**, 521–522 (2019). https://doi.org/10.1093/bioinformatics/bty630

69. Piera Líndez, P. *et al.* Accurate plasmid reconstruction from metagenomics data using assembly–alignment graphs and contrastive learning. *Nat. Biotechnol.* (2026). https://doi.org/10.1038/s41587-026-03005-7

70. Piera Líndez, P. *et al.* Adversarial and variational autoencoders improve metagenomic binning. *Commun. Biol.* **6**, 1073 (2023). https://doi.org/10.1038/s42003-023-05452-3

71. Kutuzova, S. *et al.* Improving metagenome binning by integrating intrinsic features and taxonomy. *Nat. Biotechnol.* (2026). https://doi.org/10.1038/s41587-026-03098-0

72. Wang, Z. *et al.* MetaBinner: a high-performance and stand-alone ensemble binning method to recover individual genomes from complex microbial communities. *Genome Biol.* **24**, 1 (2023). https://doi.org/10.1186/s13059-022-02832-6

73. Shen, W., Lees, J. A. & Iqbal, Z. Efficient sequence alignment against millions of prokaryotic genomes with LexicMap. *Nat. Biotechnol.* (2025). https://doi.org/10.1038/s41587-025-02812-8


## AI / genomic & protein language models

74. Cornman, A. *et al.* The OMG dataset: An Open MetaGenomic corpus for mixed-modality genomic language modeling. *bioRxiv* https://doi.org/10.1101/2024.08.14.607850 (2024).

75. Liu, W. *et al.* PLMSearch: Protein language model powers accurate and fast sequence search for remote homology. *Nat. Commun.* **15**, 2775 (2024). https://doi.org/10.1038/s41467-024-46808-5

76. Hamamsy, T. *et al.* Protein remote homology detection and structural alignment using deep learning. *Nat. Biotechnol.* **42**, 975–985 (2024). https://doi.org/10.1038/s41587-023-01917-2

77. Zhang, R., Mirdita, M. & Söding, J. De novo discovery of conserved gene clusters in microbial genomes with Spacedust. *Nat. Methods* (2025). https://doi.org/10.1038/s41592-025-02816-x

78. Han, W. *et al.* AlphaGEM enables precise genome-scale metabolic modelling by integrating protein structure alignment with deep-learning-based dark metabolism mining. *Nat. Commun.* (2026). https://doi.org/10.1038/s41467-026-75549-w

79. Palsson, B. O., Lee, S. Y. & Kim, G. B. Approaches for accelerating microbial gene function discovery using artificial intelligence. *Nat. Microbiol.* (2025). https://doi.org/10.1038/s41564-025-02214-1

## Structure search (Steinegger / Söding stack)

80. van Kempen, M. *et al.* Fast and accurate protein structure search with Foldseek. *Nat. Biotechnol.* **42**, 243–246 (2024). https://doi.org/10.1038/s41587-023-01773-0

81. Kim, W. *et al.* Rapid and sensitive protein complex alignment with Foldseek-Multimer. *Nat. Methods* **22**, 469–472 (2025). https://doi.org/10.1038/s41592-025-02593-7

82. Kim, H., Kim, R. S., Mirdita, M., Yoon, J. & Steinegger, M. Structural motif search across the protein universe with Folddisco. *Nat. Biotechnol.* (2026). https://doi.org/10.1038/s41587-026-03162-9

83. Barrio-Hernandez, I. *et al.* Clustering predicted structures at the scale of the known protein universe. *Nature* **622**, 637–645 (2023). https://doi.org/10.1038/s41586-023-06510-w

## Homology search (vector DB & phylogeny-compressed)

84. Jiang, Y. *et al.* Scalable homology detection with ERAST. *Nat. Biotechnol.* (2026). https://doi.org/10.1038/s41587-026-03051-1

85. Břinda, K. *et al.* Efficient and robust search of microbial genomes via phylogenetic compression. *Nat. Methods* **22**, 692–697 (2025). https://doi.org/10.1038/s41592-025-02625-2

## Phylogenomics

86. Minh, B. Q. *et al.* IQ-TREE 2: new models and efficient methods for phylogenetic inference in the genomic era. *Mol. Biol. Evol.* **37**, 1530–1534 (2020). https://doi.org/10.1093/molbev/msaa015

87. Price, M. N., Dehal, P. S. & Arkin, A. P. FastTree 2 — approximately maximum-likelihood trees for large alignments. *PLoS ONE* **5**, e9490 (2010). https://doi.org/10.1371/journal.pone.0009490

88. Asnicar, F. *et al.* Precise phylogenetic analysis of microbial isolates and genomes from metagenomes using PhyloPhlAn 3.0. *Nat. Commun.* **11**, 2500 (2020). https://doi.org/10.1038/s41467-020-16366-7

89. Shan, Y. *et al.* Alignment-free phylogenetic inference via hyperbolic protein language models. *bioRxiv* https://doi.org/10.64898/2026.05.26.723419 (2026).


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
