#!/usr/bin/env python
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

    turnpoints = [
            Turnpoint(name, Coord.deg(lat, lon, 0))
            for name, lat, lon in (
                    ('Salzburg', 47.79885, 13.04840),
                    ('Gaisberg', 47.80413, 13.11091),
                    ('Dachstein', 47.47107, 13.62078),
                    ('Aschau - Chiemsee (Kampenwand)', 47.753644, 12.352900),
                    ('Zugspitze', 47.42110, 10.98526),
                    ('Lermoos Tiroler Zugspitz Arena', 47.4015735712, 10.8792329),
                    ('Brenta', 46.175238, 010.875920),
                    ('St. Moritz-Piz Corvatsch', 46.408246, 9.816083),
                    ('Matterhorn', 45.97651, 7.65832),
                    ('Mont Blanc', 45.83249, 6.86427),
                    ('Annecy', 45.853203, 6.223084),
                    ('Peille', 43.75594, 7.41082),
                    ('Mont Gros', 43.74450, 7.43400))]
    document = kml.Document(name='Red Bull X-Alps 2015 Route', open=1, Snippet='created by Tom Payne twpayne@gmail.com')

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
        if index == 0:
            icon_style = kml.Icon(href='http://maps.google.com/mapfiles/kml/paddle/go.png')
        elif index == 12:
            icon_style = kml.Icon(href='http://maps.google.com/mapfiles/kml/paddle/stop.png')
        elif index == 13:
            icon_style = kml.Icon(href='http://maps.google.com/mapfiles/kml/paddle/ylw-stars.png')
        else:
            icon_style = kml.Icon.number(index)
        style = kml.Style(icon_style)
        placemark = kml.Placemark(point, style, name=turnpoint.name)
        folder.add(placemark)
        if index in (4, 7, 9):
            coordinates = [turnpoint.coord, turnpoint.coord.coord_at(0, 25000.0)]
            line_string = kml.LineString(coordinates=coordinates, tessellate=1)
            line_style = kml.LineStyle(color=(0.0, 1.0, 0.0, 0.25), width=3)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
            coordinates = [turnpoint.coord, turnpoint.coord.coord_at(pi, 25000.0)]
            line_string = kml.LineString(coordinates=coordinates, tessellate=1)
            line_style = kml.LineStyle(color=(1.0, 0.0, 0.0, 0.75), width=3)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
        if index == 8:
            coordinates = kml.coordinates.circle(turnpoint.coord, 5500.0)
            line_string = kml.LineString(coordinates)
            line_style = kml.LineStyle(color=(0.0, 1.0, 0.0, 0.75), width=2)
            style = kml.Style(line_style)
            placemark = kml.Placemark(line_string, style)
            folder.add(placemark)
        if index in (1, 2, 3, 5, 6, 10, 11):
            coordinates = [turnpoint.coord]
            icon_style = kml.IconStyle(kml.Icon(href='http://maps.google.com/mapfiles/kml/shapes/homegardenbusiness.png'))
            style = kml.Style(icon_style)
            point = kml.Point(coordinates=coordinates)
            placemark = kml.Placemark(point, style)
            folder.add(placemark)
        document.add(folder)

    kml.kml('2.2', document).write(sys.stdout)

if __name__ == '__main__':
    main()
