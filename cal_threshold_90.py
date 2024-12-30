# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 2022
calculate the 15-day window threshold
@author: Zhili Tang
"""

import pandas   as pd
import numpy    as np
import scipy.io as scio
import netCDF4  as nc


#---------------------------calculate the 15-day window threshold of LR CESM---------
l = 0
ts_all = np.empty([365*(year2-year1+1),latn,lonn])
#注意这里要多取前一年并多取后一年
for year in range(year1,year2):
    infile    = '/path/filename.nc'
    print(infile)
    nc_obj    = nc.Dataset(infile)
    ts        = (nc_obj.variables['TS'][:])
    ts_all[l*365:(l+1)*365,:,:] = ts
    l=l+1

threshold = np.empty([365,latn,lonn])
for day in range(1,366):
    thre = np.empty([15*41,latn,lonn])
    for year in range(1,42):
        start_day = year*365 + day - 7
        end_day   = year*365 + day + 7
        thre[(year-1)*15:year*15,:,:]   = ts_all[start_day-1:end_day,:,:]
    bb = np.sort(thre,axis=0)
    threshold[day-1,:,:,] = bb[554,:,:]
    
m = np.size(threshold,0)
n = np.size(threshold,1)
z = np.size(threshold,2)
data_NC = nc.Dataset('/path/threshold.nc', 'w', format='NETCDF4')
#创建维度变量
data_NC.createDimension('time',size = m)
data_NC.createDimension('lat', size = n)
data_NC.createDimension('lon', size = z)
# 创建维度变量，createVariable（变量名，值类型，维度）注意这里的维度就是上面
#创建维度的名称，不然会#报错
data_NC.createVariable('threshold',np.float64,('time','lat','lon'))
data_NC.variables['threshold'][:,:,:] = (threshold)
data_NC.close()

