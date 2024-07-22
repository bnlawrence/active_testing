from pathlib import Path
from copy import deepcopy

current_dir = Path(__file__)
results_dir = current_dir.parent.parent/'results'

def s3testlogs(target='h5netcdf'):
    template = {'def':[],'1MB':[],'5MB':[]}
    results = {'IN':deepcopy(template),'OUT':deepcopy(template)}
    this_dir = results_dir/target
    files = this_dir.glob('*.log')
    for f in files:
        bits = str(f.name).split('_')
        location,date,therest = tuple(bits)
        bits = therest.split('-')
        ignore, loc, blck, rep = tuple(bits)
        with open(f,'r') as ff:
            data = ff.readlines()
        value = data[-1].split('s')[0]
        results[loc][blck].append(value)
    print('& 1MB & 5MB & def \\\\')
    for k in ['IN','OUT']:
        s = f'{k} '
        for l in ['1MB','5MB','def']:
            ss = ','.join([str(round(float(x))) for x in results[k][l]])
            s += f' & {ss}'
        s+= '\\\\'
        print(s)

if __name__=="__main__":
    s3testlogs()