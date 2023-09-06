import xarray as xr
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import metpy.calc as mpcalc

from datetime import datetime, timedelta
from netCDF4 import num2date
from metpy.plots import USCOUNTIES

now = datetime.utcnow()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

if hour >= 3 and hour < 9:
    hr = '00'
    hr1 = 0
if hour >= 9 and hour < 15:
    hr = '06'
    hr1 = 6
if hour >= 15 and hour < 21:
    hr = '12'
    hr1 = 12
if hour >= 21 or hour < 3:
    hr = '18'
    hr1 = 18

fhr = 21
date = datetime(year, month, day)
date1 = datetime(year, month, day, hour, minute)
runtime = datetime(year, month, day, hr1)
forecast_time_1 = datetime(year, month, day, fhr)
forecast_time_2 = forecast_time_1 + timedelta(hours=24)
forecast_time_3 = forecast_time_1 + timedelta(hours=48)

### 00z and 06z runs can add an additional 12z time stamp compared to 12z and 18z runs ####
if hour >= 15 and hour < 21:
    forecast_time_4 = forecast_time_1 + timedelta(hours=72)
if hour >= 21 or hour < 3:
    forecast_time_4 = forecast_time_1 + timedelta(hours=72)

url = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+date.strftime('%Y%m%d')+'/nam_'+hr+'z'
ds = xr.open_dataset(url, engine='netcdf4')

data = ds['minrh2m']

lat = data['lat']
lon = data['lon']
time = data['time']

lat_vals = lat[:].squeeze()
lon_vals = lon[:].squeeze()
time_vals = time[:].squeeze()

# Creates bounds for plot
crs = ccrs.LambertConformal(central_latitude=35, central_longitude=-117)
bounds = [(-122, -114, 31, 39)]


# Creates figure
if hour >= 3 and hour < 9:
    fig = plt.figure(figsize=(15, 6))
if hour >= 9 and hour < 15:
    fig = plt.figure(figsize=(15, 6))
if hour >= 15 and hour < 21:
    fig = plt.figure(figsize=(12, 10))
if hour >= 21 or hour < 3:
    fig = plt.figure(figsize=(12, 10))
    
plt.suptitle('NAM 3-Day Min RH Change', fontsize=24, fontweight='bold')
plt.axis('off')

#### 00z #####
if hour >= 3 and hour < 9:
    fig.text(0.41, 0.87, 'Run: ' + runtime.strftime('%m/%d/%Y %HZ'), fontsize=16, fontweight='bold')
    fig.text(0.13, 0.10, 'Developed by: Eric Drewitz | Data Source: NOAA/NCEP/NOMADS\nImage Created: ' + date1.strftime('%m/%d/%Y %H:%MZ'), fontsize=12, fontweight='bold')    

#### 06z #####
if hour >= 9 and hour < 15:
    fig.text(0.41, 0.87, 'Run: ' + runtime.strftime('%m/%d/%Y %HZ'), fontsize=16, fontweight='bold')
    fig.text(0.13, 0.10, 'Developed by: Eric Drewitz | Data Source: NOAA/NCEP/NOMADS\nImage Created: ' + date1.strftime('%m/%d/%Y %H:%MZ'), fontsize=12, fontweight='bold')    

#### 12z #####
if hour >= 15 and hour < 21:
    fig.text(0.41, 0.92, 'Run: ' + runtime.strftime('%m/%d/%Y %HZ'), fontsize=16, fontweight='bold')
    fig.text(0.18, 0.05, 'Developed by: Eric Drewitz | Data Source: NOAA/NCEP/NOMADS\nImage Created: ' + date1.strftime('%m/%d/%Y %H:%MZ'), fontsize=12, fontweight='bold')

#### 18z #####
if hour >= 21 or hour < 3:
    fig.text(0.41, 0.92, 'Run: ' + runtime.strftime('%m/%d/%Y %HZ'), fontsize=16, fontweight='bold')
    fig.text(0.18, 0.05, 'Developed by: Eric Drewitz | Data Source: NOAA/NCEP/NOMADS\nImage Created: ' + date1.strftime('%m/%d/%Y %H:%MZ'), fontsize=12, fontweight='bold')

### 00z ######
if hour >= 3 and hour < 9:
    #### Forecast Time 1 ####
    ax = fig.add_subplot(1, 3, 1, projection=crs)
    ax.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(USCOUNTIES, linewidth=0.75)
    
    #### Forecast Time 2 ####
    ax1 = fig.add_subplot(1, 3, 2, projection=crs)
    ax1.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax1.add_feature(cfeature.STATES, linewidth=0.5)
    ax1.add_feature(USCOUNTIES, linewidth=0.75)
    
    #### Forecast Time 3 ####
    ax2 = fig.add_subplot(1, 3, 3, projection=crs)
    ax2.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax2.add_feature(cfeature.STATES, linewidth=0.5)
    ax2.add_feature(USCOUNTIES, linewidth=0.75)
    

