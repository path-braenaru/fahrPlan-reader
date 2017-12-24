#!/usr/bin/env python2


import json
import argparse

from time import localtime, strftime, strptime


class co:
	GR = '\033[92m'
	RE = '\033[91m'
	BO = '\033[1m'
	E = '\033[0m'


class process():

	def __init__(self):
		self.classifiers = {}

	def load(self):
		with open('schedule.json', 'r') as jsonfile:
			for entry in jsonfile.readlines():
				main_data = json.loads(entry)
			jsonfile.close()
		with open('extraData_classifiers.json') as jsonfile:
			for entry in jsonfile.readlines():
				data = json.loads(entry)
				for x in data:
					if x['event_id'] not in self.classifiers:
						entries = {}
						for y in x['event_classifiers']:
							entries[y] = x['event_classifiers'][y]
						self.classifiers[x['event_id']] = entries
		return main_data

	def extract(self, data):
		rooms = [
			'Saal Clarke',
			'Saal Adams',
			'Saal Borg',
			'Saal Dijkstra']
		procData = []
		for x in data['schedule']['conference']['days']:
			for room in rooms:
				for i in x['rooms'][room]:
					tup = (i['title'], i['room'], i['date'],
						i['start'], i['duration'], i['track'], i['id'])
					if tup not in procData:
						procData.append(tup)
		return procData


	def resultFormat(self, talk_dt, dt, x, classify):
		(talk, room, date, start, duration, track, id) = x
		if talk_dt > dt:
			a = co.GR
		else:
			a = co.RE
		match = '%s%s\n - Room: %s\n - Date: %s\n - ' % (
				a, talk, room, date[0:10]) +\
			'Track: %s\n - Start: %s\n - Duration: %s%s\n' % (
				track, start, duration, co.E)
		if classify:
			heat = ' - Classifiers:\n'
			if id in self.classifiers:
				for k, entry in sorted(self.classifiers[id].iteritems(),
					key=lambda (a,b):(b,a), reverse=True):
						heat += '\t- %s: %s\n' % (
							k, entry)
			match += '%s%s%s' % (a, heat, co.E)
		return match


def __init__():
	p = argparse.ArgumentParser()
	p.add_argument(
		'-t', '--title'
	)
	p.add_argument(
		'-n', '--next', action='store_true'
	)
	p.add_argument(
		'--track')
	p.add_argument(
		'--classify', action='store_true')
	args = p.parse_args()
	classify = args.classify
	title = args.title
	next = args.next
	trackSearch = args.track
	f = process()
	data = f.load()
	dt = localtime()
	d = strftime('%Y-%m-%d', localtime())
	d_struct = strptime(d, '%Y-%m-%d')
	t = strftime('%H:%M', localtime())
	t_struct = strptime(t, '%H:%M')
	results = []
	procData = f.extract(data)
	for x in procData:
		(talk, room, date, start, duration, track, id) = x
		talk_dt = date[0:10] + ' ' + start
		talk_dt = strptime(talk_dt, '%Y-%m-%d %H:%M')
		talk_d = strptime(date[0:10], '%Y-%m-%d')
		talk_t = strptime(start, '%H:%M')
		if title:
			if title.lower() in talk.lower():
				match = f.resultFormat(talk_dt, dt, x, classify)
				if match not in results:
					results.append(match)
		elif trackSearch:
			if trackSearch.lower() in track.lower():
				match = f.resultFormat(talk_dt, dt, x, classify)
				if match not in results:
					results.append(match)
		elif next:
			if talk_d == d_struct:
				if talk_t > t_struct:
					match = '%s%s\n%s - %s%s\n' % (
						co.BO, talk, start, room, co.E)
					results.append(match)
		else:
			print('Use -t $string to search for a talk')
			print('Use -n|--next to see remaining talks for today')
			exit(0)
	for entry in results:
		print(entry)
	if len(results) == 0:
		print('%sNo results found%s' % (co.RE, co.E))
	print('%sCurrent Time: %s%s%s' % (co.BO, co.GR, t, co.E))


if __name__ == '__main__':
	__init__()
