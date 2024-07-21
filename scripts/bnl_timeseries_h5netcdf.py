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
logfile=results_dir/"sci4_2407_h5netcdf-int.log"

S3_URL = 'http://uor-aces-o.s3.jc.rl.ac.uk/'
S3_BUCKET = 'bnl'

filename = 'ch330a.pc19790301-def.nc'
var = "UM_m01s30i204_vn1106"

with open(logfile,'w') as sys.stdout:


    fs = s3fs.S3FileSystem(anon=True, client_kwargs={'endpoint_url': S3_URL})
    uri = S3_BUCKET + '/' + filename
    e1 = time.time()

    with fs.open(uri,'rb') as s3file:

        dset = Dataset(s3file)

        ds = dset[var]

        # get hemispheric mean timeseries:
        # (this would be more elegant in cf-python)
        ts = []
        for i in range(40):
            ts.append(np.mean(ds[i,0,0:960,:]))

        result = np.array(ts)
        print(result)
    e2 = time.time()-e1
    print(f'Wall clock time used {e2:.2f}')
