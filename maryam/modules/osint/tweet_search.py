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

import json

meta = {
	'name': 'Tweet Search',
	'author': 'Kaushik',
	'version': '0.5',
	'description': 'Search tweets from twitter',
	'sources': ('twitter',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 15, False, 'Max result count (default=15)', '-l', 'store', int),
		('verbose', False, False, 'Print all tweet details as json', '-v', 'store_true', bool)
	),
	'examples': ('tweet_search -q <QUERY> -l 15 -- --output',)
}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	verbose = self.options['verbose']
	run = self.twitter(query, limit, verbose)
	run.run_crawl()
	output = {'results': run.tweets}
	self.save_gather(output, 'osint/twitter', query, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)['results']
	if not self.options['verbose']:
		for item in output:
			self.output(item)
	else:
		self.output(json.dumps(output, indent=4))
