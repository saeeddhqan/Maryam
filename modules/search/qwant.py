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
		'name': 'Qwant Search',
		'author': 'Saeeddqn',
		'version': '0.2',
		'description': 'Search your query in the qwant.com and show the results(without limit).',
		'sources': ('qwant',),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('method', 'webpages', False, 'Qwant methods("webpages",\
			 "images", "news", "videos"). default=None', '-m', 'store'),
			('limit', 2, False, 'Search limit(number of pages, default=2)', '-l', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('qwant -q <QUERY>', 'qwant -q <QUERY> -m images -l 3')
	}

	def module_run(self):
		query = self.options['query']
		run = self.qwant(query, self.options['limit'])
		method = self.options['method'].lower()
		if method not in ('webpages', 'images', 'news', 'videos'):
			self.error(f'Method name "{method}" is incorrect!')
			self.verbose('Running with "webpages" method...')
			method = 'webpages'

		run.run_crawl(method)
		links = run.links_with_title

		if links == {}:
			self.output('Without result')
		else:
			for item in links:
				self.output(f"{item.replace('<b>','').replace('</b>', '')}", 'G')
				self.output(f"\t{links[item]}")
				print('')

		self.save_gather(links, 'search/qwant', query, output=self.options['output'])
