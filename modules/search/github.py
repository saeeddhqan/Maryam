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
		'sources': ('google', 'carrot2', 'bing', 'yippy', 'yahoo', 'millionshort','qwant', 'duckduckgo'),
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
		repositories = []
		blogs = []
		users = []
		pages = run.pages

		if 'bing' in engine:
			run = self.bing(q, limit, count)
			run.run_crawl()
			pages += run.pages
			for item in run.links_with_title:
				link,title = item
				self.verbose(title, 'G')
				self.verbose(f"\t{link}")
				self.verbose('')
				links.append(link)

		if 'carrot2' in engine:
			run = self.carrot2(q, limit)
			run.run_crawl()
			pages += run.pages
			for item in run.json_links:
				link = item.get('url')
				self.verbose(item.get('title'), 'C')
				self.verbose(f"\t{link}")
				links.append(link)

		if 'duckduckgo' in engine:
			run = self.duckduckgo(q, limit, count)
			run.run_crawl()
			pages += run.pages
			links += run.links


		if 'yippy' in engine:
			run = self.yippy(q)
			run.run_crawl()
			pages += run.pages
			links += run.links

		if 'yahoo' in engine:
			run = self.yahoo(q, limit, count)
			run.run_crawl()
			pages += run.pages
			links.extend(run.links)

		if 'millionshort' in engine:
			run = self.millionshort(q, limit)
			run.run_crawl()
			pages += run.pages
			links.extend(run.links)

		if 'qwant' in engine:
			run = self.qwant(q, limit)
			run.run_crawl()
			pages += run.pages
			links.extend(run.links)


		links = list(set(links))
		if links == []:
			self.output('Without result')
		else:
			search = self.page_parse(pages).get_networks

			self.alert('blogs')
			for blog in set(search['Github site']):
				self.output(f'\t{blog}', 'G')
				blogs.append(blog)

			self.alert('users')
			for user in set(search['Github']):
				self.output(f'\t{user}', 'G')
				users.append(user)

			repo_reg = re.compile(r"https://(www\.)?(github\.com/[\w_-]{1,39}/[\w\-\.]+)")
			self.alert('repositories')
			for link in filter(repo_reg.match, links):
				rep = repo_reg.search(link).group(0)
				repositories.append(rep)
				title = rep.split('/')[-1].replace('-', ' ').title()
				self.output(title, 'G')
				self.output(f'\t{rep}')

		self.save_gather({'usernames': users, 'repositories': repositories, 'blogs': blogs},\
		 'search/github', query, output=self.options.get('output'))
