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
		'name': 'Web Crawler',
		'author': 'Saeeddqn',
		'version': '0.5',
		'description': 'Crawl web pages to find links, JS Files, CSS files, Comments and everything else interesting, supports concurrency.',
		'options': (
			('domain', BaseModule._global_options['target'], True, 'Domain string', '-d', 'store'),
			('debug', False, False, 'debug the scraper', '--debug', 'store_true'),
			('limit', 1, False, 'Scraper depth level', '-l', 'store'),
			('thread', 1, False, 'The number of links that open per round', '-t', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('crawler -d <DOMAIN>',
			'crawler -d <DOMAIN> -l 10 -t 3 --output --debug')
	}

	def module_run(self):
		domain = self.options['domain']
		run = self.web_scrap(domain, self.options['debug'], self.options['limit'], self.options['thread'])
		run.run_crawl()
		e = {'js': run.js, 'cdn': run.cdn,
			 'query': run.query_links, 'exlinks': run.external_links, 
			 'links': run.links, 'css': run.css, 'comments': run.comments, 
			 'emails' : run.emails, 'phones' : run.phones, 'media' : run.media}

		for obj in e:
			self.alert(f"{obj}({len(e[obj])})")
			if e[obj] == []:
				self.output('\t..')
			else:
				for obj_i in e[obj]:
					self.output(f"\t'{obj_i}'", 'o')

		usernames = run.networks
		links = []
		for net in usernames:
			lst = list(set(usernames[net]))
			if lst != []:
				self.alert(net)
				for link in lst:
					if type(link) is tuple:
						link = list(link)
						for mic in link:
							if len(mic) > 4 and mic != '':
								links.append(mic)
								self.output(f'\t{str(mic)}', 'G')
					else:
						links.append(link)
						self.output(f'\t{str(link)}', 'G')

		e['Social Networks'] = links

		self.save_gather(e, 'osint/crawler', domain, output=self.options['output'])
