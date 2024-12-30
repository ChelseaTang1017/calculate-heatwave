# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:48:38 2023

@author: Zhili Tang
"""
import numpy as np
def pick_heatwave(time_series,threshold,years):
    '''
    calculate intensity, frequency, mean_duration,sum_duration,cumulative heat
    Finial Version from Matlab
    '''
    m             = np.size(time_series)
    duration      = 0
    series        = np.empty([m])
    long_duration = np.zeros([m])
    temp          = np.zeros([m])
    
    for i in range(0,m):
        if   i==m-1 and time_series[m-1] >  threshold[i] and duration >=2:
             long_duration[i] = duration + 1
             temp[i-duration:i+1] = time_series[i-duration:i+1]
        elif i==m-1 and time_series[m-1] <= threshold[i]:
             long_duration[i] = 0
        
        if time_series[i] > threshold[i]:
            duration  = duration + 1
            series[i] = duration
            continue
        else:
            if duration >= 3:
                long_duration[i-1] = duration
                temp[i-duration:i] = time_series[i-duration:i]
            
            duration  = 0
            temp[i]   = 0
            series[i] = duration
    #calculate the frequency
    fre = np.empty([m])
    fre = long_duration.copy()
    fre[fre !=0 ] = 1
    frequency = np.sum(fre[:])/years
    #calculate the duration 
    mean_duration = sum(long_duration[:])/sum(fre[:])
    sum_duration  = sum(long_duration[:])
    #calculate the intensity
    temp_max=np.zeros([m])
    
    for i in range(0,m):
        if long_duration[i] != 0:
            day = long_duration[i]
            temp_max[i] = np.max(temp[int(i-day+1):i])
        else:
            temp_max[i] = 0
            
    intensity = sum(temp_max[:])/sum(fre[:])
    #calculate cumulative_heat
    temp_ano=np.empty([m])
    for i in range(0,m):
        if temp[i] != 0:
            temp_ano[i] = temp[i] - threshold[i]
        else:
            temp_ano[i] = np.nan;
            
    cumulative_heat = np.nansum(temp_ano[:])
    
    if frequency == 0 or frequency == np.nan:
        mean_duration = np.nan
        sum_duration  = np.nan
        cumulative_heat = np.nan
        intensity       = np.nan
    return intensity, frequency, mean_duration, sum_duration, cumulative_heat
                


#-------------Main---------------------------------
if __name__=='__main__':
    import numpy as np
    import scipy.io as scio
    import netCDF4 as nc
    from netCDF4 import Dataset
    
    file = '/path/lat.mat'
    data = scio.loadmat(file)
    lat  =data['lat']
    file = '/path/lon.mat'
    data = scio.loadmat(file)
    lon  = data['lon']
    m    = np.size(lon)
    n    = np.size(lat)
    half = np.int(n/2)
    df   = Dataset('/path/threshold.nc')
    threshold = df.variables['threshold'][:]
    threshold_summer = np.empty([90,n,m])
    threshold_summer[:,half:n,:] = threshold[153:243,half:n,:]
    threshold_summer[0:31,0:half,:] = threshold[334:365,0:half,:]
    threshold_summer[31:90,0:half,:] = threshold[0:59,0:half,:]
    
    for year in range(year1,year2):
        intensity       = np.empty([m,n])
        frequency       = np.empty([m,n])
        mean_duration   = np.empty([m,n])
        sum_duration    = np.empty([m,n])
        cumulative_heat = np.empty([m,n])
        ts_summer       = np.empty([m,n,90])
        infile = '/path/ts_jja_'+str(year)+'.mat'
        data   = scio.loadmat(infile)
        ts_summer[:,half:n,:]=data['ts_jja'][:,half:n,2:92]
        infile = '/path/ts_djf_'+str(year)+'.mat'
        data   = scio.loadmat(infile)
        ts_summer[:,0:half,:]=data['ts_djf'][:,0:half,:]
        print(str(year))
        for islon in range(0,m):
            for islat in range(0,n):
                time_series = np.empty([90])
                thre        = np.empty([90])
                time_series = ts_summer[islon,islat,:]
                thre        = threshold_summer[:,islat,islon]
                intensity[islon,islat]      ,frequency[islon,islat],\
                mean_duration[islon,islat]  ,sum_duration[islon,islat],\
                cumulative_heat[islon,islat] = pick_heatwave(time_series,thre,1)

        scio.savemat('/path/cumulative_heat_'+str(year)+'.mat',{'cumulative_heat':cumulative_heat})
        scio.savemat('/path/frequency_'+str(year)+'.mat',{'frequency':frequency})
        scio.savemat('/path/intensity_'+str(year)+'.mat',{'intensity':intensity})
        scio.savemat('/path/sum_duration_'+str(year)+'.mat',{'sum_duration':sum_duration})
        scio.savemat('/path/mean_duration_'+str(year)+'.mat',{'mean_duration':mean_duration})

    
