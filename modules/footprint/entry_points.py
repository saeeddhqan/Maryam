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

import json

meta = {
	'name': 'Find Web Entry Points',
	'author': 'Saeed',
	'version': '0.1',
	'description': 'Crawl web pages to find entry points(inputs, urls with param).',
	'options': (
		('domain', None, True, 'Domain string', '-d', 'store', str),
		('debug', False, False, 'debug the scraper', '--debug', 'store_true', bool),
		('limit', 1, False, 'Scraper depth level', '-l', 'store', int),
		('thread', 1, False, 'The number of links that open per round', '-t', 'store', int),
	),
	'examples': ('entry_points -d <DOMAIN>', 'entry_points -d <DOMAIN> --output --debug -l 10 -t 3')
}

def module_api(self):
	domain = self.options['domain']
	run = self.web_scrap(domain, self.options['debug'], self.options['limit'], self.options['thread'])
	run.run_crawl()
	get = run.query_links
	parser = self.page_parse(run.pages)
	forms = parser.get_forms
	urls = {}
	urlib = self.urlib('null')
	for link in get:
		params = urlib.self_params(link)
		urls.update(params)
	output = {'params': urls, 'forms': forms}
	self.save_gather(output, 'footprint/entry_points', domain, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)
	self.alert('FORMS')
	print(json.dumps(output['forms'], indent=4))
	print(json.dumps(output['params'], indent=4))
