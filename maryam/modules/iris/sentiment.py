"""
OWASP Maryam!
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import concurrent.futures as futures
import copy
from json import loads
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

meta = {
	'name': 'sentiment analysis',
	'author': 'Saeed',
	'version': '0.1',
	'description': 'Running sentiment analysis on your data.',
	'required': ('vaderSentiment',),
	'options': (
		('json', None, False, 'Json file that contains the data', '-j', 'store', str),
		('key', '', False, 'Data key. the value should be a list. None means the json file contains a list: ["..", ..]', '-k', 'store', str),
		('thread', 5, False, 'The number of thread per each sell(default=10)', '-t', 'store', int),
		('pipe', False, False, 'Dev only! pipe data from other modules(default=False)', '-p', 'store_true', bool),
	),
	'examples': ('sentiment -j test.json -k data',
		'sentiment -j test.json -t 50')
}
	
SHOW_MSG = {'neg': 'negative', 'neu': 'neutral', 'pos': 'positive', 'compound': 'compound'}

def dothetask(i, j):
	global OVERALL, SA, MAXES
	for cell in DATA[i:j]:
		p = SA.polarity_scores(cell)
		for i in p:
			OVERALL[i] += p[i]
			if MAXES[i] != []:
				if p[i] > MAXES[i][0]:
					MAXES[i] = [p[i], cell]
			else:
				MAXES[i] = [p[i], cell]

def thread(nthread):
	with futures.ThreadPoolExecutor(max_workers=nthread) as executor:
		tire = round(LEN/nthread)
		if tire > 0:
			for i in range(tire+1):
				mx = i*nthread
				executor.submit(dothetask, mx, mx+nthread)
		else:
			executor.submit(dothetask, 0, LEN)

def module_api(self):
	global DATA, LEN, OVERALL, SA, MAXES
	SA = SentimentIntensityAnalyzer()
	OVERALL = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
	MAXES = {'neg': [], 'neu': [], 'pos': [], 'compound': []}
	if not self.options['pipe']:
		json = self.options['json']
		key = self.options['key']
		file = self._is_readable(json)
		if not file:
			return
		DATA = loads(file.read())
		if key not in DATA:
			self.error("The key doesn't exists", 'module_api', 'iris/sentiment')
			return
		if key != '':
			DATA = DATA[key]
	LEN = len(DATA)
	thread(self.options['thread'])
	if self.options['pipe']:
		return {'overall': OVERALL, 'maxes': MAXES}
	output = {json : {key: [OVERALL, MAXES]}}
	self.save_gather(output, 'osint/docs_search', json, \
		[key], output=self.options['output'])
	return output

def module_run(self):
	module_api(self)
	for i in OVERALL:
		self.alert(SHOW_MSG[i])
		self.output(f"\t{OVERALL[i]}")
		if MAXES[i]:
			self.output(f"most {i} sentence: \t{MAXES[i][1]}")
