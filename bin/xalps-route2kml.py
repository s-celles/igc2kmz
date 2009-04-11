#!/usr/bin/env python2.5
# -*- encoding: utf-8 -*-

from math import pi
import os.path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from igc2kmz.coord import Coord
import igc2kmz.kml as kml

class Turnpoint(object):

    def __init__(self, name, coord):
        self.name = name
        self.coord = coord

def main():

    turnpoints = []

    turnpoints.append(Turnpoint('Salzburg (AT)', Coord.deg(47.0+33.310/60.0, 12.0+55.287/60.0, 0)))

    # TP1: Athletes must walk through a Red Bull arch positioned on the summit of
    # the Gaisberg mountain near Salzburg, Coordinates to be defined.
    turnpoints.append(Turnpoint('Gaisberg (AT)', Coord.deg(47.0+33.310/60.0, 12.0+55.287/60.0, 0)))

    # TP2: Through a cylinder centred around the Watzmann Middle Peak, Germany.
    # Coordinates: N47°33.310' E012°55.287’. Cylinder: 1000m radius. The athletes
    # must fly or walk through this cylinder.
    turnpoints.append(Turnpoint('Watzmann Middle Peak (DE)', Coord.deg(47.0+33.310/60.0, 12.0+55.287/60.0, 0)))

    # TP3: Through a cylinder centred around the Grossglockner, Austria.
    # Coordinates: N47°04.500' E012°41.667’. Cylinder: 5km radius. The athletes must
    # fly or walk through this cylinder.
    turnpoints.append(Turnpoint('Grossglocker (AT)', Coord.deg(47.0+4.5/60.0, 12.0+41.667/60.0, 0)))

    # TP4: The summit of Marmolada, Italy - Coordinates: N46°26.067' E011°51.033’.
    # The athletes must fly or walk South of this point.
    turnpoints.append(Turnpoint('Marmolda (IT)', Coord.deg(46.0+26.067/60.0, 11.0+51.033/60.0, 0)))

    # TP5: Through a quarter-cylinder sector, the radius of which is centred on the
    # Matterhorn Peak, Switzerland, with coordinates:  N45° 58.572'   E7° 39.428'.
    # The quarter-cylinder has an 4.5km radius, and is bound by its North and East
    # sides (see diagram). The athletes must fly or walk through this sector. It is
    # prohibited to enter or exit the sector through the sides of the sector i.e.
    # the athletes must enter and exit via the curved section.
    turnpoints.append(Turnpoint('Matterhorn (CH)', Coord.deg(45.0+58.572/60.0, 7.0+39.428/60.0, 0)))

    # TP6: The summit of Mont Blanc in France – Coordinates : N45°49.950'
    # E006°51.867'. The athlete must fly or walk North of this point.
    turnpoints.append(Turnpoint('Mont Blanc (FR)', Coord.deg(45.0+49.950/60.0, 6.0+51.867/60.0, 0)))

    # TP7: The summit of Mont Gros in Monaco - Coordinates: N43°46.026'
    # E007°26.341'. The athletes must walk or run through a virtual cylinder with a
    # radius of 100m around the summit of this point. All pilots arriving at the
    # last turn point (Mont Gros) must land and take off at the paragliding take-off
    # place, defined in details by the Race Director in advance.
    turnpoints.append(Turnpoint('Mont Gros (MN)', Coord.deg(43.0+46.026/60.0, 7.0+26.341/60.0, 0)))

    children = []

    # Turnpoints
    for index, turnpoint in enumerate(turnpoints):
        list_style = kml.ListStyle(listItemType='checkHideChildren')
        folder = kml.Folder(list_style, name=turnpoint.name)
        point = kml.Point(coordinates=[turnpoint.coord])
        placemark = kml.Placemark(point, name=turnpoint.name)
        folder.add(placemark)
        if index == 2:
            coordinates = kml.coordinates.circle(turnpoint.coord, 1000.0)
            line_string = kml.LineString(coordinates)
            placemark = kml.Placemark(line_string)
            folder.add(placemark)

    # Route
    line_string = kml.LineString(coordinates=[tp.coord for tp in turnpoints], tessellate=1)
    placemark = kml.Placemark(line_string, name='Route')
    children.append(placemark)

    coordinates = kml.coordinates.circle(turnpoints[3].coord, 5000.0)
    line_string = kml.LineString(coordinates)
    placemark = kml.Placemark(line_string)
    #children.append(placemark)

    coordinates = kml.coordinates.arc(turnpoints[5].coord, 4500.0, 0.0, pi/2.0)
    line_string = kml.LineString(coordinates)
    placemark = kml.Placemark(line_string)
    #children.append(placemark)

    coordinates = [turnpoints[5].coord.coord_at(0.0, 4500.0), turnpoints[5].coord, turnpoints[5].coord.coord_at(pi/2.0, 4500.0)]
    line_string = kml.LineString(coordinates=coordinates)
    placemark = kml.Placemark(line_string)
    #children.append(placemark)

    coordinates = kml.coordinates.circle(turnpoints[7].coord, 100.0)
    line_string = kml.LineString(coordinates)
    placemark = kml.Placemark(line_string)
    #children.append(placemark)

    kml.kml(*children).write(sys.stdout)

if __name__ == '__main__':
    main()
