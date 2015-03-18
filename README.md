# gpx-track2route
Convert a gpx track file to a route file

Modules
-------
route.py
  Handles user input
  Custom route point picking method
  
track2route.py
  Uses xml.sax module to handle xml document elements
  
bearings.py
  Great circle calculations
  
testdata.gpx
README

Installation
------------
Copy all files to the same directory
python 2.7 installed in /usr/bin/python
python xml.sax modules
python argparser module

Usage
-----
$ ./route.py -f filename -p maxroutepoints > outputfile

filename: gpx tracklog
maxroutepoints: The number of route points that your 
  gps device can handle in a route file

Future features
---------------
1. Insert named waypoints into the route
2. Create an iterative algorithm for point selection

Author
------
alxbear on github

Version
-------
Version: 0.1

Date
----
17-03-2015

Contact
-------
al123@operamail.com



