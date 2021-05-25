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
        'name': 'Gigablast',
        'author': 'Kaushik',
        'version': '0.1',
        'description': 'Gigablast provides large-scale, high-performance, \
			real-time information retrieval technology and services for partner sites',
        'sources': ('gigablast',),
        'options': (
                ('query', None, True, 'Query to search', '-q', 'store', str),
		('limit', 15, False, 'Max result count (default=15)', '-l', 'store', int),
        ),
        'examples': ('gigablast -q <QUERY> -l 20',)
}

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	run = self.gigablast(query, limit)
	run.run_crawl()
	output = {'results': run.results}

	self.save_gather(output, 'search/gigablast', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
