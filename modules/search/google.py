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

from core.module import BaseModule


class Module(BaseModule):

	meta = {
		'name': 'Google Search',
		'author': 'Saeeddqn',
		'version': '0.2',
		'description': 'Search your query in the google.com and get result.',
		'sources': ('google',),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('google -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		run = self.google(query, limit, count)
		run.run_crawl()
		links = run.links

		if links == []:
			self.output('Without result')
		else:
			for link in links:
				self.output(f'\t{link}')
				print('')
		self.save_gather(links, 'search/google', query, output=self.options['output'])
