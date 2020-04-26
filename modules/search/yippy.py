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
		'name': 'Yippy Search',
		'author': 'Saeeddqn',
		'version': '0.2',
		'description': 'Search your query in the Yippy.com and get result.',
		'sources': ('yippy',),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('method', 'webpages', False, 'Yippy methods("webpages", "images", "news", "video"). default=None', '-m', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('yippy -q <QUERY>', 'yippy -q <QUERY> -m images')
	}

	def module_run(self):
		query = self.options['query']
		method = self.options['method'].lower()
		run = self.yippy(query)
		if method:
			if method == 'webpages':
				run.crawl_with_response_filter(method)
				run.run_crawl()
			else:
				if method in ('images', 'news', 'video'):
					run.crawl_with_response_filter(method)
		else:	
			run.run_crawl()
		links = run.links

		if links == []:
			self.output('Without result')
		else:
			for link in links:
				self.output(f'\t{link}')
				print('')
		self.save_gather(links, 'search/yippy', query, output=self.options['output'])
