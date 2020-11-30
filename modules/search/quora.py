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
import re
import requests

class Module(BaseModule):
	
	meta = {
		'name': 'Quora Search',
		'author': 'Aman Rawat',
		'version': '0.1',
		'description': 'Search your query in the quora.com and get result.',
		'sources': ('yahoo', 'yippy', 'bing', 'google'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store'),
			('engine', 'bing', False, 'Engine names for search(default=bing)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('quora -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		q = f"site:www.quora.com {query}"
		run = self.yahoo(q, limit, count)
		run.run_crawl()
		links = run.links
		pages = run.pages
		titles = []
		profiles = []

		if 'bing' in engine:
			run = self.bing(q, limit, count)
			run.run_crawl()
			pages += run.pages
			for item in run.links_with_title:
				link,title = item
				self.verbose(f'\t{title}', 'C')
				self.verbose(f'\t\t{link}')
				self.verbose('')
				links.append(link)

		if 'google' in engine:
			run = self.google(q)
			run.run_crawl()
			links = run.links

		if 'yippy' in engine:
			run = self.yippy(f'www.quora.com {query}')
			run.run_crawl()
			links = run.links

		
		if links == []:
		 	self.output('Without result')
		else:
			self.alert('profiles')
			for link in links:
				link = link.replace('https://www.quora.com/profile', '').replace('/', '')
				if re.search(r'^[\w\d_\-\/]+$', link):
					profiles.append(link)
					self.output(f"\t{link}", 'G')

			self.alert('raw results')
			for link in links:
				if 'www.quora.com' in link and 'www.quora.com/profile' not in link:
					title = link.replace('https://www.quora.com/', '').replace('/', '')
					title = title.replace('-', ' ')
					title =requests.utils.unquote(title)
					titles.append(title)
					self.output(f'\t{title} \n\t\t{link}')
				

		self.save_gather({'links': links, 'title': titles, 'profiles': profiles},
			'search/quora', query, output=self.options.get('output'))
