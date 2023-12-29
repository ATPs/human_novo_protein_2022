# A massive proteogenomic screen identifies thousands of novel peptides from the human “dark” proteome

## ncORF web
Visit https://ncorf.genes.fun/

Users may check existence of novel peptides in proteins they are interested in.

If the website does not load, there may be an unstable internet connection. In this case, it is advisable to attempt accessing the website at a later time. However, if the issue persists, it is recommended to contact the author to resolve the issue.

## Data used in this project was saved in Zenodo (https://zenodo.org/record/10417233).

<details open>
  <summary>Files include:</summary>


* ALL.combined.gtf.gz 
    * GTF file modeled from GTEx RNA-seq data. Provided by Dr. Mihaela Pertea and Dr. Steven L. Salzberg and generated in the [CHESS paper](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-018-1590-2).
* ALL.info.gz 
  * Transcript annotations. Provided by Dr. Mihaela Pertea and Dr. Steven L. Salzberg and generated in the [CHESS paper](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-018-1590-2).
* GTEx_StringTie_proteins_dedup.1MSrelaxedPep.fa.gz
  * Proteins translated from genes modeled from the GTEx data with StringTie, with at least one peptide evidence from mass spectrometry data.
* GTEx_StringTie_proteins_dedup.fa.gz
  * Proteins translated from genes modeled from the GTEx data with StringTie. Proteins were deduplicated as described in the manuscript methods.
* GTEx_StringTie_proteins_dedup.protein_in_genome.gff3
  *  GFF3 file with the location of proteins in file **GTEx_StringTie_proteins_dedup.fa.gz**.
* PepQuery.MGF.tar.gz
  * MGF files used for validation with PepQuery.
