#
# pip install Pillow-3.4.2-cp27-cp27m-win32.whl
# pip install scipy-0.18.1-cp27-cp27m-win32.whl
#

import matplotlib.pyplot as plt
import numpy as np
from s2sphere import *
from shapely.geometry import Polygon
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import math
import matplotlib.image as mpimg

import requests
import json

import os
dirname, filename = os.path.split(os.path.abspath(__file__))

from pylab import rcParams
rcParams['figure.figsize'] = 10, 10

def get_current_pos():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return (lat, lon)
    
# choose OSM
proj = cimgt.OSM()
#proj = cimgt.MapQuestOSM()

# figsize: w,h tuple in inches
# if figsize is not set, the default is 8, 6 in win32 (call the figure 
# is not working for win32) 
#plt.figure(figsize=(10,10), dpi=200)

# CRS (coordinate reference system)
ax = plt.axes(projection=proj.crs)
ax.add_image(proj, 12)

#--------------------------------------------------------------------------
# XXX
#--------------------------------------------------------------------------

#p1 = LatLng.from_degrees(-51.264871, -30.241701)
#p2 = LatLng.from_degrees(-51.04618, -30.000003)
 
# extent is data axes (left, right, bottom, top) for making image plots

#ax.set_extent([-51.411886, -50.922470, -30.301314, -29.94364])

#--------------------------------------------------------------------------
# Taiwan HC
#--------------------------------------------------------------------------

p1 = LatLng.from_degrees(24.789196, 120.993251)
p2 = LatLng.from_degrees(24.790269, 121.004018)

#ax.set_extent([120.9, 121.02, 24.76, 24.83])

LAT_DIFF = 0.02
LNG_DIFF = 0.02

left = min(p1.lng().degrees, p2.lng().degrees)
right = max(p1.lng().degrees, p2.lng().degrees)
bottom = min(p1.lat().degrees, p2.lat().degrees)
top = max(p1.lat().degrees, p2.lat().degrees)

#bound = (x1, x2, y1, y2)
#ax.set_extent(bound)
ax.set_extent([left - LNG_DIFF, right + LNG_DIFF, bottom - LAT_DIFF, top + LAT_DIFF])

region_rect = LatLngRect.from_point_pair(p1, p2)

coverer = RegionCoverer()
coverer.min_level = 8
coverer.max_level = 15
coverer.max_cells = 500
covering = coverer.get_covering(region_rect)

geoms = []

#v1 = [(bottom, left), (bottom, right), (top, left), (top, right)]
#v1 = [(bottom, left), (top, left), (top, right), (bottom, right)]
v1 = [(left, bottom), (left, top), (right, top), (right, bottom)]

for v in v1:
    print "===> lat:{} lng:{}".format(v[0], v[1])

geo = Polygon(v1)
geoms.append(geo)

c_cnt = 0
for c in covering:
    new_cell = Cell(c)
    print('LVL {}:{}: AREA: {}'.format(new_cell.level(), new_cell.is_leaf(), new_cell.exact_area()))
    vertices = []
    for i in xrange(0, 4):
        vertex = new_cell.get_vertex(i)
        latlng = LatLng.from_point(vertex)
        vertices.append((latlng.lng().degrees, latlng.lat().degrees))
        

    # debug
    print "{:2d} {} LVL:{}".format(c_cnt+1, c, c.level())
    for v in vertices:
        print "lat:{} lng:{}".format(v[0], v[1])

    geo = Polygon(vertices)
    geoms.append(geo)
    c_cnt = c_cnt+1

print "Total Geometries: {}".format(len(geoms))


curPos = get_current_pos()
print curPos

curPos = (p1.lat().degrees, p1.lng().degrees)

ax.add_geometries(geoms, ccrs.PlateCarree(), facecolor='blue', edgecolor='red', alpha=0.4)
IMG_OFFSET = 0.0001
image = mpimg.imread(dirname +'\\marker-icon.png')
#plt.imshow(image)
#plt.imshow(image, aspect='auto', extent=(0.4, 0.6, .5, .7), zorder=-1)
#plt.imshow(image, extent=(curPos[1],curPos[1]+IMG_OFFSET,curPos[0], curPos[0]+IMG_OFFSET), zorder=10)
#plt.imshow('maker-icon.png', extent=(curPos[1],curPos[1]+IMG_OFFSET,curPos[0], curPos[0]+IMG_OFFSET), zorder=10)


#
#
#

colors = np.random.rand(4)
area = np.pi * (15 * np.random.rand(4))**2  # 0 to 15 point radiuses

x = [left, left, right, right]
y = [bottom, top, bottom, top]

print "x = ", x
print "y = ", y

ax.scatter(x, y, s=area, c=colors, alpha=0.5, zorder=20)

plt.show()