#### 06z ######
if hour >= 9 and hour < 15:
    #### Forecast Time 1 ####
    ax = fig.add_subplot(1, 3, 1, projection=crs)
    ax.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(USCOUNTIES, linewidth=0.75)
    
    #### Forecast Time 2 ####
    ax1 = fig.add_subplot(1, 3, 2, projection=crs)
    ax1.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax1.add_feature(cfeature.STATES, linewidth=0.5)
    ax1.add_feature(USCOUNTIES, linewidth=0.75)
    
    #### Forecast Time 3 ####
    ax2 = fig.add_subplot(1, 3, 3, projection=crs)
    ax2.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax2.add_feature(cfeature.STATES, linewidth=0.5)
    ax2.add_feature(USCOUNTIES, linewidth=0.75)
    


##### 12z ######
if hour >= 15 and hour < 21:
    #### Forecast Time 1 ####
    ax = fig.add_subplot(2, 2, 1, projection=crs)
    ax.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(USCOUNTIES, linewidth=0.75)
    
    #### Forecast Time 2 ####
    ax1 = fig.add_subplot(2, 2, 2, projection=crs)
    ax1.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax1.add_feature(cfeature.STATES, linewidth=0.5)
    ax1.add_feature(USCOUNTIES, linewidth=0.75)
    
    #### Forecast Time 3 ####
    ax2 = fig.add_subplot(2, 2, 3, projection=crs)
    ax2.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax2.add_feature(cfeature.STATES, linewidth=0.5)
    ax2.add_feature(USCOUNTIES, linewidth=0.75)

    #### Forecast Time 4 ####
    ax3 = fig.add_subplot(2, 2, 4, projection=crs)
    ax3.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax3.add_feature(cfeature.STATES, linewidth=0.5)
    ax3.add_feature(USCOUNTIES, linewidth=0.75)

##### 18z #####
if hour >= 21 or hour < 3:
    #### Forecast Time 1 ####
    ax = fig.add_subplot(2, 2, 1, projection=crs)
    ax.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(USCOUNTIES, linewidth=0.75)
    
    #### Forecast Time 2 ####
    ax1 = fig.add_subplot(2, 2, 2, projection=crs)
    ax1.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax1.add_feature(cfeature.STATES, linewidth=0.5)
    ax1.add_feature(USCOUNTIES, linewidth=0.75)
    
    #### Forecast Time 3 ####
    ax2 = fig.add_subplot(2, 2, 3, projection=crs)
    ax2.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax2.add_feature(cfeature.STATES, linewidth=0.5)
    ax2.add_feature(USCOUNTIES, linewidth=0.75)

    #### Forecast Time 4 ####
    ax3 = fig.add_subplot(2, 2, 4, projection=crs)
    ax3.set_extent((-121, -114, 31, 39), crs=ccrs.PlateCarree())
    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax3.add_feature(cfeature.STATES, linewidth=0.5)
    ax3.add_feature(USCOUNTIES, linewidth=0.75)

    
#### 00z Run ####
if hour >= 3 and hour < 9:
    #### Initial Forecast ####
    cs = ax.contourf(lon_vals, lat_vals, data[7, :, :], transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(0, 100, 5))
    cbar = fig.colorbar(cs, shrink=0.7)
    cbar.set_label(label="Min Relative Humidity (%)", size=8, fontweight='bold')
    ax.set_title('Min RH Forecast | Valid: ' + forecast_time_1.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=12) 

    #### Day 1 Forecast Trend ####
    cs1 = ax1.contourf(lon_vals, lat_vals, (data[15, :, :] - data[7, :, :]), transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(-50, 50, 5))
    cbar1 = fig.colorbar(cs1, shrink=0.7)
    cbar1.set_label(label="Max Relative Humidity Change (%)", size=8, fontweight='bold')
    ax1.set_title('Min RH Trend Forecast | Valid: ' + forecast_time_2.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=10)    

    #### Day 2 Forecast Trend ####
    cs2 = ax2.contourf(lon_vals, lat_vals, (data[23, :, :] - data[15, :, :]), transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(-50, 50, 5))
    cbar2 = fig.colorbar(cs2, shrink=0.7)
    cbar2.set_label(label="Max Relative Humidity Change (%)", size=8, fontweight='bold')
    ax2.set_title('Min RH Trend Forecast | Valid: ' + forecast_time_3.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=10) 

   
