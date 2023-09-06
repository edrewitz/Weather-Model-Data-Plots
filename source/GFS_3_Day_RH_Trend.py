# Imports
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

from datetime import datetime, timedelta
from netCDF4 import num2date
from siphon.catalog import TDSCatalog
from metpy.plots import USCOUNTIES

# Pings the THREDDS server to get the latest GFS data
try:
    best_gfs = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/'
                          'Global_0p25deg/catalog.xml?dataset=grib/NCEP/GFS/Global_0p25deg/Best')

    # Selects the most recent dataset and sets up a netCDF subset
    best_ds = best_gfs.datasets[0]
    ncss = best_ds.subset()
    # Queries data for surface RH
    query = ncss.query()
    query.lonlat_box(north=39, south=31, east=246, west=235)
    query.accept('netCDF4')
    query.variables('Relative_humidity_height_above_ground')
    # Time selection for dataset
    
    now = datetime.utcnow()
    query.time_range(now, now + timedelta(days=3))
    
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    
    if hour >= 6 and hour <12:
        hr = 0
    if hour >= 12 and hour <18:
        hr = 6
    if hour >=18 and hour <24:
        hr = 12
    if hour >=0 and hour < 6:
        hr = 18
    
    date = datetime(year, month, day, hr)
    date1 = datetime(year, month, day, hour, minute)

    # Gets our dataframes
    data = ncss.get_data(query)


except: 
    best_gfs = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/GFS/'
                          'Global_0p25deg/catalog.xml?dataset=grib/NCEP/GFS/Global_0p25deg/Best')

    # Selects the most recent dataset and sets up a netCDF subset
    best_ds = best_gfs.datasets[0]
    ncss = best_ds.subset()
    # Queries data for surface RH
    query = ncss.query()
    query.lonlat_box(north=39, south=31, east=246, west=235)
    query.accept('netCDF4')
    query.variables('Relative_humidity_height_above_ground')
    # Time selection for dataset
    
    now = datetime.utcnow()
    query.time_range(now, now + timedelta(days=3))
    
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    
    if hour >= 6 and hour <12:
        hr = 0
    if hour >= 12 and hour <18:
        hr = 6
    if hour >=18 and hour <24:
        hr = 12
    if hour >=0 and hour < 6:
        hr = 18
    
    date = datetime(year, month, day, hr)
    date1 = datetime(year, month, day, hour, minute)

    # Gets our dataframes
    data = ncss.get_data(query)

# Sets up each dataframe
RH_var = data['Relative_humidity_height_above_ground']

try:
    time_var = data['time']
except:
    time_var = data['time1']

lat_var = data['latitude']
lon_var = data['longitude']

# Gets the values from the dataframes
RH_vals = RH_var[:].squeeze()
lat_vals = lat_var[:].squeeze()
lon_vals = lon_var[:].squeeze()
time_vals = num2date(time_var[:].squeeze(), time_var.units)

RH_24 = RH_vals[8, :, :] - RH_vals[0, :, :]
RH_48 = RH_vals[16, :, :] - RH_vals[8, :, :]
RH_72 = RH_vals[24, :, :] - RH_vals[16, :, :]


#print(RH_vals, time_vals)
# Makes 2-D grids from our longitude and latitude values
lon_2d, lat_2d = np.meshgrid(lon_vals, lat_vals)

# Creates bounds for plot
crs = ccrs.LambertConformal(central_latitude=35, central_longitude=-117)
bounds = [(-122, -114, 31, 39)]

# Creates figure
fig = plt.figure(figsize=(10, 10))
fig.suptitle('GFS 3-Day RH Change', fontsize=24, fontweight='bold')
fig.text(0.38, 0.92, 'Run: ' + date.strftime('%m/%d/%Y %HZ'), fontsize=16, fontweight='bold')


# 0th hour
ax = fig.add_subplot(2, 2, 1, projection=crs)
ax.set_extent(*bounds, crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
ax.add_feature(cfeature.STATES, linewidth=0.5)
ax.add_feature(USCOUNTIES, linewidth=0.75)

# Adds heights for current time

cf_RH = ax.contourf(lon_2d, lat_2d, RH_vals[0, :, :],
                      transform=ccrs.PlateCarree(), levels=np.arange(0, 100, 5), cmap='BrBG')

cbar_RH = fig.colorbar(cf_RH, pad=0.01)
ax.set_title('Initial: ' + time_vals[0].strftime('%m/%d/%Y %HZ'), fontsize=12, fontweight='bold')

# 24 hour
ax1 = fig.add_subplot(2, 2, 2, projection=crs)
ax1.set_extent(*bounds, crs=ccrs.PlateCarree())
ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
ax1.add_feature(cfeature.STATES, linewidth=0.5)
ax1.add_feature(USCOUNTIES, linewidth=0.75)

cf_RH_24 = ax1.contourf(lon_2d, lat_2d, RH_24,
                      transform=ccrs.PlateCarree(), levels=np.arange(-50, 50, 5), cmap='BrBG')

cbar_RH_24 = fig.colorbar(cf_RH_24, pad=0.01)
ax1.set_title('24-Hour: ' + time_vals[0].strftime('%m/%d %HZ') + ' - ' + time_vals[8].strftime('%m/%d %HZ'), fontsize=12, fontweight='bold')

# 48 hour
ax2 = fig.add_subplot(2, 2, 3, projection=crs)
ax2.set_extent(*bounds, crs=ccrs.PlateCarree())
ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
ax2.add_feature(cfeature.STATES, linewidth=0.5)
ax2.add_feature(USCOUNTIES, linewidth=0.75)


cf_RH_48 = ax2.contourf(lon_2d, lat_2d, RH_48,
                      transform=ccrs.PlateCarree(), levels=np.arange(-50, 50, 5), cmap='BrBG')

cbar_RH_48 = fig.colorbar(cf_RH_48, pad=0.01)
ax2.set_title('48-Hour: ' + time_vals[8].strftime('%m/%d %HZ') + ' - ' + time_vals[16].strftime('%m/%d %HZ'), fontsize=12, fontweight='bold')

# 72 hour
ax3 = fig.add_subplot(2, 2, 4, projection=crs)
ax3.set_extent(*bounds, crs=ccrs.PlateCarree())
ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
ax3.add_feature(cfeature.STATES, linewidth=0.5)
ax3.add_feature(USCOUNTIES, linewidth=0.75)


cf_RH_72 = ax3.contourf(lon_2d, lat_2d, RH_72,
                      transform=ccrs.PlateCarree(), levels=np.arange(-50, 50, 5), cmap='BrBG')

cbar_RH_72 = fig.colorbar(cf_RH_72, pad=0.01)
ax3.set_title('72-Hour: ' + time_vals[16].strftime('%m/%d %HZ') + ' - ' + time_vals[24].strftime('%m/%d %HZ'), fontsize=12, fontweight='bold')

fig.text(0.13, 0.06, 'Developed by: Eric Drewitz | Data Source: thredds.ucar.edu\nImage Created: ' + date1.strftime('%m/%d/%Y %H:%MZ'), fontsize=14, fontweight='bold')
plt.savefig("GFS 3 Day RH Day Change")
