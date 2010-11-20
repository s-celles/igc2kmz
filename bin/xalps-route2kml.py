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

    turnpoints = [Turnpoint(name, Coord.deg(lat, lon, 0))
    for name, lat, lon in (
            ('Salzburg', 47.79885, 13.04840),
            ('Gaisberg', 47.80413, 13.11091),
            ('Dachstein', 47.47107, 13.62078),
            ('Großklockner', 47.07436, 12.69471),
            ('Tre Cime', 46.61917, 12.30417),
            ('Piz Palü', 46.37833, 9.9605),
            ('Matterhorn', 45.97651, 7.65832),
            ('Mont Blanc', 45.83249, 6.86427),
            ('Mont Gros', 43.76549, 7.44273))]
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
        if index == 3:
            coordinates = kml.coordinates.circle(turnpoint.coord, 6000.0)
            line_string = kml.LineString(coordinates)
            line_style = kml.LineStyle(color=(0.0, 1.0, 0.0, 0.75), width=2)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
        elif index == 4:
            coordinates = kml.coordinates.circle(turnpoint.coord, 1000.0)
            line_string = kml.LineString(coordinates)
            line_style = kml.LineStyle(color=(0.0, 1.0, 0.0, 0.75), width=2)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
        elif index == 5:
            coordinates = kml.coordinates.circle(turnpoint.coord, 6000.0)
            line_string = kml.LineString(coordinates)
            line_style = kml.LineStyle(color=(0.0, 1.0, 0.0, 0.75), width=2)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
        elif index == 6:
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
        elif index == 8:
            coordinates = kml.coordinates.circle(turnpoint.coord, 100.0)
            line_string = kml.LineString(coordinates)
            line_style = kml.LineStyle(color=(0.0, 1.0, 0.0, 0.75), width=2)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
        document.add(folder)

    kml.kml('2.2', document).write(sys.stdout)

if __name__ == '__main__':
    main()
