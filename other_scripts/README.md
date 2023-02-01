# Other scripts used in this study

## Generation of the GTEx gene model
We used [TransDecoder (version 5.5.0)](https://github.com/TransDecoder/TransDecoder) was used to find the coding sequences from the GTEx model.

The GTEx model can be found in the [Zenodo](https://zenodo.org/record/7014020).

To eliminate potential transcriptional noise, transcripts with the max Transcripts Per Million (TPM) values ≥ 2 among all GTEx RNA-seq samples and detected in ≥ 3 samples were kept.

Transcript sequences were acquired with the “gtf_genome_to_cdna_fasta.pl” tool in TransDecoder. 
```bash
util/gtf_genome_to_cdna_fasta.pl $FILE_GTF $FILE_GENOME >$FILE_TRANSCRIPT
```
The sample scripts for protein translation were shown below.

```bash
TransDecoder.LongOrfs -m 30 -t $FILE_TRANSCRIPT
TransDecoder.Predict -t $FILE_TRANSCRIPT
```

The genomic location of proteins were determined with the script below.
```bash
util/cdna_alignment_orf_to_genome_orf.pl $FILE_TRANSCRIPT.transdecoder.gff3 $FILE_GTF $FILE_TRANSCRIPT > $FILE_TRANSCRIPT.transdecoder.genome.gff3
```
where 
* `FILE_GTF`: the GTF file
* `FILE_GENOME`: the genome file
* `FILE_TRANSCRIPT`: the transcript file. It is also used as the output prefix for TransDecoder results, such as `$FILE_TRANSCRIPT.transdecoder.gff3`.

Proteins aligned to the genome by TransDecoder were combined for further analysis. We use CD-HIT to identify proteins which were identical or part of longer proteins. The command is shown below.
```bash
cd-hit -i $FILE_PROTEINS_COMBINED -o $OUTPUT_FILE_DEDUP_PROTEINS -c 1.0 -n 5 -M 250000 -T 28 -U 0 -s 0 -uL 0 -uS 0
```

## Translation of GTEx model directly
The GTEx model was also translated directly with TransDecoder.
The minimum protein length was set to 30.

## blast search
Sample scripts of how the homologous search was performed.

### nr

* The NCBI nr sequences were split to 500 parts.
* DIAMOND (v2.0.11)
  ```bash
  diamond makedb --in $FILE_PROTEIN_SEQ --db $FILE_PROTEIN_DB
  diamond blastp --db $FILE_PROTEIN_DB --query $FILE_PROTEIN_QEURY --ultra-sensitive --outfmt 6 \
    --out $FILE_OUTPUT --max-target-seqs 1 --evalue 0.00001 --block-size 20 --tmpdir $FOLDER_TEMP \
    --no-unlink --threads 12 --masking 0 --comp-based-stats 3
  ```
 * Each query protein, the best match protein in nr was selected based on the highest bitscore and combined.
 * BLASTP against best match proteins.
 * Calculate e-value against all nr sequences.
   * As the selected proteins from nr was a subset of the large databases, the e-values were smaller due to the smaller database size. The e-values against the entire nr were calculated by multiplying a ratio, which equaled the total length of proteins in nr dividing the total length of the selected nr proteins.


### UniProt
Similar to nr.

### SwissProt
Search with BLASTP directly.
