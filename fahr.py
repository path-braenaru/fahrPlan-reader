#!/usr/bin/env python3


import json
import argparse


from time import localtime, strftime, strptime


class co:
	CY = '\033[96m'
	GR = '\033[92m'
	RE = '\033[91m'
	BO = '\033[1m'
	E = '\033[0m'


class process():

	def __init__(self):
		self.classifiers = {}
		self.tracks = []

	def load(self):
		with open('schedule.json', 'r') as jsonfile:
			main_data = json.load(jsonfile)

		#with open('extraData_classifiers.json') as jsonfile:
		#	for entry in jsonfile.readlines():
		#		data = json.loads(entry)
		#		for x in data:
		#			if x['event_id'] not in self.classifiers:
		#				entries = {}
		#				for y in x['event_classifiers']:
		#					entries[y] = x['event_classifiers'][y]
		#				self.classifiers[x['event_id']] = entries
		return main_data

	def extract(self, data):
		rooms = ['Ada', 'Borg', 'Clarke', 'Dijkstra', 'Eliza']
		procData = []
		for x in data['schedule']['conference']['days']:
			for room in rooms:
				for i in x['rooms'][room]:
					tup = (i['title'].encode('utf-8'), i['room'], i['date'],
						i['start'], i['duration'], i['track'],
						i['id'], i['description'].encode('utf-8'))
					if tup not in procData:
						procData.append(tup)
					if i['track'] not in self.tracks:
						self.tracks.append(i['track'])
		return procData


	def resultFormat(self, talk_dt, dt, x, classify, isDesc):
		(talk, room, date, start, duration, track, id, desc) = x
		if talk_dt > dt:
			a = co.GR
		else:
			a = co.RE
		match = '{}{}\n - Room: {}\n - Date: {}\n - '.format(a, talk.decode('utf-8'), room, date[0:10]) +\
			'Track: {}\n - Start: {}\n - Duration: {}{}\n'.format(track, start, duration, co.E)
		if isDesc:
			match += '{} - Description:\n{}\n{}'.format(a, desc.decode('utf-8'), co.E)
		if classify:
			heat = ' - Classifiers:\n'
			if id in self.classifiers:
				for k, entry in sorted(self.classifiers[id].items(),
					key=lambda a: a[1], reverse=True):
						heat += '\t- {}: {}\n'.format(k, entry)
			match += '{}{}{}'.format(a, heat, co.E)

		return match


def __init__():
	p = argparse.ArgumentParser()
	p.add_argument('-t', '--title', help='Search for a title by string')
	p.add_argument('-n', '--next', action='store_true', help='Show remaining talks for the current day')
	p.add_argument('--track', help='Search for all talks in a track (USE FIRST TRACK WORD ONLY)')
	p.add_argument('--classify', action='store_true', help='Show track relevance by classifiers')
	p.add_argument('--description', action='store_true', help='Append talk descriptions to output items')
	args = p.parse_args()
	classify = args.classify
	title = args.title
	next = args.next
	trackSearch = args.track
	isDesc = args.description
	f = process()
	data = f.load()
	dt = localtime()
	d = strftime('%Y-%m-%d', localtime())
	d_struct = strptime(d, '%Y-%m-%d')
	t = strftime('%H:%M', localtime())
	t_struct = strptime(t, '%H:%M')
	results = {'Ada': [], 'Borg': [], 'Clarke': [], 'Dijkstra': [], 'Eliza': []}
	procData = f.extract(data)
	for x in procData:
		(talk, room, date, start, duration, track, id, desc) = x
		talk_dt = date[0:10] + ' ' + start
		talk_dt = strptime(talk_dt, '%Y-%m-%d %H:%M')
		talk_d = strptime(date[0:10], '%Y-%m-%d')
		talk_t = strptime(start, '%H:%M')
		if title:
			if title.lower() in str(talk).lower():
				match = f.resultFormat(talk_dt, dt, x, classify, isDesc)
				results[room].append(match)
		elif trackSearch:
			if trackSearch.lower() in track.lower():
				match = f.resultFormat(talk_dt, dt, x, classify, isDesc)
				if match not in results:
					results[room].append(match)
		elif next:
			if talk_d == d_struct:
				if talk_t > t_struct:
					match = '{}{}\nStart: {} Length: {}{}\n\n'.format(
						co.BO, talk.decode('utf-8'), start, duration, co.E)
					results[room].append(match)
		else:
			print('Use -t $string to search for a talk')
			print('Use -n|--next to see remaining talks for today')
			exit(0)
	for entry in sorted(results):
		print(str('{}Saal {}:{}\n\n{}'.format(co.CY, entry, co.E, '\n'.join(results[entry]))))
	if len(results) == 0:
		print('{}No results found{}'.format(co.RE, co.E))
	print('{}{}Tracks (use first word only!):\n{}\n\nCurrent Time: {}{} ({}){}'.format(co.E, co.BO, ', '.join(f.tracks),co.GR, t, d, co.E))


if __name__ == '__main__':
	__init__()
