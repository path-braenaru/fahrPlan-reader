fahr.py
=======

fahr.py is an offline Fahrplan checking script written in Python (both 2 and 3 compatible).  Using the fahrplan 
schedule JSON, the script will either search for a talk by string or simply show remaining 
talks for the day, with the option to show full descriptions.  Don't let network lag or outages ruin schedule checks!

Usage: python fahr.py [-t/--talk $string] [-n] [--track $string] [--classify]

+ -t $string will search all titles for $string and return talk details  
+ -n will show remaining talks for the current date  
+ --track will show all results for a given track  
+ add --classify to see the associated classifiers (track relevance by %) in the output for the talks
++ As of 2019/12/21: JSON with classifiers may be available again, but currently will not populate !
talks that have already passed are returned in red, talks yet to occur will return in green

Deps
----

+ argparse  
+ json  
+ time  

The fahrplan schedule.json file is included, but please check for CCC updates to this file
