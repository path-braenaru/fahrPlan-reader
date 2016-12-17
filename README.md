fahr.py
=======

Usage: python fahr.py [-t $string] [-n]

-t $string will search all titles for $string and return talk details
-n will show remaining talks for the current date

talks that have already passed are returned in red, talks yet to occur wil lreturn in green

Deps
----

argparse
json
time

The fahrplan schedule.json file is included, but please check for CCC updates to this file
