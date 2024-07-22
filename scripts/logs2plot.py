from pathlib import Path
from copy import deepcopy

current_dir = Path(__file__)
results_dir = current_dir.parent.parent/'results'

def active_logs():

    result_keys = {
                    'Uni-NN-OP-R1': ('uni24','Uni24'),
                    'Uni-NN-NP-R1': ('uni24np','Uni24-newproxy'),
                    'Uni-NN-NP-R3': ('uni24np3','Uni24-np3'),
                    'Hom-NN-NP-R3': ('Hom24','Hom24-np3'),
                    }

    options = ['1-2-100','5-2-100',
            '1-2-1','5-2-1',
            '1-1-100','5-1-100',
            '1-1-1','5-1-1']

    repititions = ['a','b','c']

    results = {k:{o:[] for o in options} for k in result_keys}

    for k,v in result_keys.items():
        dir,loc = v
        this_dir = results_dir/f'results-{dir}'
        for option in options:
            for rep in repititions:
                logfile = f'timeseries4-{loc}-{option}-{rep}.log'
                with open(this_dir/logfile,'r') as f:
                    data = f.readlines()
                    last_line = data[-1]
                    #Summary:  Hom24-np1:Active (T1,BS1): 7.02s,87.18s,114.3s
                    try:
                        bits = [s.strip()[:-1] for s in last_line.split(':')[-1].split(',')]
                        results[k][option].append(str(round(float(bits[-1]))))
                    except Exception as e:
                        print(f'Ignoring {logfile} (raised {e})')

    print('& & 1MB & 5 MB & 1 MB & 5 MB \\\\')
    first = ['1-2-100','5-2-100',
            '1-2-1','5-2-1']
    second = ['1-1-100','5-1-100',
            '1-1-1','5-1-1']
    for k in results:
        print(f'{k} & active  & ' + ' & '.join([','.join(x) for x in [results[k][v] for v in first]])+'\\\\')
    for k in results:
        print(f'{k} & local & ' + ' & '.join([','.join(x) for x in [results[k][v] for v in second]])+'\\\\')


if __name__=="__main__":
    active_logs()
                

        

