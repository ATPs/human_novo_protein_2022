# modified from https://github.com/yafeng/trypsin/blob/master/trypsin.py

from Bio import SeqIO
import pandas as pd
import numpy as np
import glob

def TRYPSIN(proseq,miss_cleavage=2, peplen_min=6, peplen_max=40):
    '''
    code modified from
    https://github.com/yafeng/trypsin
    only return peptides >= peplen_min and <= peplen_max
    '''
    peptides=[]
    cut_sites=[0]
    for i in range(0,len(proseq)-1):
        if proseq[i]=='K' and proseq[i+1]!='P':
            cut_sites.append(i+1)
        elif proseq[i]=='R' and proseq[i+1]!='P':
            cut_sites.append(i+1)
    
    if cut_sites[-1]!=len(proseq):
        cut_sites.append(len(proseq))

    if len(cut_sites)>2:
        if  miss_cleavage==0:
            for j in range(0,len(cut_sites)-1):
                peptides.append(proseq[cut_sites[j]:cut_sites[j+1]])

        elif miss_cleavage==1:
            for j in range(0,len(cut_sites)-2):
                peptides.append(proseq[cut_sites[j]:cut_sites[j+1]])
                peptides.append(proseq[cut_sites[j]:cut_sites[j+2]])
            
            peptides.append(proseq[cut_sites[-2]:cut_sites[-1]])

        elif miss_cleavage==2:
            for j in range(0,len(cut_sites)-3):
                peptides.append(proseq[cut_sites[j]:cut_sites[j+1]])
                peptides.append(proseq[cut_sites[j]:cut_sites[j+2]])
                peptides.append(proseq[cut_sites[j]:cut_sites[j+3]])
            
            peptides.append(proseq[cut_sites[-3]:cut_sites[-2]])
            peptides.append(proseq[cut_sites[-3]:cut_sites[-1]])
            peptides.append(proseq[cut_sites[-2]:cut_sites[-1]])
    else: #there is no trypsin site in the protein sequence
        peptides.append(proseq)
    peptides = [e for e in peptides if len(e) >= peplen_min and len(e) <= peplen_max]
    return set(peptides)

# below are some protein sequences in fasta format.
file_ref = '/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201combined/20201201UniprotRefSeqGencodeHLAChessEnsemblCombined.fa'
file_new = '/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201combined/20201201ChessStringTieNovo.fa'
file_cont = '/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201combined/contaminants.fasta'
files_ref_gnomAD = glob.glob('/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201gnomADKnown/*.pergeno.protein_changed.fa')
files_new_gnomAD = glob.glob('/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201gnomADChessStringTie/*.pergeno.protein_changed.fa')


ls_ref = list(SeqIO.parse(file_ref,'fasta'))#168478
ls_new = list(SeqIO.parse(file_new, 'fasta'))#2698539
ls_cont = list(SeqIO.parse(file_cont, 'fasta'))#246
lsGnomAD_ref = [e for f in files_ref_gnomAD for e in SeqIO.parse(f,'fasta')]#428124
lsGnomAD_new = [e for f in files_new_gnomAD for e in SeqIO.parse(f,'fasta')]#2811005
# drop duplicates for lsGnomAD_ref and lsGnomAD_new
lsGnomAD_ref1 = list(dict([[str(e.seq), e] for e in lsGnomAD_ref]).values())#36988
lsGnomAD_new1 = list(dict([[str(e.seq), e] for e in lsGnomAD_new]).values())#496197

# get all peptides
pep_ref = set([i for e in ls_ref for i in TRYPSIN(str(e.seq).strip('*'),miss_cleavage=2, peplen_min=6, peplen_max=40)])#3093576
pep_cont = set([i for e in ls_cont for i in TRYPSIN(str(e.seq).strip('*'),miss_cleavage=2, peplen_min=6, peplen_max=40)])#23878
pep_new = set([i for e in ls_new for i in TRYPSIN(str(e.seq).strip('*'),miss_cleavage=2, peplen_min=9, peplen_max=40)])#22682004
pepGnomAD_ref = set([i for e in lsGnomAD_ref1 for i in TRYPSIN(str(e.seq).strip('*'),miss_cleavage=2, peplen_min=6, peplen_max=40)])#1084375
pepGnomAD_new = set([i for e in lsGnomAD_new1 for i in TRYPSIN(str(e.seq).strip('*'),miss_cleavage=2, peplen_min=9, peplen_max=40)])#5273826
# count new pep by gnomAD
pepGnomAD_ref1 = pepGnomAD_ref - pep_ref#44777
pepGnomAD_new1 = pepGnomAD_new - pep_new#1477314


# change all I to L in AA
pep_ref2 = set([e.upper().replace('I','L') for e in pep_ref])#3085376
pep_cont2 = set([e.upper().replace('I','L') for e in pep_cont])#23836
pep_new2 = set([e.upper().replace('I','L') for e in pep_new])#22663688
pepGnomAD_ref2 = set([e.upper().replace('I','L') for e in pepGnomAD_ref1]) - pep_ref2#44506
pepGnomAD_new2 = set([e.upper().replace('I','L') for e in pepGnomAD_new1]) - pep_new2#1469859

# non-overlap pep
pep_cont3 = pep_cont2#23836
pep_ref3 = pep_ref2 - pep_cont3#3076726
pepGnomAD_ref3 = (pepGnomAD_ref2 - pep_ref3) - pep_cont3#44409
pep_new3 = ((pep_new2 - pepGnomAD_ref3) - pep_ref3) - pep_cont3#20567934
pepGnomAD_new3 = pepGnomAD_new2 - pep_new3 - pepGnomAD_ref3 - pep_ref3 - pep_cont3#1371190

# save 
file_db_ref = '/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201combined/20201201DB_Ref/20201201known.CONT.pep'
fout = open(file_db_ref,'w')
for n, pep in enumerate(pep_cont3):
    seq_id = 'C_' + str(np.base_repr(n, 36))
    fout.write('>{}\n{}\n'.format(seq_id, pep))
for n, pep in enumerate(pep_ref3):
    seq_id = 'R_' + str(np.base_repr(n, 36))
    fout.write('>{}\n{}\n'.format(seq_id, pep))
for n, pep in enumerate(pepGnomAD_ref3):
    seq_id = 'F_' + str(np.base_repr(n, 36))
    fout.write('>{}\n{}\n'.format(seq_id, pep))
fout.close()

file_db_ref = '/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201combined/20201201DB_All/20201201known.CONT.NEW.pep'
fout = open(file_db_ref,'w')
for n, pep in enumerate(pep_cont3):
    seq_id = 'C_' + str(np.base_repr(n, 36))
    fout.write('>{}\n{}\n'.format(seq_id, pep))
for n, pep in enumerate(pep_ref3):
    seq_id = 'R_' + str(np.base_repr(n, 36))
    fout.write('>{}\n{}\n'.format(seq_id, pep))
for n, pep in enumerate(pepGnomAD_ref3):
    seq_id = 'F_' + str(np.base_repr(n, 36))
    fout.write('>{}\n{}\n'.format(seq_id, pep))
for n, pep in enumerate(pep_new3):
    seq_id = 'N_' + str(np.base_repr(n, 36))
    fout.write('>{}\n{}\n'.format(seq_id, pep))
for n, pep in enumerate(pepGnomAD_new3):
    seq_id = 'W_' + str(np.base_repr(n, 36))
    fout.write('>{}\n{}\n'.format(seq_id, pep))
fout.close()

