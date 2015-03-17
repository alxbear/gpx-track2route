#!/usr/bin/python

from math import sin, sqrt, cos, pow, atan2, radians, degrees

"""
Radius (km) * Distance (radians) = Distance of arc (km)
"""
RADIUS_OF_EARTH_KM = 6371.0
RADIUS_OF_EARTH_MI = 3959.0

def distance(lat1,lon1,lat2,lon2):
    """Input 2 points in Lat/Lon degrees.
    Calculates the great circle distance between them in radians
    """
    rlat1= radians(lat1)
    rlon1= radians(lon1)
    rlat2= radians(lat2)
    rlon2= radians(lon2)

    dlat = rlat1 - rlat2
    dlon = rlon1 - rlon2
    
    a = pow(sin(dlat/2.0),2) +  cos(rlat1)*cos(rlat2)*pow(sin(dlon/2.0),2)
    c = 2* atan2(sqrt(a), sqrt(1-a))    

    return c


def bearing(lat1,lon1,lat2,lon2):
    """Input 2 points in Lat/Lon degrees.
     Bearing at point 1 to point 2 calculated in radians
    """
    rlat1= radians(lat1)
    rlon1= radians(lon1)
    rlat2= radians(lat2)
    rlon2= radians(lon2)

    dlat = rlat1 - rlat2
    dlon = rlon1 - rlon2
    
    theta = atan2(sin(dlon)*cos(rlat2), \
             cos(rlat1)*sin(rlat2) - sin(rlat1)*cos(rlat2)*cos(dlon) )

    return theta

def test():

    print distance(51.3975616,-0.9932566,51.3971252,-0.9947758)
    print degrees(bearing(51.426,-0.933,51.439,-1.071))

if __name__ == '__main__':
    test()