#### 06z Run ####
if hour >= 9 and hour < 15:
    
    #### Initial Forecast ####
    cs = ax.contourf(lon_vals, lat_vals, data[5, :, :], transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(0, 100, 5))
    cbar = fig.colorbar(cs, shrink=0.8)
    cbar.set_label(label="Min Relative Humidity (%)", size=8, fontweight='bold')
    ax.set_title('Min RH Forecast | Valid: ' + forecast_time_1.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=12) 

    #### Day 1 Forecast Trend ####
    cs1 = ax1.contourf(lon_vals, lat_vals, (data[13, :, :] - data[5, :, :]), transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(-50, 50, 5))
    cbar1 = fig.colorbar(cs1, shrink=0.8)
    cbar1.set_label(label="Min Relative Humidity Change (%)", size=8, fontweight='bold')
    ax1.set_title('Min RH Trend Forecast | Valid: ' + forecast_time_2.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=10)    

    #### Day 2 Forecast Trend ####
    cs2 = ax2.contourf(lon_vals, lat_vals, (data[21, :, :] - data[13, :, :]), transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(-50, 50, 5))
    cbar2 = fig.colorbar(cs2, shrink=0.8)
    cbar2.set_label(label="Min Relative Humidity Change (%)", size=8, fontweight='bold')
    ax2.set_title('Min RH Trend Forecast | Valid: ' + forecast_time_3.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=10) 

    
#### 12z Run ####
if hour >= 15 and hour < 21:
    #### Initial Forecast ####
    cs = ax.contourf(lon_vals, lat_vals, data[3, :, :], transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(0, 100, 5))
    cbar = fig.colorbar(cs, shrink=0.6)
    cbar.set_label(label="Min Relative Humidity (%)", size=8, fontweight='bold')
    ax.set_title('Min RH Forecast | Valid: ' + forecast_time_1.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=12) 

    #### Day 1 Forecast Trend ####
    cs1 = ax1.contourf(lon_vals, lat_vals, (data[11, :, :] - data[3, :, :]), transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(-50, 50, 5))
    cbar1 = fig.colorbar(cs1, shrink=0.6)
    cbar1.set_label(label="Min Relative Humidity Change (%)", size=8, fontweight='bold')
    ax1.set_title('Min RH Trend Forecast | Valid: ' + forecast_time_2.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=10)    

    #### Day 2 Forecast Trend ####
    cs2 = ax2.contourf(lon_vals, lat_vals, (data[19, :, :] - data[11, :, :]), transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(-50, 50, 5))
    cbar2 = fig.colorbar(cs2, shrink=0.6)
    cbar2.set_label(label="Min Relative Humidity Change (%)", size=8, fontweight='bold')
    ax2.set_title('Min RH Trend Forecast | Valid: ' + forecast_time_3.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=10)     

    #### Day 3 Forecast Trend ####
    cs3 = ax3.contourf(lon_vals, lat_vals, (data[27, :, :] - data[19, :, :]), transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(-50, 50, 5))
    cbar3 = fig.colorbar(cs3, shrink=0.7)
    cbar3.set_label(label="Max Relative Humidity Change (%)", size=8, fontweight='bold')
    ax3.set_title('Min RH Trend Forecast | Valid: ' + forecast_time_4.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=10)
    

#### 18z Run ####
if hour >= 21 or hour < 3:
    #### Initial Forecast ####
    cs = ax.contourf(lon_vals, lat_vals, data[1, :, :], transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(0, 100, 5))
    cbar = fig.colorbar(cs, shrink=0.6)
    cbar.set_label(label="Min Relative Humidity (%)", size=8, fontweight='bold')
    ax.set_title('Min RH Forecast | Valid: ' + forecast_time_1.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=12) 

    #### Day 1 Forecast Trend ####
    cs1 = ax1.contourf(lon_vals, lat_vals, (data[9, :, :] - data[1, :, :]), transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(-50, 50, 5))
    cbar1 = fig.colorbar(cs1, shrink=0.6)
    cbar1.set_label(label="Min Relative Humidity Change (%)", size=8, fontweight='bold')
    ax1.set_title('Min RH Trend Forecast | Valid: ' + forecast_time_2.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=10)    

    #### Day 2 Forecast Trend ####
    cs2 = ax2.contourf(lon_vals, lat_vals, (data[17, :, :] - data[9, :, :]), transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(-50, 50, 5))
    cbar2 = fig.colorbar(cs2, shrink=0.6)
    cbar2.set_label(label="Min Relative Humidity Change (%)", size=8, fontweight='bold')
    ax2.set_title('Min RH Trend Forecast | Valid: ' + forecast_time_3.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=10)     

    #### Day 3 Forecast Trend ####
    cs3 = ax3.contourf(lon_vals, lat_vals, (data[25, :, :] - data[17, :, :]), transform=ccrs.PlateCarree(), cmap='BrBG', levels=np.arange(-50, 50, 5))
    cbar3 = fig.colorbar(cs3, shrink=0.8)
    cbar3.set_label(label="Min Relative Humidity Change (%)", size=8, fontweight='bold')
    ax3.set_title('Min RH Trend Forecast | Valid: ' + forecast_time_4.strftime('%m/%d/%Y %HZ'), fontweight='bold', fontsize=10)   


plt.savefig("NAM_Min_RH_Trends")
