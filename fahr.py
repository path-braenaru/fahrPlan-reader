#!/usr/bin/env python2


import json
import argparse

from time import localtime, strftime, strptime


class co:
        GR = '\033[92m'
        RE = '\033[91m'
        BO = '\033[1m'
        E = '\033[0m'


class factory():

    def load(self):
        with open('schedule.json', 'r') as jsonfile:
            for entry in jsonfile.readlines():
                data = json.loads(entry)
            jsonfile.close()
        return data

    def extract(self, data):
        rooms = [
            'Saal 1',
            'Saal 2',
            'Saal 6',
            'Saal G'
        ]
        procData = []
        for x in data['schedule']['conference']['days']:
            for room in rooms:
                for i in x['rooms'][room]:
                    tup = (i['title'], i['room'], i['date'], i['start'], i['duration'])
                    if tup not in procData:
                        procData.append(tup)
        return procData


    def times(self):
        dt = strftime('%Y-%m-%d %H:%M', localtime())
        d = strftime('%Y-%m-%d', localtime())
        t = strftime('%H:%M', localtime())
        return dt, d, t


def __init__():
    p = argparse.ArgumentParser()
    p.add_argument(
        '-t', '--title'
    )
    p.add_argument(
        '-n', '--next', action='store_true'
    )
    args = p.parse_args()
    title = args.title
    next = args.next
    f = factory()
    data = f.load()
    dt, d, t = f.times()
    results = []
    procData = f.extract(data)
    for x in procData:
        (talk, room, date, start, duration) = x
        talk_dt = date[0:10] + ' ' + start
        talk_dt = strptime(talk_dt, '%Y-%m-%d %H:%M')
        talk_d = strptime(date[0:10], '%Y-%m-%d')
        talk_t = strptime(start, '%H:%M')
        if title:
            if title in talk.lower():
                if talk_dt > dt:
                    a = co.GR
                #elif date == d:
                #    if start > t:
                #        a = co.GR
                #    else:
                #        a = co.RE
                else:
                    a = co.RE
                match = '%s%s\n - Room: %s\n - Date: %s\n - Start: %s\n - Duration: %s%s\n' % (
                        a, talk, room, date[0:10], start, duration, co.E)
                if match not in results:
                    results.append(match)
        elif next:
            if talk_d == d:
                if talk_t > t:
                    match = '%s%s\n%s - %s%s\n' % (co.BO, talk, start, room, co.E)
                    results.append(match)
        else:
            print('Use -t $string to search for a talk')
            print('Use -n|--next to see remaining talks for today')
            exit(0)
    for entry in results:
        print(entry)
    print '%sCurrent Time: %s%s%s' % (co.BO, co.GR, t, co.E)

if __name__ == '__main__':
    __init__()
