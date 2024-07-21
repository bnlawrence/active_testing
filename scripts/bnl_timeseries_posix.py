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

from netCDF4 import Dataset
import numpy as np


filename = 'ch330a.pc19790301-def.nc'
var = "UM_m01s30i204_vn1106"

with Dataset(filename,'r') as dset:

    ds = dset[var]

    # get hemispheric mean timeseries:
    # (this would be more elegant in cf-python)
    ts = []
    for i in range(40):
        ts.append(np.mean(ds[i,0,0:960,:]))
        # get some performance diagnostics from pyactive

    result = np.array(ts)
    print(result)