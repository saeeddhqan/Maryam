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

from json import dumps
from datetime import datetime

meta = {
	'name': 'Tweet Search',
	'author': 'Kaushik',
	'version': '0.7',
	'description': 'Search tweets from twitter',
	'required': ('$iris',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 15, False, 'Max result count (default=15)', '-l', 'store', int),
		('sentiment', False, False, 'Do sentiment Analysis on tweets(default=False)', '-s', 'store_true', bool),
		('daterange', -1, False, 'Number of past days to fetch tweets for', '-d', 'store', int),
		('monthly', False, False, 'Group datewise sentiment values by month', '-m', 'store_true', bool),
		('verbose', False, False, 'Print all tweet details as json', '-v', 'store_true', bool),
	),
	'examples': ('tweet_search -q <QUERY> -l 15',
		'tweet_search -q <QUERY> -l 15 --sentiment --daterange 2')
}

SHOW_MSG = {'neg': 'negative', 'neu': 'neutral', 'pos': 'positive', 'compound': 'compound'}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	sentiment = self.options['sentiment']
	daterange = self.options['daterange']
	monthly = self.options['monthly']

	if sentiment:
		verbose = False
	else:
		verbose = self.options['verbose']

	run = self.tweet_search(query, limit, verbose, daterange)
	run.run_crawl()

	output = {'results': run.tweets['all'] if daterange == -1 else run.tweets}
	if sentiment:
		if 'sentiment' not in self._loaded_modules:
			self._load_modules('iris')
		output['sentiment'] = {}
		if monthly:
			allmonths = {}
		sent_mod = self._loaded_modules['sentiment']
		self.options['pipe'] = True
		self.options['thread'] = 1
		if daterange == -1:
			sent_mod.DATA = output['results']
			output['sentiment'] = sent_mod.module_api(self)
		else:
			for day in output['results']:
				sent_mod.DATA = output['results'][day]
				output['sentiment'][day] = sent_mod.module_api(self)
				if monthly:
					month = datetime.strptime(day, '%Y-%m-%d').strftime('%B')
					curr_day = output['sentiment'][day]

					if month not in allmonths:
						allmonths[month] = {}
						allmonths[month]['maxes'] = curr_day['maxes']
						allmonths[month]['overall'] = curr_day['overall']
						allmonths[month]['count'] = 1

					else:
						for key in SHOW_MSG:
							if allmonths[month]['maxes'][key][0] < curr_day['maxes'][key][0]:
								allmonths[month]['maxes'][key] = curr_day['maxes'][key]
						value = allmonths[month]['overall'][key]
						count = allmonths[month]['count']
						allmonths[month]['count'] += 1
						allmonths[month]['overall'][key] = (value*(count)+curr_day['overall'][key])/count+1

			if monthly:
				output['sentiment']['monthly'] = allmonths

	self.save_gather(output, 'osint/twitter', query, output=self.options['output'])
	return output

	

def module_run(self):
	sentiment = self.options['sentiment']
	daterange = self.options['daterange']
	monthly = self.options['monthly']
	output = module_api(self)

	def print_sentiment(sent):
		for i in sent['overall']:
			self.alert(SHOW_MSG[i])
			self.output(f"\t{sent['overall'][i]}")
			if sent['maxes'][i]:
				self.output(f"\tmost {SHOW_MSG[i]} sentence:  {sent['maxes'][i][1]}")

	if not self.options['verbose']:
		if daterange != -1:
			for day in output['results']:
				print()
				self.output(day)
				for tweet in output['results'][day]:
					self.output(tweet)
				if sentiment:
					print()
					self.alert('Sentiment')
					sent = output['sentiment'][day]
					print_sentiment(sent)
			if sentiment and monthly:
				print()
				self.output('Monthwise Sentiment Aggregate')
				allmonths = output['sentiment']['monthly']
				for month in allmonths:
					self.alert(f"Month: {month}")
					print_sentiment(allmonths[month])
					print()

		else:
			for tweet in output['results']:
				self.output(tweet)

			if sentiment:
				print()
				sent = output['sentiment']
				print_sentiment(sent)
	else:
		self.output(dumps(output, indent=4))
