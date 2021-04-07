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
	'name': 'Search Portal',
	'author': 'Aman Singh',
	'version': '0.1',
	'description': 'Search your query using the searchportal.co(Google CSE) and show the results.',
	'sources': ('searchportal',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 10, False, 'Max result count (default=10)', '-l', 'store', int),
	),
	'examples': ('searchportal -q <QUERY>',)
}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	run = self.searchportal(query, 0 ,limit)
	run.run_crawl()

	output = {'results': [[link.get('titleNoFormatting'), link.get('contentNoFormatting'), link.get('url')] for link in run.json_links]}

	self.save_gather(output, 'search/searchportal', query, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)
	for item in output['results']:
		title, desc, link = item[0], re.sub('\r?\n', ' ', item[1]), item[2]
		self.output(title)
		self.output(f"\t{desc}", 'G')
		self.output(f"\t{link}", 'G')
