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
		'name': 'Linkedin Search',
		'author': 'Saeeddqn',
		'version': '0.4',
		'description': 'Search your query in the linkedin.com and get result.',
		'sources': ('google','carrot2','bing'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store'),
			('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('linkedin -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		q = f"site:linkedin.com {query}"
		run = self.google(q, limit, count)
		run.run_crawl()
		links = run.links
		pages = run.pages
		people = []

		if 'bing' in engine:
			run = self.bing(q, limit, count)
			run.run_crawl()
			pages += run.pages 
			for item in run.links_with_title:
				link,title = item
				self.verbose(f'{title}', 'C')
				self.verbose(f'\t{link}')
				links.append(link)

		if 'carrot2' in engine:
			run = self.carrot2(q)
			run.run_crawl()
			pages += run.pages 
			for item in run.json_links:
				link = item.get('url')
				self.verbose(item.get('title'), 'C')
				self.verbose(f"\t{link}")
				links.append(link)

		usernames = self.page_parse(pages).get_networks
		self.alert('People')
		for net in usernames:
			lst = list(set(usernames[net]))
			if lst != []:
				self.alert(net)
				for link in lst:
					if type(link) is tuple:
						link = list(link).pop(link.index(''))
						for mic in link:
							if len(mic) > 2:
								mic = mic[mic.find('/')+1:]
								mic = mic.replace('company/', '').replace('in/', '').replace('\\x22', '')
								mic = f"@{mic}"
								people.append(mic)
								self.output(f'\t{mic}', 'G')
					else:
						link = link[link.find('/')+1:]
						link = link.replace('company/', '').replace('in/', '').replace('\\x22', '')
						link = f"@{link}"
						people.append(link)
						self.output(f'\t{link}', 'G')
		self.alert('links')
		if links == []:
			self.output('Without result')
		else:

			for link in links:
				self.output(f'\t{link}')

		self.save_gather(links, 'search/linkedin', query, output=self.options.get('output'))
