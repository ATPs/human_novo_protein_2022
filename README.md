# A massive proteogenomic screen identifies thousands of novel human protein coding sequences

## Data used in this project was saved in Zenodo (https://zenodo.org/record/7014020).

Files include:
* [ALL.combined.gtf.gz](#) GTF file modeled from GTEx RNA-seq data. Provided by Dr. Mihaela Pertea and Dr. Steven L. Salzberg and generated in the [CHESS paper](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-018-1590-2).
* [ALL.info.gz](#) Transcript annotations. Provided by Dr. Mihaela Pertea and Dr. Steven L. Salzberg and generated in the [CHESS paper](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-018-1590-2).
* [GTEx_StringTie_proteins_dedup.1MSrelaxedPep.fa.gz](#) Proteins translated from StringTie genes modeled from the GTEx data, with at least one peptide evidence from mass spectrometry data.
* [GTEx_StringTie_proteins_dedup.fa.gz](#) Proteins translated from StringTie genes modeled from the GTEx data. Proteins were deduplicated as described in the manuscript methods.
* [GTEx_StringTie_proteins_dedup.protein_in_genome.gff3](#) GFF3 file with the location of proteins in file [GTEx_StringTie_proteins_dedup.fa.gz](#).
* [PepQuery.MGF.tar.gz](#) MGF files used for validation with PepQuery.
* [Table_S4_peptides.info.tsv.gz](#) Novel peptides in table S4 of the manuscript with additional annotations. Columns are:
    * **peptide**: peptide sequence detected in peptide-spectrum matches (PSMs).
    * **pep_group**: peptide group. "N" and "W". "N" for those translated from GTEx StringTie transcripts directly. "W" for proteins altered with gnomAD common alleles.
    * **peptide_before_gnomAD**: peptide sequence before adding 
    * **genome_location_chr**: genomic location of peptide in genome. e.g., "chr16|+|50153490|50153549" means chromosome 16, + strand, 50153490 to 50153549. 
    * **protein_id_best**: the representative protein ID that contribute to the peptide sequence.
    * **gene_id_best**: gene ID based on **protein_id_best**.
    * **psms|q-value|min**: minumum q-value for PSMs with the novel peptide calculated by Percolator.
    * **peptides|q-value|min**: minimum q-value for peptide sequences calculated by Percolator.
    * **GENCODE|group**: relative location of peptides to GENCODE gene models. Values could be 'All_intron', 'All_intergene', 'All_UTR', 'All_exon_noncoding', 'All_transcript_coding', 'All_CDS', 'All_exon_coding', 'other', 'All_transcript_noncoding', 'All_transcript'.
    * **spectrums**: Spectrums matches with the peptides. The IDs look like "26N1_31599,1G48_65306", where "26N1" is the MS run ID in table S3 of the manuscript and "31599" 
    * **relaxed**, **stringent**, **strictest**, **relaxed|PepQuery**, **stringent|PepQuery**, **strictest|PepQuery**, **HUPO|relaxed**, **HUPO|stringent**, **HUPO|strictest**, **HUPO|relaxed|PepQuery**, **HUPO|stringent|PepQuery**, **HUPO|strictest|PepQuery**: value could be 0 or 1. Different filtering standards.
* [Table_S5_proteins.info.tsv.gz](#) Novel proteins in table S5 of the manuscript with additional annotations. Columns are:
    * **protein_id**: novel protein ID.
    * **gene_id**: gene ID of the novel protein.
    * **protein_seq**: protein sequence.
    * **novel_peptides_relaxed**: novel peptides (relaxed standard) that belongs to the protein.
    * **protein_id_homolog**: homologs of the protein based on homologous search.
    * **protein_name_homolog**: protein description of the homolog protein.
    * **species_homolog**: species of the homolog protein.
    * **GENCODE|group**: relative location of peptides to GENCODE gene models. Values could be 'All_intron', 'All_intergene', 'All_UTR', 'All_exon_noncoding', 'All_transcript_coding', 'All_CDS', 'All_exon_coding', 'other', 'All_transcript_noncoding', 'All_transcript'.
    * **GENCODE_gene_id**: overlapped GENCODE gene ID in the genome.
    * **relaxed**, **stringent**, **strictest**, **relaxed|PepQuery**, **stringent|PepQuery**, **strictest|PepQuery**, **HUPO|relaxed**, **HUPO|stringent**, **HUPO|strictest**, **HUPO|relaxed|PepQuery**, **HUPO|stringent|PepQuery**, **HUPO|strictest|PepQuery**: value could be 0 or 1. Different filtering standards.
* [Protein.interpro.domain.tsv.gz](#): domain structures predicted by InterProScan v5.38 of proteins in `Table_S5_proteins.info.tsv.gz`. The meaning of each columns can be found: https://interproscan-docs.readthedocs.io/en/latest/OutputFormats.html.
* [CircAtlas2.0.human_sequence_v2.0.translation.30AA.protein.fa.gz](): protein sequences from circRNA 6-frame translation. cicrRNA sequences were downloaded from CircAtlas 2.0 database.
Other files and methods could be provided upon request.

## [Python_scripts](https://github.com/ATPs/human_novo_protein_2021/tree/main/Python_scripts)
Python scripts used to process the data. Visit the folder for details.

## [blast](https://github.com/ATPs/human_novo_protein_2021/blob/main/blast/blast_search.md)
Sample scripts of how the homologous search was performed.

# Note
**`I` were changed to `L` in the stored Peptide sequences**.
 
