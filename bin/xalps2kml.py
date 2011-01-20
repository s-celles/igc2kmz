#!/usr/bin/python

from optparse import OptionParser
import os
import re
import string
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from igc2kmz.color import default_gradient, hsl_to_rgba
from igc2kmz.igc import IGC
import igc2kmz.kml as kml
import igc2kmz.kmz as kmz
from igc2kmz.util import runs

def main(argv):
    parser = OptionParser()
    parser.add_option('-b', '--by', metavar='KEY')
    parser.set_defaults(by='date')
    options, args = parser.parse_args(argv[1:])
    tracks = {}
    for filename in args:
        md = re.match(r'\A(\w+\d*)_(\d+).igc\Z', os.path.basename(filename))
        if not md:
            continue
        team, date = md.group(1), md.group(2)
        if not team in tracks:
            tracks[team] = {}
        tracks[team][date] = IGC(open(filename)).track()
    dates = sorted(set(date for dates in tracks.values() for date in dates))
    teams = sorted(tracks.keys())
    date_character = dict(zip(dates, string.digits[1:] + string.uppercase))
    team_character = dict(zip(teams, string.uppercase + string.digits[1:]))
    track_folders = {}
    for i, team in enumerate(sorted(tracks.keys())):
        hue = float(i) / len(tracks)
        colors = [''.join('%02x' % (255 * x) for x in reversed(hsl_to_rgba((h, 1.0, 0.5)))) for h in (hue, (hue + 1.0 / 9) % 1.0)]
        track_folders[team] = {}
        for date in sorted(tracks[team].keys()):
            if options.by == 'date':
                name = team.upper()
            elif options.by == 'team':
                name = date
            else:
                raise RuntimeError
            track_folders[team][date] = kml.Folder(kml.Style(kml.ListStyle(listItemType='checkHideChildren')), name=name)
            track = tracks[team][date]
            if options.by == 'date':
                character = team_character[team]
            elif options.by == 'team':
                character = date_character[date]
            else:
                raise RuntimeError
            icon_style = kml.IconStyle(kml.Icon.character(character))
            style = kml.Style(icon_style)
            point = kml.Point(style, coordinates=[track.coords[-1]])
            placemark = kml.Placemark(point, style, description=' '.join((team.upper(), date)))
            track_folders[team][date].add(placemark)
            multi_geometries = [kml.MultiGeometry() for c in colors]
            for sl in runs(c.dt.hour for c in track.coords):
                coords = track.coords[sl.start:sl.stop + 1]
                multi_geometries[coords[0].dt.hour % len(colors)].add(kml.LineString(coordinates=coords))
            for color, multi_geometry in zip(colors, multi_geometries):
                style = kml.Style(kml.LineStyle(color=color))
                placemark = kml.Placemark(multi_geometry, style, name=date)
                track_folders[team][date].add(placemark)
    folder = kml.Folder(name='Tracklogs', open=1)
    if options.by == 'date':
        date_folders = dict((date, kml.Folder(name=date)) for date in dates)
        for team in sorted(track_folders.keys()):
            for date in sorted(track_folders[team].keys()):
                date_folders[date].add(track_folders[team][date])
        for date in sorted(dates):
            folder.add(date_folders[date])
    elif options.by == 'team':
        for team in sorted(track_folders.keys()):
            team_folder = kml.Folder(name=team.upper())
            for date in sorted(track_folders[team].keys()):
                team_folder.add(track_folders[team][date])
            folder.add(team_folder)
    else:
        raise RuntimeError
    kmz.kmz(folder).write('rbx.kmz', '2.0')

if __name__ == '__main__':
    main(sys.argv)
