import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from igc2kmz.color import default_gradient
from igc2kmz.igc import IGC
import igc2kmz.kml as kml

def main(argv):
    tracks = {}
    for filename in argv[1:]:
        md = re.match(r'\A(\w+\d*)_(\d+).igc\Z', os.path.basename(filename))
        if not md:
            continue
        team, date = md.group(1), md.group(2)
        if not team in tracks:
            tracks[team] = {}
        tracks[team][date] = IGC(open(filename)).track()
    document = kml.Document(name='Tracklogs')
    for i, team in enumerate(sorted(tracks.keys())):
        team_folder = kml.Folder(name=team.upper())
        if len(tracks) == 1:
            color = '0000ffff'
        else:
            color = ''.join('%02x' % (255 * x) for x in reversed(default_gradient(float(i) / (len(tracks) - 1))))
        for date in sorted(tracks[team].keys()):
            track = tracks[team][date]
            line_string = kml.LineString(coordinates=track.coords, altitudeMode='absolute', extrude=1)
            style = kml.Style(kml.LineStyle(color=color, width=2))
            placemark = kml.Placemark(line_string, style, name=date)
            team_folder.add(placemark)
            sys.stderr.write(color + "\n")
            line_string = kml.LineString(coordinates=track.coords)
            style = kml.Style(kml.LineStyle(color=color))
            placemark = kml.Placemark(line_string, style, name=date)
            team_folder.add(placemark)
        document.add(team_folder)
    kml.kml('2.0', document).pretty_write(sys.stdout)

if __name__ == '__main__':
    main(sys.argv)
