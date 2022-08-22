import pandas as pd
from Bio import SeqIO
from Bio import Seq
from multiprocessing import Pool
from Bio import pairwise2

# the two files were downloaded from circAtlas 2.0. link: http://159.226.67.237:8080/new/links.php
fileC_bed = '/data/pub/circRNA/circAtlas/human_bed_v2.0.txt.gz'
fileC_seq = '/data/pub/circRNA/circAtlas/human_sequence_v2.0.txt.gz'

df_Cbed = pd.read_csv(fileC_bed, sep='\t')#580718, 580718 unique Name
df_Cseq = pd.read_csv(fileC_seq, sep='\t',header=None)#578933, 578933 unique Name.
df_Cseq.columns = ['species','Name','seq']
# check those with seq
df_Cjoin = df_Cbed.merge(df_Cseq[df_Cseq['seq'] != 'partial'], on = 'Name',how='inner')#511723
df_Cjoin['seqlen'] = df_Cjoin['seq'].str.len()# all less than 2000bp
df_Cjoin['spanLen'] = df_Cjoin.End - df_Cjoin.Start# some longer than 100,000 bp. 
(df_Cjoin['spanLen'] == df_Cjoin['seqlen']).sum()#20. the bed file, Start and End is much longer than the seqlen. seq is the mature sequence.
(df_Cjoin.spanLen/df_Cjoin.seqlen).mean()#94.34

# 6 frame translation
# seq = df_Cjoin.iloc[0].seq
# min_protein = 30
# requireM = True
# max_circle = 10
def translateCircRNA(seq, min_protein=30, max_circle=10, requireM=True):

    seqlen = len(seq)
    len_keep = seqlen * max_circle - seqlen * max_circle % 3
    seq1 = seq*10
    seq1 = Seq.Seq(seq1)
    seq2 = seq1[1:]+seq1[:1]
    seq3 = seq1[2:] + seq1[:2]
    seqs_f = [seq1, seq2, seq3]
    seqs_all = [e.reverse_complement() for e in seqs_f] + seqs_f
    seqs_all = [e[:len_keep] for e in seqs_all]
    seqs_translation = [e.translate() for e in seqs_all]
    seqs_translation_concat = '*'.join(str(e) for e in seqs_translation)
    if requireM:
        seqs_translation_concat = seqs_translation_concat.replace('M', '*M')
        seqs_keep  = sorted(set([i for i in seqs_translation_concat.split('*') if len(i) >= min_protein and i.startswith('M')]))
    else:
        seqs_keep  = sorted(set([i for i in seqs_translation_concat.split('*') if len(i) >= min_protein]))
    return seqs_keep

# translate circRNA

pool = Pool()
results = pool.starmap(translateCircRNA,[(seq, 30, 10, True) for seq in df_Cjoin['seq']])
pool.close()
pool.join()
df_Cjoin['Protein'] = results

# save translated sequences
file_protein = '/data/pub/circRNA/circAtlas/human_sequence_v2.0.translation.30AA.protein.fa'
f = open(file_protein, 'w')
for Name, Protein in zip(df_Cjoin['Name'], df_Cjoin['Protein']):
    for n, pr in enumerate(Protein):
        f.write('>{}.{}\n{}\n'.format(Name,n+1,pr))
f.close()

# save sequence to fasta format
file_CircSeq = '/data/pub/circRNA/circAtlas/human_sequence_v2.0.seq.fa'
f = open(file_CircSeq, 'w')
for Name, seq in zip(df_Cjoin['Name'], df_Cjoin['seq']):
    f.write('>{}\n{}\n'.format(Name,seq))
f.close()