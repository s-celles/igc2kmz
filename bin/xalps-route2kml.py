#!/usr/bin/env python2.5
# -*- encoding: utf-8 -*-

from math import pi
import os.path
import sys
from pprint import pprint

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from igc2kmz.coord import Coord
import igc2kmz.kml as kml

class Turnpoint(object):

    def __init__(self, name, coord):
        self.name = name
        self.coord = coord

def main():

    turnpoints = []

    turnpoints.append(Turnpoint('Salzburg', Coord.deg(47.798872, 13.047809, 0)))
    turnpoints.append(Turnpoint('Gaisberg', Coord.deg(47.8032, 13.10937, 0)))
    turnpoints.append(Turnpoint('Dachstein', Coord.deg(47.0+28.0/60.0+32.0/3600.0, 13.0+36.0/60.0+23.0/3600.0, 0)))
    turnpoints.append(Turnpoint('Tre Cima', Coord.deg(46.0+37.0/60.0+7.0/3600.0, 12.0+18.0/60.0+20.0/3600.0, 0)))
    turnpoints.append(Turnpoint('Piz Palu', Coord.deg(46.0+22.0/60.0+42.0/3600.0, 9.0+57.0/60.0+38.0/3600.0, 0)))
    turnpoints.append(Turnpoint('Matterhorn', Coord.deg(45.0+58.572/60.0, 7.0+39.428/60.0, 0)))
    turnpoints.append(Turnpoint('Mont Blanc', Coord.deg(45.0+49.950/60.0, 6.0+51.867/60.0, 0)))
    turnpoints.append(Turnpoint('Monviso', Coord.deg(44.0+40.0/60.0+3.0/3600.0, 7.0+5.0/60.0+30.0/3600.0, 0)))
    turnpoints.append(Turnpoint('Mont Gros', Coord.deg(43.0+46.026/60.0, 7.0+26.341/60.0, 0)))

    document = kml.Document(name='Red Bull X-Alps 2011 Route', open=1, Snippet='created by Tom Payne twpayne@gmail.com')

    # Route
    line_string = kml.LineString(coordinates=[tp.coord for tp in turnpoints], tessellate=1)
    line_style = kml.LineStyle(color=(1.0, 1.0, 0.0, 0.75), width=4)
    style = kml.Style(line_style)
    placemark = kml.Placemark(line_string, style, name='Route')
    document.add(placemark)

    # Turnpoints
    for index, turnpoint in enumerate(turnpoints):
        list_style = kml.ListStyle(listItemType='checkHideChildren')
        style = kml.Style(list_style)
        folder = kml.Folder(style, name=turnpoint.name)
        point = kml.Point(coordinates=[turnpoint.coord])
        icon_style = kml.Icon.number(index) if index else kml.Icon.palette(4, 25)
        style = kml.Style(icon_style)
        placemark = kml.Placemark(point, style, name=turnpoint.name)
        folder.add(placemark)
        if True:
            pass
        elif index == 2:
            coordinates = kml.coordinates.circle(turnpoint.coord, 1000.0)
            line_string = kml.LineString(coordinates)
            line_style = kml.LineStyle(color=(0.0, 1.0, 0.0, 0.75), width=2)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
        elif index == 3:
            coordinates = kml.coordinates.circle(turnpoint.coord, 5000.0)
            line_string = kml.LineString(coordinates)
            line_style = kml.LineStyle(color=(0.0, 1.0, 0.0, 0.75), width=2)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
        elif index == 5:
            coordinates = kml.coordinates.arc(turnpoint.coord, 4500.0, 0.0, pi/2.0)
            line_string = kml.LineString(coordinates)
            line_style = kml.LineStyle(color=(0.0, 1.0, 0.0, 0.75), width=2)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
            coordinates = [turnpoint.coord.coord_at(0.0, 4500.0), turnpoint.coord, turnpoint.coord.coord_at(pi/2.0, 4500.0)]
            line_string = kml.LineString(coordinates=coordinates, tessellate=1)
            line_style = kml.LineStyle(color=(1.0, 0.0, 0.0, 0.75), width=2)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
        elif index == 7:
            coordinates = kml.coordinates.circle(turnpoints[7].coord, 100.0)
            line_string = kml.LineString(coordinates)
            line_style = kml.LineStyle(color=(0.0, 1.0, 0.0, 0.75), width=2)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
        document.add(folder)

    kml.kml('2.2', document).write(sys.stdout)

if __name__ == '__main__':
    main()
