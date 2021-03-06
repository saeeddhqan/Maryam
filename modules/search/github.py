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

class Module(BaseModule):

	meta = {
		'name': 'GitHub Search',
		'author': 'Aman Singh',
		'version': '0.1',
		'description': 'Search your query in the GitHub and show the results.',
		'sources': ('google', 'carrot2', 'bing', 'yippy', 'yahoo', 'millionshort','qwant'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store'),
			('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('github -q <QUERY> -l 15 -e carrot2,bing,qwant --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		q = f"site:github.com {query}"

		run = self.google(q, limit, count)
		run.run_crawl()
		links = run.links
		users = []
		repository = []
		pages = run.pages

		if 'bing' in engine:
			run = self.bing(q, limit, count)
			run.run_crawl()
			pages += run.pages
			for item in run.links_with_title:
				link,title = item
				self.verbose(f"\t{title}", 'C')
				self.verbose(f"\t\t{link}")
				self.verbose('')
				links.append(link)

		if 'carrot2' in engine:
			run = self.carrot2(google_q)
			run.run_crawl()
			pages += run.pages
			for item in run.json_links:
				link = item.get('url')
				self.verbose(item.get('title'), 'C')
				self.verbose(f"\t{link}")
				links.append(link)

		if 'yippy' in engine:
			run = self.yippy(yippy_q)
			run.run_crawl()
			links += run.links

		if 'yahoo' in engine:
			run = self.yahoo(q, limit, count)
			run.run_crawl()
			links.extend(run.links)

		if 'millionshort' in engine:
			run = self.millionshort(q, limit)
			run.run_crawl()
			links.extend(run.links)

		if 'qwant' in engine:
			run = self.qwant(q, limit)
			run.run_crawl()
			links.extend(run.links)


		links = list(set(links))
		if links == []:
			self.output('Without result')
		else:
			self.alert('Users')
			for link in links:
				try:
					link = link.split('/')[3]
				except:
					continue
				if re.search(r'^[\w\d_\-\/]+$', link):
					if(link not in users):
						users.append(link)
						self.output(f"\t{link}", 'G')

			self.alert('Repository')
			for link in links:
				try:
					link = link.split('/')[3] + '/' + link.split('/')[4]
				except:
					continue
				if re.search(r'^[\w\d_\-\/]+$', link):
					if(link not in repository):
						repository.append(link)
						self.output(f"\t{link}", 'G')

			self.alert('Links')
			for link in links:
				self.output(f'\t{link}')

		self.save_gather({'users': users, 'repo': repository,}, 'search/github', query, output=self.options.get('output'))
