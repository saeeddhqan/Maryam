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
		'name': 'Search engine suggestions',
		'author': 'Qux',
		'version': '0.1',
		'description': 'Keyword autocompleter to find suggestions in search engines',
		'sources': ('google', 'bing', 'yahoo', 'searx', 'peekier', 'gigablast', 'zapmeta', 'millionshort'),
		'comments': (
			"""example: query='google' out: ['google docs', 'google summer of code', 'google maps', 'google mail', 'google news', ..]""",
		),
		'options': (
			('query', None, True, 'keyword, domain name, company name, etc', '-q', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
        'examples': ('suggest -q amazon --output',)

	}

	def module_run(self):
		q = self.options['query']
		run = self.keywords(q)
		run.run_crawl()
		suggests = run.keys
		
		if suggests == []:
			self.output('Nothing to declare')
		else:
			for suggest in suggests:
				self.output(f'\t{suggest}')
		self.save_gather(suggests, 'osint/suggest', q, output=self.options['output'])
