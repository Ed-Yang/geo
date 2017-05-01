import sys
import getopt

import gpxpy
import gpxpy.gpx

gpx_file_header = '<?xml version="1.0" encoding="UTF-8"?>'
gpx_header = '<gpx>'
gpx_footer = '</gpx>'


def conv_gpx(infilename, ofilename):
    # GPX file is created by gpsies.com

    print 'Input file is "', infilename
    print 'Output file is "', ofilename

    gpx_file = open(infilename, 'r')
    gpx = gpxpy.parse(gpx_file)

    gpx_out = open(ofilename, 'w')
    gpx_out.write(gpx_file_header + '\n')
    gpx_out.write(gpx_header + '\n')

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                t = point.time
                ts = '%d-%02d-%02dT%02d:%02d:%02dZ' % (
                    t.year, t.month, t.day, t.hour, t.minute, t.second)
                wpt = '\t<wpt lat=\"{}\" lon=\"{}\"> <ele>{}</ele> <time>{}</time></wpt>\n'.format(
                    point.latitude, point.longitude, point.elevation, ts)
                print wpt
                gpx_out.write(wpt)

    for waypoint in gpx.waypoints:
        print 'waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude)

    for route in gpx.routes:
        print 'Route:'

    gpx_out.write(gpx_footer)
    gpx_out.close()


def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'Usage: gpsies.py -i <inputfile> -o <outputfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: gpsies.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            print 'input file: {}'.format(inputfile)
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            print 'output file: {}'.format(outputfile)

    if not inputfile or not outputfile:
        print 'no input or output file specified.'
        print 'Usage: gpsies.py -i <inputfile> -o <outputfile>'
        sys.exit()

    conv_gpx(inputfile, outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
