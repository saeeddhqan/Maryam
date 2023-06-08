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


import re

meta = {
	'name': 'Pastebin Search',
	'author': 'Divya Goswami',
	'version': '1.1',
	'description': 'Search your query in the pastebin.com and show the results as paste links.',
	'sources': ('pastebin',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store', int),
	),
	'examples': ('pastebin -q passwords -l 15 --output',)
}


def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	output = {'pastes': []}
	pastebin = self.pastebin(query, limit, count)
	pastebin.run_crawl()
	output['pastes'] = pastebin.links_and_titles
	self.save_gather(output, 'search/pastebin', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)
	for i in range(len(output['pastes'])):
		self.output(f"{output['pastes'][i][1]}", 'G')
		self.output(f"\t{output['pastes'][i][0]}", 'N')
	output.pop('pastes')
	self.alert_results(output)
