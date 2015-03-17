#!/usr/bin/python

from math import fabs, pi
from heapq import nlargest
from xml.sax import parse
from xml.sax.handler import ErrorHandler
import argparse
import os.path
import sys

from bearings import bearing
from track2route import RouteMaker

class WrongFileType(ErrorHandler):
    def fatalError(self, exception):
        sys.stderr.write( "File not an XML document\n")
        sys.exit(0)

class RouteReducer(RouteMaker):
    """
    Extend the `RouteMaker` class.
    Overload `selectPoints` method with one
    to reduce the number of route points to 
    a maximum of `maxPoints`.
    """    
    maxPoints = 100

    def setMaxPoints(self, maxPoints=100):
        'Set the `maxPoints` attribute.'
        self.maxPoints = maxPoints


    def selectPoints(self, tracklist):
        """
        Reduce the number of route points to that 
        that GPS device can handle.
        The method calculates the angle of the track at
        a point. The points with the largest angles are 
        selected for the route. 
        """
        # _tmp0: [{lat,lon,pos,bbear,fbear,angle}]
        _tmp0 = self._calcBearing(tracklist)
        # store the start end end points so they are not lost
        try:
            _startPoint = _tmp0.pop(0)
            _endPoint = _tmp0.pop()
        except IndexError:
            sys.exit(1)
        # select the points with the largest angle of turn
        _tmp1 = nlargest(self.maxPoints-2, _tmp0, key=lambda x: x['angle']) 
        # sort the list back into route order
        _tmp2 = sorted(_tmp1, key=lambda x: x['pos'])
        # add the start and end points back
        _tmp2.insert(0, _startPoint)
        _tmp2.append(_endPoint)
        # return just the la/lon pairs
        return [(x['lat'],x['lon']) for x in _tmp2]


    def _calcBearing(self,tracklist):
        'Get the angle between the next and previous points'
        wlist = []
        # i retains the route point order 
        for i, x in enumerate(tracklist):
            wlist.append({'lat':float(x[0]), \
                    'lon':float(x[1]),'pos':i,'angle':0.0, \
                    'fbear':0.0, 'bbear':0.0})
        # get the forward and back bearings from a point
        for x in range(len(wlist)-1):
            fb = bearing( wlist[x]['lat'], wlist[x]['lon'], \
                        wlist[x+1]['lat'], wlist[x+1]['lon'])
            bb = bearing( wlist[x+1]['lat'], wlist[x+1]['lon'], \
                        wlist[x]['lat'], wlist[x]['lon'])
            wlist[x]['fbear']   = float(fb)
            wlist[x+1]['bbear'] = float(bb)
        # calculate the angle between points
        for x in range(len(wlist)-1):
            _tmp1 = fabs(wlist[x]['fbear']-wlist[x]['bbear'])
            if _tmp1 > pi: _tmp1 = (2.0 * pi) - _tmp1 
            wlist[x]['angle'] = fabs(pi - _tmp1)
        return wlist



"""################################################################"""

def main():
    """
    Process the command line options.
    Call the sax parser.
    """
    options = argparse.ArgumentParser(description="Convert GPX track to route")
    options.add_argument('-f', '--file' , dest='filename',
                        help="source gpx file", metavar="FILE")
    options.add_argument('-p', '--points', type=int, dest='maxpoints',
                        help="number of route points in output", default=100)

    opts = options.parse_args()

    try:
        if not os.path.isfile(opts.filename): raise IOError
    except IOError:
        sys.stderr.write( "Cannot open file -f option\n")
        sys.exit(0)
    
    try:
        maxpoints = int(opts.maxpoints)
    except (TypeError, ValueError):
        sys.stderr.write( "Cannot convert -p option to a number\n" )
        sys.exit(0)
    
    # create instance
    myRoute = RouteReducer()
    # set the maxPoints parameter in the instane
    myRoute.setMaxPoints(maxpoints)
    # create an error handler 
    mh = WrongFileType()
    
    parse(opts.filename,myRoute,mh)

if __name__ == '__main__': main()



