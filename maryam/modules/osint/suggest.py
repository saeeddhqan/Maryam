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
	'name': 'Search engine suggestions',
	'author': 'Saeed',
	'version': '0.1',
	'description': 'Keyword autocompleter to find suggestions in search engines',
	'sources': ('google', 'bing', 'yahoo', 'searx', 'peekier', 'gigablast', 'zapmeta', 'millionshort'),
	'comments': (
		"""example: query='google' out: ['google docs', 'google summer of code', 'google maps', 'google mail', 'google news', ..]""",
	),
	'options': (
		('query', None, True, 'keyword, domain name, company name, etc', '-q', 'store', str),
	),
	'examples': ('suggest -q amazon --output',)

}

def module_api(self):
	q = self.options['query']
	run = self.keywords(q)
	run.run_crawl()
	output = {'suggestions': run.keys}
	self.save_gather(output, 'osint/suggest', q, output=self.options['output'])
	return output

def module_run(self):
	self.alert_results(module_api(self))
