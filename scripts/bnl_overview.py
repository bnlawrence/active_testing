from matplotlib import pyplot as plt
from bnl_timeseries_2df import log2df, plot_threads
from pathlib import Path


my_path = Path(__file__)
results_dir = my_path.parent.parent/'plots'
inputs_dir = my_path.parent.parent/'results'

options = ['1-2-100','5-2-100',
           '1-2-1','5-2-1',
           '1-1-100','5-1-100',
           '1-1-1','5-1-1']


for location,locstr in [
                        ('Hom24','Hom24-np3'),
                        ('uni24','Uni24'),
                        ('uni24np','Uni24-newproxy'),
                        ('uni24np3',"Uni24-np3")]:
    
    experiments = {option:(f'results-{location}',f'timeseries4-{locstr}-{option}-a.log') for option in options}
    
    figure, axes = plt.subplots(3,3)
    figure.set_size_inches(10, 8, forward=True)

    for ax,exp in zip(axes.flat, experiments.keys()):
        input_file = inputs_dir/experiments[exp][0]/experiments[exp][1]
        summary, df, threads = log2df(input_file)
        opt = exp.split('-')
        if opt[1] == '1': 
            plot_threads(ax, summary,threads, xtime=5.0)
        else:
            plot_threads(ax,summary,threads)

    axes.flat[-1].remove()
    plt.tight_layout()
    plt.savefig(results_dir/f'experiments-{location}.pdf')
