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
	'name': 'Pubmed',
	'author': 'Kaushik',
	'version': '0.1',
	'description': 'PubMed comprises more than 32 million citations for biomedical \
		literature from MEDLINE, life science journals, and online books.',
	'sources': ('pubmed',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('count', 15, False, 'Max result count (default=15)', '-c', 'store', int),
	),
	'examples': ('pubmed -q <QUERY> -l 15 --output',)
}

def module_api(self):
	query = self.options['query']
	count = self.options['count']
	run = self.pubmed(query, count)
	run.run_crawl()
	output = {'results': run.results}
	self.save_gather(output, 'search/pubmed', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
