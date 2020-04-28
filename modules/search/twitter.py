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
		'name': 'Twitter Search',
		'author': 'Saeeddqn',
		'version': '0.3',
		'description': 'Search your query in the twitter.com and get result.',
		'sources': ('google', 'carrot2', 'bing'),
		'options': (
			('query', None, True, 'Query string', '-q', 'store'),
			('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
			('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store'),
			('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('twitter -q <QUERY> -l 15 --output',)
	}

	def module_run(self):
		query = self.options['query']
		limit = self.options['limit']
		count = self.options['count']
		engine = self.options['engine'].split(',')
		q = f"site:twitter.com {query}"
		run = self.google(q, limit, count)
		run.run_crawl()
		links = run.links
		people = []
		hashtags = []
		pages = run.pages

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
		for _id in list(set(usernames.get('Twitter'))):
			if type(_id) is tuple:
				_id = _id[0]
				_id = f"@{_id[_id.find('/')+1:]}"
				people.append(_id)
				self.output(f'\t{_id}', 'G')
			else:
				_id = f"@{_id[_id.find('/')+1:]}"
				people.append(_id)
				self.output(f'\t{_id}', 'G')

		if links == []:
			self.output('Without result')
		else:
			self.alert('Hashtags')
			for link in links:
				if '/hashtag/' in link:
					link = link.replace('https://twitter.com/hashtag/', '')
					if re.search(r'^[\w\d_\-]+$', link):
						hashtags.append(link)
						self.output(f"\t#{link}", 'G')

			self.alert('links')
			for link in links:
				self.output(f'\t{link}')

		self.save_gather({'links': links, 'people': people, 'hashtags': hashtags}, 'search/twitter', query, output=self.options.get('output'))
