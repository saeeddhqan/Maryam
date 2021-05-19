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


meta = {
	'name': 'Google Scholar',
	'author': 'Kaushik',
	'version': '0.1',
	'description': 'Google Scholar is a freely accessible web search engine that \
		indexes scholarly literature across an array of publishing formats and disciplines.',
	'sources': ('scholar'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 15, False, 'Max result count (default=15)', '-l', 'store', int),
	),
	'examples': ('scholar -q <QUERY> -l 15 --output',)
}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	run = self.scholar(query, limit)
	run.run_crawl()
	output = {'results': run.results}
	self.save_gather(output, 'search/scholar', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
