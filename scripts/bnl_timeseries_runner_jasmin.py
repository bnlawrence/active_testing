from bnl_timeseries_jasmin import timeseries
import sys
from pathlib import Path

my_path = Path(__file__)
results_dir = my_path.parent.parent/'results'

location = 'sci6-in1'

results_dir = my_path.parent.parent/'results'/location
results_dir.mkdir()

blocks = [1,5]
version = [1,]
threads = [1,100]
iterations = ['a','b','c']

for b in blocks:
    for v in version:
        for t in threads:
            for i in iterations:
                logfile = results_dir/f'timeseries4-{location}-{b}-{v}-{t}-{i}.log'
                with open(logfile,'w') as sys.stdout:
                    timeseries(location, b, v, t)
