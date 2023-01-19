# Linux bash scripts used in this study

## Generation of the GTEx gene model
We used TransDecoder (version 5.5.0) (https://github.com/TransDecoder/TransDecoder) was used to find the coding sequences from the GTEx model.

The GTEx model can be found in the [Zenodo](https://zenodo.org/record/7014020).

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

## Mass spectrometry (MS) raw data pre-processing
Sample script to convert MS raw data to mzML format.
```bash
msconvert $FILE_RAW -o $FOLDER_OUT --mzML --filter "msLevel 2-" --inten32 –zlib
```
Sample script to convert mzML file to MGF format.
```bash
msconvert $FILE_mzML -o $FOLDER_OUT --mgf --filter "peakPicking true 1-" --mz64 --inten32 --filter "zeroSamples removeExtra" -g
```