* Table_S4_peptides.info.tsv.gz
  * Novel peptides in table S4 of the manuscript with additional annotations. Columns are:
    * **peptide**: peptide sequence detected in peptide-spectrum matches (PSMs).
    * **pep_group**: peptide group. "N" and "W". "N" for those translated from GTEx transcripts directly. "W" for proteins altered with gnomAD common alleles.
    * **peptide_before_gnomAD**: peptide sequence before adding 
    * **genome_location_chr**: genomic location of peptide in genome. e.g., "chr16|+|50153490|50153549" means chromosome 16, + strand, 50153490 to 50153549. 
    * **protein_id_best**: the representative protein ID that contribute to the peptide sequence.
    * **gene_id_best**: gene ID based on **protein_id_best**.
    * **psms|q-value|min**: minumum q-value for PSMs with the novel peptide calculated by Percolator.
    * **peptides|q-value|min**: minimum q-value for peptide sequences calculated by Percolator.
    * **GENCODE|group**: relative location of peptides to GENCODE gene models. Values could be 'All_intron', 'All_intergene', 'All_UTR', 'All_exon_noncoding', 'All_transcript_coding', 'All_CDS', 'All_exon_coding', 'other', 'All_transcript_noncoding', 'All_transcript'.
    * **spectrums**: Spectrums matches with the peptides. The IDs look like "26N1_31599,1G48_65306", where "26N1" is the MS run ID in table S3 of the manuscript and "31599" 
    * **relaxed**, **stringent**, **strictest**, **relaxed|PepQuery**, **stringent|PepQuery**, **strictest|PepQuery**, : value could be 0 or 1. Different filtering standards. `HUPO` stands for the "Human Proteome Organization", which designs the HPP (Human Proteome Project) guidelines. `HUPO` means the `HPP` filtering standard.
    * **identified_in_SmProt**: the peptide is identified in [SmProt](http://bigdata.ibp.ac.cn/SmProt/). 
    * **identified_in_OpenProt**: the peptide is identified in [OpenProt](https://openprot.org/). Peptide in OpenProt were found from links like [IP_591792](https://openprot.org/p/altorfDbView/79/43726886/591792/IP_591792/2/msDetectionDetail). 
    * **identified_in_Science**: the peptide is identified in the Science paper, *Chen, J. et al. Pervasive functional translation of noncanonical human open reading frames. Science 367, 1140-1146 (2020).*
    * **identified_in_breast_cancer**, **identified_in_breast_cancer_pepquery**: the peptide were identified in the paper, *Hari PS, Balakrishnan L, Kotyada C, Everad John A, Tiwary S, Shah N, Sirdeshmukh R. Proteogenomic Analysis of Breast Cancer Transcriptomic and Proteomic Data, Using De Novo Transcript Assembly: Genome-Wide Identification of Novel Peptides and Clinical Implications. Mol Cell Proteomics. 2022 Apr;21(4):100220. doi: 10.1016/j.mcpro.2022.100220IF: 7.0 Q1 . Epub 2022 Feb 26. PMID: 35227895; PMCID: PMC9020135.*. **identified_in_breast_cancer_pepquery**, peptide passed PepQuery Quality Control in the paper.
* Table_S5_proteins.info.tsv.gz
  * Novel proteins in table S5 of the manuscript with additional annotations. Columns are:
    * **protein_id**: novel protein ID.
    * **gene_id**: gene ID of the novel protein.
    * **protein_seq**: protein sequence.
    * **novel_peptides_relaxed**: novel peptides (relaxed standard) that belongs to the protein.
    * **protein_id_homolog**: homologs of the protein based on homologous search.
    * **protein_name_homolog**: protein description of the homolog protein.
    * **species_homolog**: species of the homolog protein.
    * **GENCODE|group**: relative location of peptides to GENCODE gene models. Values could be 'All_intron', 'All_intergene', 'All_UTR', 'All_exon_noncoding', 'All_transcript_coding', 'All_CDS', 'All_exon_coding', 'other', 'All_transcript_noncoding', 'All_transcript'.
    * **GENCODE_gene_id**: overlapped GENCODE gene ID in the genome.
    * **relaxed**, **stringent**, **strictest**, **relaxed|PepQuery**, **stringent|PepQuery**, **strictest|PepQuery**: value could be 0 or 1. Different filtering standards.
    * **OpenProt_accession_id**: OpenProt accession ID if the protein sequence is identified in [OpenProt](https://openprot.org/). 
* **Protein.interpro.domain.tsv.gz**: 
  * domain structures predicted by InterProScan v5.38 of proteins in `Table_S5_proteins.info.tsv.gz`. The meaning of each columns can be found: https://interproscan-docs.readthedocs.io/en/latest/OutputFormats.html.
* **CircAtlas2.0.human_sequence_v2.0.translation.30AA.protein.fa.gz**: 
  * protein sequences from circRNA 6-frame translation. cicrRNA sequences were downloaded from CircAtlas 2.0 database.
* **20231210NW_pep.pepquery.multiple.EachLoc.tsv.gz** peptides with more than one genomic location. 
* **20231210NW_pep.pepquery.other.tsv.gz** peptides that cannot be located to the chromosomes precisely. They may from scaffolds of the genome, or resulting from mutations other than amino acid substitution.
* **20231218Proteins_FromPepLocMultiple_info.AddBlastAndTaxon.AddGENOCDEloc.tsv.gz** proteins with peptides with more than one genomic location. For location of the peptide, one single representative protein was selected.

Other files and methods could be provided upon request.

## Identification of representative proteins and proteins passing the HPP Data Interpretation Guidelines 
**Table_S4_peptides.info.tsv.gz** and **Table_S5_proteins.info.tsv.gz**

Candidate novel peptides under the relaxed standard with a single location in chromosomes were selected. For peptides in the peptide group W, only those resulting from AA substitutions were kept. Peptides might belong to different proteins from different genes. To explain the observed peptides with the minimum number of proteins and genes, a single representative protein for each novel peptide was selected. The rules to select a representative protein for each novel peptide were: 1) for genes with the peptide, those with the largest counts of novel peptides were selected; 2) proteins from these genes with the largest counts of novel peptides were selected; 3) the longest protein was selected. Finally, the representative gene was determined by the representative protein. For a peptide with multiple loci, a representative protein was selected for each locus with the same procedures.

After a representative protein (referred to as novel protein below) was selected for each novel peptide, the proteins were checked if they met parts of the definition of a novel protein in the Mass Spectrometry Data Interpretation Guidelines 3.0 of HPP (33). The HPP guidelines require a novel protein containing either ≥ 2 distinct uniquely mapping, non-nested peptide sequences of length ≥ 9 AAs, or ≥ 2 nested peptides with a total length ≥ 18 AAs. 


</details>


## [Python_scripts](Python_scripts)
Python scripts used to process the data. Visit the folder for details. We used [Anaconda Python version 3.8](https://www.anaconda.com/products/distribution) under the Linux System. The scripts should work with Python versions >= 3.4 with required packages installed (Biopython, pandas, and etc.) and work with Linux, Windows or MacOS since Python and the required pacakges can be installed in these operating systems.

## [other_scripts](other_scripts)
Linux bash scripts used to process the data. Visit the folder for details.


## [MS](MS/)
MS data filtering and processing.

## [Fig_Data](Fig_Data/)
Some tables related to figures in the manuscript.

# Note
**`I` were changed to `L` in the stored Peptide sequences**.
 
