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
	'name': 'Onions Network Search',
	'author': 'Saeed',
	'version': '0.4',
	'description': 'onion_search is used to create the premier \
	search engine for services residing on the Tor anonymity network.',
	'sources': ('ahmia', 'onionland', 'darksearch'),
	'options': (
		('query', None, True, 'Domain Name,\
			Company Name, keyword, etc', '-q', 'store', str),
	),
	'examples': ('onion_search -q <KEYWORD|COMPANY>', 'onion_search -q <KEYWORD|COMPANY> --output')
}

def module_api(self):
	q = self.options['query']
	ahmia = self.ahmia(q)
	ahmia.run_crawl()
	links = ahmia.links
	output = {'links': []}
	onionland = self.onionland(q, limit=5)
	onionland.run_crawl()
	links.extend(onionland.links)

	darksearch = self.darksearch(q, limit=1)
	darksearch.run_crawl()
	links.extend(darksearch.links)

	output['links'] = list(set(links))
	self.save_gather(output, 'osint/onion_search', q, output=self.options['output'])
	return output

def module_run(self):
	self.alert_results(module_api(self))
