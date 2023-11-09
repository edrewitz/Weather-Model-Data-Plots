# IMPORTS
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

from datetime import datetime, timedelta
from netCDF4 import num2date
from siphon.catalog import TDSCatalog

# PINGS THE UCAR THREDDS SERVER TO GET THE LATEST GFS DATA
best_gfs = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/'
                      'Global_0p25deg/catalog.xml?dataset=grib/NCEP/GFS/Global_0p25deg/Best')


# SELECTS THE MOST RECENT DATASET AND SETS UP A NETCDF SUBSET
best_ds = best_gfs.datasets[0]
ncss = best_ds.subset()


# QUERIES DATA TO GET THE 500MB GEOPOTENTIAL HEIGHT DATA ACROSS THE LOWER-48
query = ncss.query()
query.lonlat_box(north=55, south=20, east=290, west=235)
query.accept('netCDF4')
query.variables('Geopotential_height_isobaric')
query.vertical_level(50000)

# TIME SELECTION FOR DATASET
now = datetime.utcnow()
query.time_range(now, now + timedelta(days=3))

# GETS OUR DATA ARRAYS
data = ncss.get_data(query)

# SETS UP EACH DATA ARRAY
height_var = data['Geopotential_height_isobaric']
time_var = data['time']
lat_var = data['latitude']
lon_var = data['longitude']

# GETS THE VALUES FROM THE DIFFERENT DATA ARRAYS
height_vals = height_var[:].squeeze()
lat_vals = lat_var[:].squeeze()
lon_vals = lon_var[:].squeeze()
time_vals = num2date(time_var[:].squeeze(), time_var.units)

# MAKES A 2-D GRID FROM OUR LATITUDE AND LONGITUDE VALUES
lon_2d, lat_2d = np.meshgrid(lon_vals, lat_vals)

# CREATES OUR BOUNDS FOR THE PLOT
crs = ccrs.LambertConformal(central_latitude=45, central_longitude=-100)
bounds = [(-122, -75, 25, 50)]

# CREATES THE FIGURE
fig = plt.figure(figsize=(20,12))

# TITLE OF THE FIGURE
plt.suptitle('GFS 500 MB 3-Day Geopotential Height Change\nValid: '+ time_vals[0].strftime('%m/%d/%Y %HZ') + ' - ' + time_vals[24].strftime('%m/%d/%Y %HZ'), fontsize=24, fontweight='bold')

# TURNS OFF THE X-Y AXES FOR THE DISPLAY
plt.axis('off')

