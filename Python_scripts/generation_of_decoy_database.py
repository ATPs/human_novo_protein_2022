from Bio import SeqIO
import os
import time
import numpy as np
from multiprocessing import Pool
from itertools import product

# file_in is the input of target database
file_in = '/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201combined/20201201DB_All/20201201known.CONT.NEW.pep'

for n in range(5):
    time.sleep(2)# wait a few seconds so that the random seed for different run is different
    file_temp = '/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201combined/20201201DB_All/temp.{}.pep'.format(n+1)
    os.system(f'/gpfs/gpfs/scratch/xc278/p/mimic/mimic-master/src/mimic {file_in} > {file_temp} &')

seqs_in = set([str(e.seq) for e in SeqIO.parse(file_in,'fasta')])#25084095

def checkSimilarPep(seq):
    '''return '', if seq and any it's variants in in seqs_in. else return the seq
    I=L, N[Deamidated]=D, Q[Deamidated]=E, GG=N, Q≈K, F≈M[Oxidation]
    https://www.hupo.org/resources/Documents/HPPMSDataGuidelines_3.0.0.pdf
    ignore GG=N. ignore I=L as all I were changed to L.
    '''
    #dc = {'I':'IL', 'L':'IL', 'N':'ND','D':'ND', 'Q':'QEK','E':'QEK','K':'QEK','F':'FM','M':'FM'}
    dc = {'N':'ND','D':'ND', 'Q':'QE','E':'QE'}
    ln = [dc[e] if e in dc else e for e in seq]
    l2 = [e for e in ln if len(e) != 1]
    if len(l2) > 10:# do not check alternative AAs if number of alternative AAs >10
        if seq in seqs_in:
            return ''
        else:
            return seq
    ln = product(*ln)
    for e in ln:
        if ''.join(e) in seqs_in:
            return ''
    return seq

for n in range(5):
    file_temp = '/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201combined/20201201DB_All/temp.{}.pep'.format(n+1)
    file_out = '/gpfs/gpfs/project1/jx76-001/xc/MS/proteins/20201201combined/20201201DB_All/20201201DECOY.{}.pep'.format(n+1)
    seqs_decoy = [str(e.seq) for e in SeqIO.parse(file_temp,'fasta')]
    pool = Pool(36)
    results = pool.map(checkSimilarPep, seqs_decoy)
    #results = pool.map(checkIn, seqs_decoy)
    pool.close()
    pool.join()
    seqs_keep = set([e for e in results if e != ''])
    print(n, len(seqs_decoy), len(set(seqs_decoy)), len(seqs_keep), len(seqs_keep) / len(seqs_in))
    fout = open(file_out,'w')
    for i, s in enumerate(seqs_keep):
        seq_id = 'D_' + str(np.base_repr(i, 36))
        seq = s
        fout.write('>{}\n{}\n'.format(seq_id, seq))
    fout.close()
