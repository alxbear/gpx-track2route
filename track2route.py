#!/usr/bin/env python
#--------------------------------------------------------
# Name:      track2route.py
# Purpose:   Read a GPX tracklog and write as GPX route
# 
# Author:    Al Neal
#
# Created:   2015
# Copyright: (c) Al Neal
# Licence:   MIT
#--------------------------------------------------------


from xml.sax.handler import ContentHandler
from xml.sax import parse

__VERSION__ = '0.1'
__FILE__ = 'track2route'

__metaclass__ = type

class RouteMaker(ContentHandler):
    """
    Parse a GPX track file.
    Output  a GPX route file.
    Output sent to the terminal.
    Overload the handlers in the xml.sax module
    """

    wayPoints = []
    trackPoints = []

    'Flags'
    _inWayPointName = False
    _inWayPoint = False
    _inTrack = False
    _inTrackName = False

    _trackName = ''
    _wayPoint = dict.fromkeys(['name','lat','lon'])

    def selectPoints(self, tracklist ):
        """
        Dummy method that returns the track points as an
        unaltered list of route points. Overload this in a 
        sub class to change the number of route points
        The lists contain (lat,lng) tuples.
        """
        routelist = []
        for x in tracklist:
            routelist.append((x[0],x[1]))
        return routelist

    def insertWaypoints(self,tracklist):
        'Unimplemented: insert named waypoints into final route'
        pass

    def startDocument(self):
        print '<?xml version="1.0" encoding="UTF-8" ?>' 

    def endDocument(self):
        routePoints = []
        print '''
<rte>
  <name>%s</name>
<type>Route</type>''' % self._trackName
        routePoints = self.selectPoints(self.trackPoints)
        count = 1000 # generate unique point names
        for x in routePoints:
            count += 1
            name = '%s%04d' % \
     (self._trackName[:3].upper() if len(self._trackName)>0 else 'XX',count) 
            print '''
<rtept lat="%s" lon="%s">
  <name>%s</name>
  <type>Waypoints</type>
  <sym>Dot</sym>
</rtept>''' % (x[0],x[1],name)
        print '''
    </rte>
 </gpx>''' 

    def startElement(self, name, attrs):
        if name == 'gpx':        
            print '<' + name,
            for k,v in attrs.items():            
                if k == 'creator': print ' creator="%s"' % __FILE__,
                elif k == 'version': print ' version="%s"' % __VERSION__,
                else: print ' %s="%s"' % (k,v),
            print '>'
        elif name == 'wpt': # collect waypoints. Not used in this version
            self._inWayPoint = True
            self._wayPoint['lat']=attrs.get('lat')
            self._wayPoint['lon']=attrs.get('lon')
        elif name == 'name' and self._inWayPoint: self._inWayPointName = True
        elif name == 'name' and self._inTrack: self._inTrackName = True
        elif name == 'trk': self._inTrack = True
        elif name == 'trkpt' and self._inTrack:
            self.trackPoints.append((attrs.get('lat'),attrs.get('lon')))

    def endElement(self, name):
        if name == 'wpt':
            self._inWayPoint = False
            self.wayPoints.append(self._wayPoint.copy())
            self._wayPoint.update({'name':None,'lat':None,'lon':None}) 
        elif name == 'name' and self._inWayPointName:
            self._inWayPointName = False 
        elif name == 'name' and self._inTrackName:
            self._inTrackName = False

    def characters(self, chars):
        if self._inWayPoint and self._inWayPointName:
            self._wayPoint['name'] = chars
        elif self._inTrack and self._inTrackName:
            self._trackName = chars 


def test():
    parse('testdata.gpx',RouteMaker())

if __name__ == '__main__': test()


