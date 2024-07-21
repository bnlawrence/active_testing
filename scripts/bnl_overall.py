from matplotlib import pyplot as plt
from bnl_timeseries_2df import log2df, plot_threads
from pathlib import Path

my_path = Path(__file__)
results_dir = my_path.parent.parent/'plots'
inputs_dir = my_path.parent.parent/'results'

for option in ['1-1-1','1-2-1',
                '1-1-100','1-2-100',
                '5-1-100','5-2-100',
                '5-1-1','5-2-1',
                ]:

    experiments = {
        'Uni 24 OP AS1a': ('results-uni24', f'timeseries4-Uni24-{option}-a.log'),
        'Uni 24 NP AS1a': ('results-uni24np',f'timeseries4-Uni24-newproxy-{option}-a.log'),
        'Uni 24 NP AS3a': ('results-uni24np3',f'timeseries4-Uni24-np3-{option}-a.log'),
        'Uni 24 OP AS1b': ('results-uni24', f'timeseries4-Uni24-{option}-b.log'),
        'Uni 24 NP AS1b': ('results-uni24np',f'timeseries4-Uni24-newproxy-{option}-b.log'),
        'Uni 24 NP AS3b': ('results-uni24np3',f'timeseries4-Uni24-np3-{option}-b.log'),
        'Uni 24 OP AS1c': ('results-uni24', f'timeseries4-Uni24-{option}-c.log'),
        'Uni 24 NP AS1c': ('results-uni24np',f'timeseries4-Uni24-newproxy-{option}-c.log'),
        'Uni 24 NP AS3c': ('results-uni24np3',f'timeseries4-Uni24-np3-{option}-c.log')
    }

    figure, axes = plt.subplots(3,3)
    figure.set_size_inches(10, 8, forward=True)

    for ax,exp in zip(axes.flat, experiments.keys()):
        input_file = inputs_dir/experiments[exp][0]/experiments[exp][1]
        summary, df, threads = log2df(input_file)
        options = option.split('-')
        if options[1] == '1': 
            plot_threads(ax, summary,threads, xtime=5.0)
        else:
            plot_threads(ax,summary,threads)

    plt.tight_layout()
    plt.savefig(results_dir/f'experiments-{option}.pdf')
