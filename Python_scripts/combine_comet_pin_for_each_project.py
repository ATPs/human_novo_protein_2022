import gzip
import glob
import os
import numpy as np
from multiprocessing import Pool
import pandas as pd

# filename = '/gpfs/gpfs/staging/jx76-003/xc/MS/20210118Comet/known.join.DECOY.1.fa/PXD000004/4A.pin.gz'

# folder = '/gpfs/gpfs/staging/jx76-003/xc/MS/20210118Comet/known.join.DECOY.2.fa/PXD010154/'
# outprefix = '/gpfs/gpfs/staging/jx76-003/xc/MS/20210118Comet/20210122percolator_known.join.DECOY.2.fa/PXD010154'
max_size = 4e9
df = pd.DataFrame()
df['folder_pin'] = glob.glob('/gpfs/gpfs/staging/jx76-003/xc/MS/20210118Comet/known.*.fa/PXD*')
df['project_id'] = df['folder_pin'].apply(os.path.basename)
df['DB'] = df['folder_pin'].apply(lambda x: os.path.basename(os.path.dirname(x)))
df['percolator_prefix'] = df.apply(lambda x:os.path.join('/gpfs/gpfs/staging/jx76-003/xc/MS/20210118Comet', '20210214percolatorY_'+x['DB'], x['project_id']), axis=1)
# get folder_pin size
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


pool = Pool()
df['pin_size'] = pool.map(get_size, list(df['folder_pin']))
pool.close()
pool.join()

# get projects with at least one file greater than max_size
projects_large = set(df[df['pin_size'] >= max_size]['project_id'])#28

# get projects to split
df_work = df[df['project_id'].isin(projects_large)].copy()#420

# get projects with medium size, max_size/4
projects_medium = set(df[df['pin_size'] >= max_size/4]['project_id']) - projects_large#106
projects_small = set(df['project_id']) - projects_medium - projects_large #791

# generate scripts to run percolator for projects_medium, projects_small
df_small = df[df['project_id'].isin(projects_small)]#11865
df_medium = df[df['project_id'].isin(projects_medium)]#1590

cmd = 'python /home1/xc278/w/GitHub/xiaolongTools/Rutgers/MS/20210214runPercolator_Y.py {folder_pin}'
open('/gpfs/gpfs/staging/jx76-003/xc/MS/20210118Comet/20210224percolatorCombineRun_small.cmd','w').write('\n'.join(cmd.format(folder_pin = folder_pin) for folder_pin in df_small['folder_pin']) + '\n')
df_medium = df_medium.sort_values(by='pin_size')
open('/gpfs/gpfs/staging/jx76-003/xc/MS/20210118Comet/20210224percolatorCombineRun_medium.cmd','w').write('\n'.join(cmd.format(folder_pin = folder_pin) for folder_pin in df_medium['folder_pin']) + '\n')


# generate scripts to run percolator for large files
# get parts for projects
dc_project2parts = df_work.groupby(['project_id','DB'])['pin_size'].apply(lambda x:int(np.ceil(x.sum()/max_size))).to_frame().reset_index().groupby('project_id')['pin_size'].max().to_dict()# for each DB, 28 projects splitted to 66 parts. {2: 21, 3: 4, 4: 3}
df_work['parts'] = df_work['project_id'].map(dc_project2parts)
df_work['pin_size_part'] = df_work['pin_size'] / df_work['parts']
df_work = df_work.sort_values(by='pin_size_part', ascending=False)

ls_parts = []
for prefix, parts in zip(df_work['percolator_prefix'], df_work['parts']):
    for i in range(parts):
        ls_parts.append(os.path.join(prefix, f'part_{i}'))

cmd = '(cat {prefix}.pin | percolator  - -Y --testFDR 0.01 --trainFDR 0.01 --maxiter 10 --num-threads 24  --results-peptides {prefix}.target.peptides.txt --decoy-results-peptides /dev/null --protein-enzyme "trypsin" -P D_ --results-psms {prefix}.target.psms.txt  --decoy-results-psms /dev/null &>{prefix}.log) && pigz -f {prefix}.target.*.txt'
ls_cmds = [cmd.format(prefix=e) for e in ls_parts]

open('/gpfs/gpfs/staging/jx76-003/xc/MS/20210118Comet/20210224percolatorCombineRun_large.cmd', 'w').write('\n'.join(ls_cmds) + '\n')


def iterCometPin(filename):
    '''iter each line of comet .pin.gz file
    if "D_" in all Proteins, change Label to -1
    '''
    f = gzip.open(filename, 'rt')
    f.readline()
    for line in f:
        es = line.split('\t')
        # if len(es) != 28:
        #     print(filename)
        #     print(line)
        Proteins = es[27:]
        if all([e.startswith('D_') for e in Proteins]):
            es[1] = '-1'
        line_new = '\t'.join(es)
        yield line_new

def iterPinSpectrum(filename):
    '''Comet pin SpecId looks like 4A_1664_2_1. 4A is filename, 1664 is the spectrum_id. iter each spectrum_id
    '''
    comet_lines = iterCometPin(filename)
    for line in comet_lines:
        spectrum_id = line.split('_', maxsplit=2)[1]
        spectrum = [line]
        break
    for line in comet_lines:
        spectrum_id2 = line.split('_', maxsplit=2)[1]
        if spectrum_id2 == spectrum_id:
            spectrum.append(line)
        else:
            yield  ''.join(spectrum)
            spectrum_id = spectrum_id2
            spectrum = [line]
    yield ''.join(spectrum)

def splitPins(folder, outprefix, parts):
    '''combine and evenly split the pin files in folder. save results with name outprefix/part_{N}.pin.gz
    folder is the location of all .pin.gz files
    outprefix will be used as a output folder to store the combined and splitted pin files
    parts is the number of parts to split of the combined .pin.gz file
    '''
    try:
        os.makedirs(outprefix)
    except:
        print(outprefix,'exists. Remove all files in this folder')
        os.system(f'rm {outprefix}/*')

    files_pin = glob.glob(os.path.join(folder, '*.pin.gz'))
    if len(files_pin) == 0:
        print(folder,'empty')
        return None
    header = gzip.open(files_pin[0],'rt').readline()

    dc_outs = {n:open(os.path.join(outprefix, f'part_{n}.pin'),'w') for n in range(parts)}
    for v in dc_outs.values():
        v.write(header)
    spectrum_n = 0
    for file_pin in files_pin:
        for spectrum in iterPinSpectrum(file_pin):
            spectrum_n += 1
            dc_outs[spectrum_n % parts].write(spectrum)
    for v in dc_outs.values():
        v.close()
    # for n in range(parts):
    #     os.system('pigz ' + os.path.join(outprefix, f'part_{n}.pin'))



ls_params = [(folder, outprefix, parts) for folder, outprefix, parts in zip(df_work['folder_pin'], df_work['percolator_prefix'], df_work['parts'])]

pool = Pool()
pool.starmap(splitPins, ls_params, chunksize=1)
pool.close()
pool.join()
