# Python scripts used to process the data

Python scripts were run interactively in iPython console. The input and output were included in the scripts.

## *in silico* digesion of protein sequences

modified from https://github.com/yafeng/trypsin/blob/master/trypsin.py

sample code in [Trypsin.py](https://github.com/ATPs/human_novo_protein_2021/blob/main/Python_scripts/Trypsin.py)

## generation of decoy database
In-house Python scripts were used to remove peptides in the decoy database that are the same to peptides in the target database. 

A peptide in the decoy database was also removed if any of its possible variants considering amino acid N=D, Q=E was found in the target database, because N[Deamidated]=D, Q[Deamidated]=E in MS search. For example, peptide AANQ was found in the target database, its variants (AADQ, AANE, and AADE) would be removed from the decoy database.

sample code in
[generation_of_decoy_database.py](https://github.com/ATPs/human_novo_protein_2021/blob/main/Python_scripts/generation_of_decoy_database.py)

## combine comet pin for each project
sample code in
[combine_comet_pin_for_each_project.py](https://github.com/ATPs/human_novo_protein_2021/blob/main/Python_scripts/combine_comet_pin_for_each_project.py)

After running comet, Percolator was run based on each PRIDE project. We need to combine the output files of comet (.pin files) from the same project.

## circRNA
### 6-frame translation of circRNA
circRNA bed file and sequence of Human were downloaded from circAtlas 2.0 database: http://159.226.67.237:8080/new/links.php
sample code in [circRNA.six_frame_translation.py](https://github.com/ATPs/human_novo_protein_2021/blob/main/Python_scripts/circRNA.six_frame_translation.py)


## other code
other Python scripts were highly relied on the data and the HPC system that were used and can be provided upon request.

