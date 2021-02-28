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
		'name': 'Stackoverflow Search',
		'author': 'Sanjiban Sengupta',
		'version': '0.1',
		'description': 'Search your query in the stackoverflow.com and show the results.',
		'sources': ('yahoo', 'yippy', 'bing', 'google', 'carrot2'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False,
			 'Number of results per page(min=10, max=100, default=50)', '-c', 'store'),
			('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('stackoverflow -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		q = f"site:www.stackoverflow.com {query}"
		run = self.google(q, limit, count)
		run.run_crawl()
		links = run.links
		pages = run.pages
		titles = []
		profiles = []
		tags = []

		if 'bing' in engine:
			run = self.bing(q, limit, count)
			run.run_crawl()
			pages += run.pages
			for item in run.links_with_title:
				link, title = item
				self.verbose(f'\t{title}', 'C')
				self.verbose(f'\t\t{link}')
				self.verbose('')
				links.append(link)

		if 'google' in engine:
			run = self.google(q)
			run.run_crawl()
			links = run.links

		if 'yippy' in engine:
			run = self.yippy(f'www.stackoverflow.com {query}')
			run.run_crawl()
			links = run.links

		if 'carrot2' in engine:
			run = self.carrot2(q)
			run.run_crawl()
			pages += run.pages
			for item in run.json_links:
				link = item.get('url')
				self.verbose(item.get('title'), 'C')
				self.verbose(f"\t{link}")
				links.append(link)

		if links == []:
		 	self.output('Without result')
		else:
			self.alert('profiles')
			for link in links:
				link = link.replace('https://stackoverflow.com/users/',
				                    '').replace('/', '')
				if re.search(r'^[\w\d_\-\/]+$', link):
					profiles.append(link)
					self.output(f"\t{link}", 'G')

			self.alert('raw results')
			for link in links:
				if 'www.stackoverflow.com' in link and 'https://stackoverflow.com/users/' not in link:
					title = link.replace('https://stackoverflow.com/users/', '').replace('/', '')
					title = title.replace('-', ' ')
					title = requests.utils.unquote(title)
					titles.append(title)
					self.output(f'\t{title} \n\t\t{link}')
			
			self.alert('tags')
			for link in links:
				if '/tag/' in link:
					link = link.replace('https://stackoverflow.com/tags/', '')
					if re.search(r'^[\w\d_\-]+$', link):
						tags.append(link)
						self.output(f"\t#{link}", 'G')

		self.save_gather({'links': links, 'title': titles, 'profiles': profiles,'tags':tags},
			'search/stackoverflow', query, output=self.options.get('output'))

