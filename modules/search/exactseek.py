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

import lxml

meta = {
	'name': 'Exactseek Search',
	'author': 'Divya Goswami',
	'version': '1.0',
	'description': 'Backend engine for activesearch. Gives better SEO based results',
	'sources': ('exactseek.com',),
	'options': (
		('query', '', False, 'Enter a location name', '-q', 'store', str),
		('engine', 'exactseek', False, 'Engine used is photon', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('exactseek -q OSINT --output',)
	}

def module_api(self):
	global PAGES
	query = self.options['query']
	engine = self.options['engine']
	output = {}
	run = self.exactseek(query)
	run.run_crawl()
	PAGES = run.pages

	self.save_gather(output, 'search/exactseek', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)