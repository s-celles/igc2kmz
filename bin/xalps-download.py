#!/usr/bin/python

TEAMS = 'aus aut1 aut2 bel can col cze esp fra1 fra2 gbr1 gbr2 ger1 ger2 grc ita1 ita2 jpn pol rom rus slo sui1 sui2 sui3 svk tur usa1 usa2 ven'.split()
DATES = '0723 0724 0725 0726 0727 0730 0731 0801 0802 0803 0804 0805 0806 0807 0808'.split()

for index, team in enumerate(TEAMS):
    for date in DATES:
        print "http://tracking.redbullxalps.com/IGC/%d/%s_2007%s.igc" % (index + 1, team, date)
