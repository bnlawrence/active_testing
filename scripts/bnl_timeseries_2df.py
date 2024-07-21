from pathlib import Path
import ast
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np


def log2df(logfile):
    """ 
    Processes a logfile produced by bnl_timeseries to a dataframe and summary point for subsequent manipulation
    """
    print(logfile)
    with open(logfile,'r') as f:
        # lines 2-81 are the thread times
        lines = f.readlines()
        index = 1
        threads = []
        pdict = []
        for timestep in range(40):
            tline = lines[index]
            rline = lines[index+1][:-1]
            index +=2 
            try:
                ttimes = [float(x) for x in tline[14:-3].split(',')]
                # unfortunately the full  dictionary doesn't parse into ast, dunno why, so we have to do strip it manually
                # mydict = ast.literal_eval(rline)
                apos = rline.find('args')
                ipos = rline.find('indexing time')
                r2line =  rline[0:apos] + rline[ipos:]
                mydict = ast.literal_eval(r2line)
            except:
                print(tline)
                print(rline)
                raise
            threads+=ttimes
            if 'load nc time' in mydict:
                del(mydict['load nc time'])
            pdict.append(mydict)
        
        summary = {k:float(x.strip()[:-1]) for k,x in zip(['NC Load','Reduction','Overall'],lines[121].split(':')[-1].split(','))}
        summary['location']=lines[121].split(':')[1].strip()
        if summary['location'].startswith('Uni24whi'): 
            summary['location'] = 'Uni24'
        elif summary['location'].startswith('Uni24-new'):
            summary['location'] = 'Uni24-np1'
        details = lines[121].split(':')[2]
        summary['method']=details.split(' ')[0]
        summary['max threads']=details.split(' ')[1].split(',')[0][2:]
        summary['blocks']=details.split(' ')[1].split(',')[1][2:-1]
        print(summary)
        df = pd.DataFrame(pdict)
        df.drop('chunk number',axis=1,inplace=True)
        print(df)
        print(threads)
        return summary, df, threads

def plot_threads(ax, summary, threads, xtime=1.0, nbins=50):
    bins = np.arange(nbins)*xtime/nbins
    ax.hist(threads, density=False, bins=bins)
    #plt.grid()
    ax.set_ylabel('Counts')
    ax.set_xlabel('Chunk process time [s]')
    ax.set_xlim(0, xtime)
    ##plt.ylim(0, 10)
    #plt.axvline(np.mean(data), color="r")
    title = f"{summary['location']}({summary['method']},B{summary['blocks']}MB):MT{summary['max threads']}"
    ax.set_title(title)
    ax.text(0.95,0.98,f"{summary['Reduction']}s\n{summary['Overall']}s",
            verticalalignment='top',
            horizontalalignment='right', 
            transform=ax.transAxes)
    

if __name__== "__main__":
    my_path = Path(__file__)
    results_dir = my_path.parent.parent/'results'
    summary, df, threads = log2df(results_dir/'results-uni24np3/timeseries4-Uni24-np3-5-1-1-c.log')
    figure, axis = plt.subplots(1, 1) 

    plot_threads(axis, summary,threads,xtime=5.0)
    plt.show()
