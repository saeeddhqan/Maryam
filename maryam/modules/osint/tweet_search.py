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

meta = {
	'name': 'Tweet Search',
	'author': 'Kaushik',
	'version': '0.7',
	'description': 'Search tweets from twitter',
	'required': ('$iris/sentiment',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 15, False, 'Max result count (default=15)', '-l', 'store', int),
		('sentiment', False, False, 'Do sentiment Analysis on tweets(default=False)', '-s', 'store_true', bool),
		('verbose', False, False, 'Print all tweet details as json', '-v', 'store_true', bool)
	),
	'examples': ('tweet_search -q <QUERY> -l 15',
		'tweet_search -q <QUERY> -l 15 --sentiment'
		)
}

SHOW_MSG = {'neg': 'negative', 'neu': 'netural', 'pos': 'positive', 'compound': 'compound'}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	sentiment = self.options['sentiment']
	if sentiment:
		self.options['verbose'] = False
	run = self.tweet_search(query, limit, self.options['verbose'])
	run.run_crawl()
	output = {'results': run.tweets}
	if sentiment:
		if 'sentiment' not in self._loaded_modules:
			self._load_modules('iris')
		sent_mod = self._loaded_modules['sentiment']
		sent_mod.DATA = output['results']
		self.options['pipe'] = True
		self.options['thread'] = 10
		output['sentiment'] = sent_mod.module_api(self)
	self.save_gather(output, 'osint/twitter', query, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)
	if not self.options['verbose']:
		for item in output['results']:
			self.output(item)
		if self.options['sentiment']:
			print()
			sent = output['sentiment']
			for i in sent['overall']:
				self.alert(SHOW_MSG[i])
				self.output(f"\t{sent['overall'][i]}")
				if sent['maxes'][i]:
					self.output(f"most {i} sentence:\t{sent['maxes'][i][1]}")
	else:
		self.output(dumps(output['results'], indent=4))
