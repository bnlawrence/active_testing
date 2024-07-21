# Simple code to get hemispheric mean of the lowest level of air temperature from 
# float UM_m01s30i204_vn1106(time, air_pressure_3, latitude_1, longitude_1) ;
#		UM_m01s30i204_vn1106:long_name = "TEMPERATURE ON P LEV/UV GRID" ;" ;
#		UM_m01s30i204_vn1106:units = "K" ;
#		UM_m01s30i204_vn1106:cell_methods = "time: point" ;
# with
# 	time = 40 ;
#	latitude_1 = 1921 ;
#	latitude = 1920 ;
#	longitude_1 = 2560 ;
#	air_pressure_3 = 11 ;

#  This variable is held in an 18 GB file on posix storage

from h5netcdf.legacyapi import Dataset
import numpy as np
from pathlib import Path
import sys
import time
import s3fs

my_path = Path(__file__)
results_dir = my_path.parent.parent/'results'/'h5netcdf'


S3_URL_IN = 'http://uor-aces-o.s3.jc.rl.ac.uk/'
S3_URL_OUT = 'https://uor-aces-o.s3-ext.jc.rl.ac.uk/'
S3_BUCKET = 'bnl'

filename = 'ch330a.pc19790301-def.nc'
var = "UM_m01s30i204_vn1106"

def simple_h5netdf(s3='IN',default=True, blocks_MB=1, loc='sci4', rep='a'):

    if s3 == 'IN':
        s3url = S3_URL_IN
    elif s3 == 'OUT':
        s3url = S3_URL_OUT

    if default:
        kwargs =  { 'endpoint_url': s3url}
        logfile = results_dir/f"{loc}_2407_h5netcdf-{s3}-def-{rep}.log" 
    else:
        kwargs = {  'endpoint_url': s3url, 
            'default_fill_cache':False,
            'default_cache_type':"readahead",
            'default_block_size': blocks_MB * 2**20 }
        logfile = results_dir/f"{loc}_2407_h5netcdf-{s3}-{blocks_MB}MB-{rep}.log" 

    with open(logfile,'w') as sys.stdout:

        fs = s3fs.S3FileSystem(anon=True, **kwargs)
        uri = S3_BUCKET + '/' + filename
        e1 = time.time()

        with fs.open(uri,'rb') as s3file:

            dset = Dataset(s3file)

            ds = dset[var]

            # get hemispheric mean timeseries:
            # (this would be more elegant in cf-python)
            ts,tt = [],[]
            for i in range(40):
                e3 = time.time()
                ts.append(np.mean(ds[i,0,0:960,:]))
                tt.append(time.time()-e3)
            result = np.array(ts)
            print(result)
            print(tt)
        e2 = time.time()-e1
        print(f'{e2:.2f}s wall clock time')


if __name__ == "__main__":

    for s3loc in ['IN','OUT']:
        for reps in ['a','b','c']:
            simple_h5netdf(s3=s3loc,default=True, loc='sci4', rep=reps)
            for blocks in [1,5]:
                simple_h5netdf(s3='IN',default=False, blocks_MB=blocks, loc='sci4', rep=reps)



