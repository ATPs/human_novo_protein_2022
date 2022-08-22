# blast search

## nr

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


## UniProt
Similar to nr.

## SwissProt
Search with BLASTP directly.
