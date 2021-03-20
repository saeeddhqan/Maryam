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


meta = {
	'name': 'Yippy Search',
	'author': 'Saeed',
	'version': '0.2',
	'description': 'Search your query in the yippy.com and show the results.',
	'sources': ('yippy',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('method', 'webpages', False, \
			'Yippy methods("webpages", "images", "news", "video"). default=None', '-m', 'store', str),
	),
	'examples': ('yippy -q <QUERY>', 'yippy -q <QUERY> -m images')
}

def module_api(self):
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
	self.save_gather({'links': links}, 'search/yippy', query, output=self.options['output'])
	return links

def module_run(self):
	self.alert_results(module_api(self))