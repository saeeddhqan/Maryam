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
		'name': 'Google Dork Search',
		'author': 'Saeeddqn',
		'version': '0.2',
		'description': 'Search google for your dork and get result.',
		'sources': ('google',),
		'options': (
			('dork', None, True, 'Google dork string', '-d', 'store'),
			('limit', 2, False, 'Search limit(number of pages, default=2)', '-l', 'store'),
			('count', 50, False, 'number of results per page(min=10, max=100, default=50)', '-c', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('godork -d <DORK> -l 15 --output',)

	}

	def module_run(self):
		dork = self.options['dork']
		limit = self.options['limit']
		count = self.options['count']
		run = self.google(dork, limit, count)
		run.run_crawl()
		links = run.links
		
		if links == []:
			self.output('Nothing to declare')
		else:
			for link in links:
				self.output(f'\t{link}')
		self.save_gather(links, 'osint/godork', dork, output=self.options['output'])
