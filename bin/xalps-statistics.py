#!/usr/bin/python

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from igc2kmz.coord import Coord
from igc2kmz.igc import IGC
from igc2kmz.util import pairwise, runs, runs_where

igc = IGC(sys.stdin)
coords = [Coord.deg(b.lat, b.lon, b.ele, b.dt) for b in igc.b]
n = len(coords) - 1

dss, ss, dsdts, dzs, dzdts = [], [], [], [], []
s = sigma_dz_pos = 0.0
for c0, c1 in pairwise(coords):
    ds = c0.distance_to(c1)
    dss.append(ds)
    s += ds
    ss.append(s)
    dt = (c1.dt - c0.dt).seconds + 24 * 60 * 60 * (c1.dt - c0.dt).days
    dsdts.append(ds / dt)
    dz = c1.ele - c0.ele
    dzs.append(dz)
    dzdts.append(dz / dt)
    if dz > 0.0:
        sigma_dz_pos += dz

RESTING, HIKING, FLYING = xrange(0, 3)
state = [HIKING] * n
resting = (dzdt < 0.01 for dzdt in dzdts)
for sl in runs_where(resting):
  state[sl] = [RESTING] * (sl.stop - sl.start)

if 0:
    print n
    for sl in runs(state):
        c0, c1 = coords[sl.start], coords[sl.stop]
        dt0, dt1 = c0.dt, c1.dt
        st = state[sl.start]
        print "%(dt0)s--%(dt1)s\t%(st)s" % locals()
    sys.exit()

for sl in runs(state):
    st = state[sl.start]
    c0, c1 = coords[sl.start], coords[sl.stop]
    dt0, dt1 = c0.dt, c1.dt
    dt = (c1.dt - c0.dt).seconds + 24 * 60 * 60 * (c1.dt - c0.dt).days
    #ds = ss[sl.stop] - ss[sl.start]
    ds = sum(dss[sl])
    dsdt = ds / dt
    mins = dt / 60
    print "%(dt0)s--%(dt1)s\t%(st)d\t%(dt)d\t%(ds)f\t%(dsdt)f" % locals()
    


print "sigma_ds = %f" % sum(dss)
print "sigma_dz = %f" % sum(dzs)
print "sigma_dz_pos = %f" % sigma_dz_pos
