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
		'name': 'Web Applications Identifier',
		'author': 'Saeeddqn',
		'version': '0.3',
		'description': 'Web fingerprinting to identify the applications used with over 1000 pyload.',
		'sources': ('wappalyzer.com',),
		'options': (
			('domain', BaseModule._global_options.get('target'), True, 'Domain string', '-d', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('wapps -d <DOMAIN>',)
	}

	def module_run(self):
		domain = self.options['domain']
		req = self.request(domain)
		headers = req.headers
		text = req.text
		resp = {}
		
		v = self.wapps(domain, text, headers)
		wapps = v.run_crawl()
		self.alert('WAPPS')
		resp['wapps'] = []
		for i in wapps:
			self.output(f'\t{i} : {wapps[i]}', 'g')
			resp['wapps'].append((i,wapps[i]))

		_os = self.os_identify(text, headers)
		_os.run_crawl()
		if _os.os:
			resp['os'] = _os.os
			self.alert(f"Used '{_os.os}' operating system")

		cms = self.cms_identify(text, headers)
		cms.run_crawl()
		if cms.cms:
			resp['cms'] = cms.cms
			self.alert(f"Used '{cms.cms}' content management")

		lang = self.lang_identify(text, headers)
		lang.run_crawl()
		if lang.lang:
			resp['lang'] = lang.lang
			self.alert(f"Used '{lang.lang}' programming language")

		self.save_gather(resp, 'footprint/wapps', domain, output=self.options['output'])
