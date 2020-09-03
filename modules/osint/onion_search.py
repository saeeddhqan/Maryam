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
		'name': 'Onions Network Search',
		'author': 'Saeeddqn',
		'version': '0.4',
		'description': 'onion_search is used to create the premier search engine for services residing on the Tor anonymity network.',
		'sources': ('ahmia','onionland'),
		'options': (
			('query', BaseModule._global_options['target'], True, 'Domain Name, Company Name, keyword, etc', '-q', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('onion_search -q <KEYWORD|COMPANY>', 'onion_search -q <KEYWORD|COMPANY> --output')
	}

	def module_run(self):
		q = self.options['query']
		ahmia = self.ahmia(q)
		ahmia.run_crawl()
		links = ahmia.links
		onionland = self.onionland(q, limit=5)
		onionland.run_crawl()
		links.extend(onionland.links)

		links = list(set(links))
		if links != []:
			for link in links:
				self.output(f'\t{link}')
		else:
			self.output('Nothing to declare', 'O')
			return
		self.save_gather({'links' : links}, 'osint/onion_search', q, output=self.options['output'])
