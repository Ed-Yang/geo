"""
render image test
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from collections import namedtuple 
from s2sphere import Cell, CellId, LatLng
import requests
import json
import os

dirname, filename = os.path.split(os.path.abspath(__file__))

earthCircumferenceMeters = 1000 * 40075.017

def get_current_pos():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return (lat, lon)

def meters_to_radians(meters):
    return (2 * np.pi) * (meters / earthCircumferenceMeters);

def radians_to_meters(radians):
    return (radians * earthCircumferenceMeters) / 360

def plot_cell_spawnpoint(plt, lat, lng):
    plt.scatter(lat, lng, c='red', )

def plot_cell_circle(plt, lat, lng):
    plt.scatter(lat, lng, s=area, c='blue', alpha=0.5)

Bound = namedtuple('Bound', 'left right bottom top')


#area = Bound(120.993251, 121.004018, 24.789196, 24.790269)
left = 120.993251
right = 121.004018
top = 24.789196
bottom = 24.790269

x = [left, left, right, right]
y = [bottom, top, top, bottom]

print "x = ", x
print "y = ", y

#plt.scatter(x, y, s=area, c='b', alpha=0.5)
plt.plot(x+[left], y + [bottom])

image = mpimg.imread(dirname +'\\marker-icon.png')

r1 = [left, right, bottom, top]
print "r1 = ", r1
plt.imshow(image, extent=(r1), zorder=10)

xs = (right-left)/100
r2 = [left, left+xs*56, bottom, bottom + xs*56]
print "r2 = {} xs = {} ".format(r2, xs)
plt.imshow(image, extent=(r2), zorder=10)


plt.xticks( np.arange(120.99, 121.106, 0.001), ["%.3f"%v for v in np.arange(120.99, 121.106, 0.001)], rotation='vertical' )
plt.xlim(120.99, 121.01)
plt.xlabel("Longitute")
#plt.yticks( np.arange(6) )

#plt.yticks(np.arange(24.785, 24.792, 0.001))
plt.ylim(24.785, 24.8)

plt.grid()
plt.subplots_adjust(bottom=0.15)

#plt.axis('off')  # clear x- and y-axes

plt.show()