######## INITIALIZATION SUBPLOT #################
ax = fig.add_subplot(2, 2, 1, projection=crs)
ax.set_extent(*bounds, crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
ax.add_feature(cfeature.STATES, linewidth=0.5)

# CONTOURS THE GEOPOTENTIAL HEIGHT VALUES FOR THE INITIAL ANALYSIS FRAME
c_height = ax.contour(lon_2d, lat_2d, height_vals[0, :, :], colors='black', linewidths=1,
                      transform=ccrs.PlateCarree())
cf_height = ax.contourf(lon_2d, lat_2d, height_vals[0, :, :], cmap='coolwarm',
                      transform=ccrs.PlateCarree())

# CREATES A COLORBAR
cbar_height = fig.colorbar(cf_height, pad=0.01, shrink=0.8)

# LABELS OUR COLORBAR
cbar_height.set_label(label='Geopotential Height (Dm)', fontsize=14, fontweight='bold')
ax.clabel(c_height, fontsize=14, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)

# TITLE FOR THE INITIALIZATION SUBPLOT
ax.set_title('Initial: ' + time_vals[0].strftime('%m/%d/%Y %HZ'), fontsize=18, fontweight='bold')

# CALCULATES THE HEIGHT FALLS/RISES FOR THE VARIOUS TIMES
# THESE TIMES INCLUDE:
#      1) 24 HOURS AFTER INITIAL ANALYSIS
#      2) 48 HOURS AFTER INITIAL ANALYSIS
#      3) 72 HOURS AFTER INITIAL ANALYSIS
falls_24 = height_vals[8, :, :] - height_vals[0, :, :]
falls_48 = height_vals[16, :, :] - height_vals[8, :, :]
falls_72 = height_vals[24, :, :] - height_vals[16, :, :]

######## 24 HOURS AFTER INITIAL ANALYSIS HEIGHT FALLS/RISES SUBPLOT ################

# CREATES SUBPLOT
ax1 = fig.add_subplot(2, 2, 2, projection=crs)
ax1.set_extent(*bounds, crs=ccrs.PlateCarree())
ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
ax1.add_feature(cfeature.STATES, linewidth=0.5)

# CONTOURS THE HEIGHT FALLS/RISES VALUES
c_height_24 = ax1.contour(lon_2d, lat_2d, height_vals[8, :, :], colors='black', linewidths=1,
                      transform=ccrs.PlateCarree())

c_falls_24 = ax1.contour(lon_2d, lat_2d, falls_24, colors='black', linewidths=0.5,
                      transform=ccrs.PlateCarree(), levels=np.arange(-150, 160, 10))

cf_falls_24 = ax1.contourf(lon_2d, lat_2d, falls_24,
                      transform=ccrs.PlateCarree(), levels=np.arange(-150, 160, 10), cmap='coolwarm')

# CREATES AND LABELS A COLORBAR
cbar_falls_24 = fig.colorbar(cf_falls_24, pad=0.01, shrink=0.8)
cbar_falls_24.set_label(label='Geopotential Height Change (Dm)', fontsize=14, fontweight='bold')
ax1.clabel(c_height_24, fontsize=14, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)

# SUBPLOT TITLE
ax1.set_title('24-Hour: '+ time_vals[8].strftime('%m/%d/%Y %HZ'), fontsize=18, fontweight='bold')

######## 48 HOURS AFTER INITIAL ANALYSIS HEIGHT FALLS/RISES SUBPLOT ################

# CREATES SUBPLOT
ax2 = fig.add_subplot(2, 2, 3, projection=crs)
ax2.set_extent(*bounds, crs=ccrs.PlateCarree())
ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
ax2.add_feature(cfeature.STATES, linewidth=0.5)

# CONTOURS THE HEIGHT FALLS/RISES VALUES
c_height_48 = ax2.contour(lon_2d, lat_2d, height_vals[16, :, :], colors='black', linewidths=1,
                      transform=ccrs.PlateCarree())

c_falls_48 = ax2.contour(lon_2d, lat_2d, falls_48, colors='black', linewidths=0.5,
                      transform=ccrs.PlateCarree(), levels=np.arange(-150, 160, 10))

cf_falls_48 = ax2.contourf(lon_2d, lat_2d, falls_48,
                      transform=ccrs.PlateCarree(), levels=np.arange(-150, 160, 10), cmap='coolwarm')

# CREATES AND LABELS A COLORBAR
cbar_falls_48 = fig.colorbar(cf_falls_48, pad=0.01, shrink=0.8)
cbar_falls_48.set_label(label='Geopotential Height Change (Dm)', fontsize=14, fontweight='bold')
ax2.clabel(c_height_48, fontsize=14, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)

# SUBPLOT TITLE
ax2.set_title('48-Hour: ' + time_vals[16].strftime('%m/%d/%Y %HZ'), fontsize=18, fontweight='bold')

######## 72 HOURS AFTER INITIAL ANALYSIS HEIGHT FALLS/RISES SUBPLOT ################
# CREATES SUBPLOT
ax3 = fig.add_subplot(2, 2, 4, projection=crs)
ax3.set_extent(*bounds, crs=ccrs.PlateCarree())
ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
ax3.add_feature(cfeature.STATES, linewidth=0.5)

# CONTOURS THE HEIGHT FALLS/RISES VALUES
c_height_72 = ax3.contour(lon_2d, lat_2d, height_vals[24, :, :], colors='black', linewidths=1,
                      transform=ccrs.PlateCarree())

c_falls_72 = ax3.contour(lon_2d, lat_2d, falls_72, colors='black', linewidths=0.5,
                      transform=ccrs.PlateCarree(), levels=np.arange(-150, 160, 10))

cf_falls_72 = ax3.contourf(lon_2d, lat_2d, falls_72,
                      transform=ccrs.PlateCarree(), levels=np.arange(-150, 160, 10), cmap='coolwarm')

# CREATES AND LABELS A COLORBAR
cbar_falls_72 = fig.colorbar(cf_falls_72, pad=0.01, shrink=0.8)
cbar_falls_72.set_label(label='Geopotential Height Change (Dm)', fontsize=14, fontweight='bold')
ax3.clabel(c_height_72, fontsize=14, inline=1, inline_spacing=1, fmt='%i', rightside_up=True)

# SUBPLOT TITLE
ax3.set_title('72-Hour: '+ time_vals[24].strftime('%m/%d/%Y %HZ'), fontsize=18, fontweight='bold')

# PROGRAMMER SIGNATURE AND CITING THE DATA SOURCE AT THE BOTTOM OF THE FIGURE AND GIVES THE TIME THE IMAGE WAS CREATED
fig.text(0.30, 0.05, 'Developed by: Eric Drewitz | Data Source: thredds.ucar.edu\n           Image Created: ' + now.strftime('%m/%d%Y %H:%MZ'), fontsize=18, fontweight='bold')

# SAVES FIGURE TO THE WEATHER DATA FOLDER
plt.savefig(f"Weather Data/GFS 500 MB Height Falls And Rises")
