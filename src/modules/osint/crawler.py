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
	'name': 'Web Crawler',
	'author': 'Saeed',
	'version': '0.5',
	'description': 'Crawl web pages to find links, JS Files, CSS files, Comments\
	 and everything else interesting, supports concurrency.',
	'options': (
		('domain', None, True, 'Domain string', '-d', 'store', str),
		('debug', False, False, 'debug the scraper', '--debug', 'store_true', bool),
		('limit', 1, False, 'Scraper depth level', '-l', 'store', int),
		('thread', 1, False, 'The number of links that open per round', '-t', 'store', int),
	),
	'examples': ('crawler -d <DOMAIN>',
		'crawler -d <DOMAIN> -l 10 -t 3 --output --debug')
}

def module_api(self):
	domain = self.options['domain']
	run = self.web_scrap(domain, self.options['debug'], self.options['limit'], self.options['thread'])
	run.run_crawl()
	output = {'js': run.js, 'cdn': run.cdn,
		 'getlinks': run.query_links, 'exlinks': run.external_links, 
		 'links': run.links, 'css': run.css, 'comments': run.comments, 
		 'emails': run.emails, 'phones': run.phones, 'media': run.media}
	output['usernames'] = run.networks
	self.save_gather(output, 'osint/crawler', domain, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)
	for obj in output:
		self.alert(f"{obj}({len(output[obj])})")
		if output[obj] == []:
			self.output('\t..')
		else:
			for obj_i in output[obj]:
				if obj == 'usernames':
					if output[obj][obj_i] != []:
						self.output(f"\t{obj_i}")
						for user in output[obj][obj_i]:
							self.output(f"\t\t{user}", 'G')
				else:
					self.output(f"\t{obj_i}", 'G')
