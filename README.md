fahr.py
=======

fahr.py is an offline Fahrplan checking script written in Python 3.  Using the fahrplan 
schedule JSON, the script will either search for a talk by string or simply show remaining 
talks for the day.  Don't let network outages ruin schedule checks!

Usage: python fahr.py [-t/--talk $string] [-n] [--track $string]

+ -t $string will search all titles for $string and return talk details  
+ -n will show remaining talks for the current date  
+ --track will show all results for a given track  

talks that have already passed are returned in red, talks yet to occur will return in green

Deps
----

+ argparse  
+ json  
+ time  

The fahrplan schedule.json file is included, but please check for CCC updates to this file
