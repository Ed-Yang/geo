import sys
import getopt
import random

from haversine import *
from math import radians, modf
import gpxpy
import gpxpy.gpx

DIST = 0.04 # in 40m in km
SPEED = 2.0 #  km per hour
M = 0.00000003

gpx_file_header = '<?xml version="1.0" encoding="UTF-8"?>'
gpx_header = '<gpx>'
gpx_footer = '</gpx>'

wpt_str = "<wpt lat=\"{}\" lon=\"{}\"> <time>{} </time></wpt>"
time_str = "2010-01-01T00:{}:{}Z"

def gen_wpt(secs,  lat, lon, r=1):    
    
    s = secs % 60
    m = secs / 60

    # left down to left up
    ts = "2010-01-01T00:%02d:%02dZ" % (m, s)

    # rand the fractional part F to to:
    #  F  = (Fo - M)  + 2 * M * P, P = 0 ~ 1

    if r:
        P = 0.0; I = 0.0; F = 0.0;
        P = random.random()
        I, F = modf(lat)
        lat1 = I + (F - M) + 2 * M * P 
        I, F = modf(lon)
        lon1 = I + (F - M) + 2 * M * P 
        print '({}, {}) --> ({}, {}'.format(lat, lon, lat1, lon1)
        print 'distance between (m): ', 1000 * distance_between_points(lat, lon, lat1, lon1)
        lat = lat1
        lon = lon1

    return wpt_str.format(lat, lon, ts) 

def gen_gpx(ofilename, lat_str, lon_str):

    gpx_out = open(ofilename, 'w')
    gpx_out.write(gpx_file_header + '\n')
    gpx_out.write(gpx_header + '\n')

    lat, lon = map(float, (lat_str, lon_str))
    dlat, dlon = bounding_box(lat, lon, DIST)

    #lat_rad, lat_rad = map(radians, (lat - dlat, lat + dlat))
    #lon_rad, lon_rad = map(radians, (lon - dlon, lon + dlon))

    lat_min, lat_max = (lat - dlat, lat + dlat)
    lon_min, lon_max = (lon - dlon, lon + dlon)

    print lat_min, lat_max, dlat
    print lon_min, lon_max

    print 'Latitude (min/max): ', lat_min, lat_max
    print 'Longitude(min/max): ', lon_min, lon_max
    print 'Output file: {}'.format(ofilename)    

    sp = SPEED * 1000 / 24 * 60
    s = DIST * 1000 * 2 / SPEED
    # 0: 0, 0 
    gpx_out.write(gen_wpt(s * 0, lat_min, lon_min) +"\n")

    # 1: 0, 1 
    gpx_out.write(gen_wpt(s * 1, lat_min, lon_max) +"\n")

    # 2: 1, 1 
    gpx_out.write(gen_wpt(s * 2, lat_max, lon_max) +"\n")

    # 3: 1, 0 
    gpx_out.write(gen_wpt(s * 3, lat_max, lon_min) +"\n")

    # 4: 0, 0 
    gpx_out.write(gen_wpt(s * 4, lat_min, lon_min) +"\n")

    gpx_out.write(gpx_footer)
    gpx_out.close()
    


usage_str = 'Usage: gcircle.py -o <outputfile> lat, lon'

def main(argv):
    
    outputfile = ''
    
    try:
        opts, args = getopt.getopt(argv, "ho:", ["ofile="])
    except getopt.GetoptError:
        print usage_str
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print usage_str
            sys.exit()
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if not outputfile:
        print 'output is not specified !'
        print usage_str
        sys.exit()

    try:
        print args
        lat_str, lon_str = args
        # remove tailing comma
        if lat_str.endswith(","): lat_str = lat_str[:-1]
    except ValueError:
        print 'position is not correctly specified !'
        print usage_str
        sys.exit(2)

    gen_gpx(outputfile, lat_str, lon_str)


if __name__ == "__main__":
    main(sys.argv[1:])
