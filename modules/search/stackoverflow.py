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
		'name': 'StackOverFlow Search',
		'author': 'Sanjiban Sengupta',
		'version': '0.2',
		'description': 'Search your query in the stackoverflow.com and show the results.',
		'sources': ('yippy', 'bing', 'google', 'carrot2'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False,
			 'Number of results per page(min=10, max=100, default=50)', '-c', 'store'),
			('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to the workspace', '--output', 'store_true'),
		),
		'examples': ('stackoverflow -q "syntax error" -l 15 --output',)
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
				self.verbose(f"\t{title}", 'C')
				self.verbose(f"\t\t{link}")
				self.verbose('')
				links.append(link)

		if 'yippy' in engine:
			run = self.yippy(f"www.stackoverflow.com {query}")
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

		links = list(set(links))
		if links == []:
		 	self.output('Without result')
		else:
			self.alert('Questions')
			for link in links:
				first_type = re.search(r'stackoverflow\.com/questions/[\d]+/([\w\d\-_]+)/?', link)
				second_type = re.search(r'stackoverflow\.com/a/[\d+]/?', link)
				if first_type:
					title = first_type.group(1).replace("-", " ").title()
					title = self.urlib(title).unquote
					titles.append(title.title())
					self.output(title, 'C')
					self.output(f'\t{link}')
				elif second_type:
					self.output('Without Title', 'C')
					self.output(f'\t{link}')

			self.alert('profiles')
			for link in links:
				link = link.replace('https://stackoverflow.com/users/',
				                    '').replace('/', '')
				if re.search(r'^[\w\d_\-\/]+$', link):
					profiles.append(link)
					self.output(f"\t{link}", 'G')

			self.alert('Tags')
			for link in links:
				if '/tag/' in link:
					link = link.replace('https://stackoverflow.com/tags/', '')
					if re.search(r'^[\w\d_\-]+$', link):
						tags.append(link)
						self.output(f"\t#{link}", 'G')

		self.save_gather({'links': links, 'titles': titles, 'profiles': profiles, 'tags': tags},
			'search/stackoverflow', query, output=self.options.get('output'))

