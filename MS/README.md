# Mass spectrometry

## MS data
Filtering process for MS data from PRIDE
<!-- ![filtering process for MS data from PRIDE](MS.png) -->
<img src="MS.png" width="300">

## Mass spectrometry (MS) raw data pre-processing
Sample script to convert MS raw data to mzML format.
```bash
msconvert $FILE_RAW -o $FOLDER_OUT --mzML --filter "msLevel 2-" --inten32 –zlib
```
Sample script to convert mzML file to MGF format.
```bash
msconvert $FILE_mzML -o $FOLDER_OUT --mgf --filter "peakPicking true 1-" --mz64 --inten32 --filter "zeroSamples removeExtra" -g
```
## MS database search

### Comet param files
Need to pay attention to the comet versions. There might be some change if different version of Comet was used.

The parameters were consistent for most versions. There might be some tiny changes, but for the versions we used, we didn't find any differences.

File `comet.params.decoy.HCD` was used in the first round of MS/MS search to select MS runs and PRIDE projects.

File `comet.params.NoDecoySearch.NoCut.HCD` was used in the second round of MS/MS search to select candidate novel peptides and the third round of MS/MS search to identify novel peptides. "No_cut" was defined in this file with a non-existing amino acid "Z". This option was added in later version of Comet.

The settings are: 10 ppm (parts per million) for precursor tolerance, 0.02 Da (Dalton) for MS/MS fragment tolerance, trypsin as the digestion enzyme with maximum 2 missed cleavages allowed. The fixed modification was carbamidomethyl (+57.02146) for all cysteines. The variable modifications were oxidation of methionine (+15.9949), N-terminal acetylation (+42.010565), N-terminal carbamidomethyl (+57.02146), deamidation of asparagine and glutamine residues (+0.98402), oxidation of methionine (+15.9949), and N-terminal conversion of glutamine and glutamic acid to pyro-glutamine (-17.026549, -18.010565)

### First round of MS search
Run Comet with GENCODE gene model and common contaminant proteins (protein group C) as protein database.
```bash
comet -P$FILE_COMET_PARAMS -D$FILE_PROTEIN_DATABASE $FILE_mzML
```
Here, `FILE_COMET_PARAMS` is file [`comet.params.decoy.HCD`](comet.params.decoy.HCD), `FILE_PROTEIN_DATABASE` is files of protein sequences.

The accuracy of peptide-spectrum matches (PSMs) was evaluated with Percolator (v3.04) for each MS run.
```bash
cat $ MS_RUN_NAME.pin | percolator - --testFDR 0.01 --trainFDR 0.01 --maxiter 20 --num-threads 12 --protein-enzyme "trypsin" -Y -P DECOY_ --results-psms $MS_RUN_NAME.target.psms.txt --decoy-results-psms /dev/null --results-peptides $MS_RUN_NAME.target.peptides.txt --decoy-results-peptides /dev/null
```
Here `MS_RUN_NAME` is the MS run name. `$MS_RUN_NAME.pin` is the output of Comet. `$MS_RUN_NAME.target.psms.txt` and `$MS_RUN_NAME.target.peptides.txt` is the output of Percolator. Other outputs were set to `/dev/null` as they were not used.

### Second round of MS search
#### Index the searching database
```bash
comet -P$FILE_COMET_PARAMS -D$FILE_PROTEIN_DATABASE -i
```
Here, `FILE_COMET_PARAMS` is file [`comet.params.NoDecoySearch.NoCut.HCD`](comet.params.NoDecoySearch.NoCut.HCD). The modifications and other settings were the same as in the first round of MS search, but the “No_cut” option instead of “Trypsin” digestion was enabled. 

`FILE_PROTEIN_DATABASE` is the protein sequences used as the searching database. To reduce the indexed database size, every 10,000 peptides from different peptide groups (peptide groups C, R, F, N, W, and decoy peptides) were joined to create pseudo-protein sequences with “\*” symbol (Comet would treat “\*” as the cutting site), and the protein names were assigned with unique names to represent their peptide groups.

#### Search against the indexed database
Each mzML file were searched against 5 different databases.
```bash
comet -P$FILE_COMET_PARAMS -D$FILE_INDEXED_PROTEIN_DATABASE $FILE_mzML
```
`FILE_INDEXED_PROTEIN_DATABASE` is the indexed protein database file.  
`FILE_mzML` is the MS data in mzML format.

#### Evaluate accuracy of MS database search
The accuracy of peptide-spectrum matches (PSMs) was evaluated with Percolator (v3.04) for different searching results of each MS run. The scripts were similar to the first round. 

Here, because "No_cut" is used, and the output of Comet does not include labeling for decoy matches. To run Percolator, the “pin” files, output of Comet, were modified so that PSMs with peptides from the decoy databases would have a “-1” value in the “Label” column to indicate that the peptides were from the decoy databases.

### Third round of MS search
15 searching database were created.
Peptides from peptide groups N and W were filtered based on searching result of the second round of MS search.

To create the searching databases, the target database could be pepCRF (peptide groups C, R, and F, the same below), or pepCRFNW.

The decoy database could be decoy pepCRF(1-5, for five distinct decoy databases) or decoy pepCRFNW.

The 15 searching databases were:
* pepCRF + decoy pepCRF(1-5)
* pepCRF + decoy pepCRFNW(1-5)
* pepCRFNW + decoy pepCRFNW(1-5)

The "pepCRFNW + decoy pepCRFNW(1-5)" were used to identify spectrums that matches with peptide groups N and W, to identify new proteins. The other ten databases were used as control, so that the spectrums do not match with known peptides.

MS database search was performed similar the second round of MS search. 

For PSM evaluation, to reduce the fluctuation of q-values caused by small sample size of each MS run, the accuracy of PSMs was evaluated with Percolator on each PRIDE project. For each of the 15 target-decoy databases, the Comet outputs from the same PRIDE projects were combined, with the “Label” column values changed to “-1” for decoy peptides. Among all PRIDE projects, the combined files were too large and they were equally divided into 2 to 4 groups to run Percolator.

## FDR control and identification of novel peptides
Three filtering standards (relaxed, stringent, and strictest) were used to select candidate novel peptides.

Novel peptides identified under the stringent and strictest standards were a subset of those under the relaxed standard.

## Novel peptide identification with PepQuery
The inputs for PepQuery were a file with possible novel peptides to check, a MGF file with spectra from novel peptides, and a reference protein database to exclude the possibility that the spectrum could match known proteins with unrestricted post-translational modifications. The inputs were prepared as described in the manuscript.
```bash
java -jar pepquery-1.6.2.jar -o $OUTPUT_FOLDER -prefix $OUTPUT_PREIFX -tol 10 -tolu ppm -itol 0.05 -cpu 24 -fragmentMethod 1 -minCharge 2 -maxCharge 4 -n 1000 -pep $FILE_PEP -ms $FILE_MGF -db $FILE_PROTEIN_DB -fixMod 6 -varMod 117,158,159,21,80,77 -um
```
The output of PepQuery included a column of “confident” with “Yes” or “No” to indicate if a PSM identified a novel peptide reliably. 
