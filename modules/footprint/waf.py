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
		'name': 'WAF(Web Application Firewall) Identifier',
		'author': 'Saeeddqn',
		'version': '0.1',
		'description': 'Identify web application firewalls. It can detect over 200 firewalls.',
		'sources': ('github.com/EnableSecurity/wafw00f',),
		'options': (
			('domain', BaseModule._global_options.get('target'), True, 'Domain string', '-d', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('waf -d <DOMAIN>',)
	}

	def module_run(self):
		domain = self.options['domain']
		req = self.request(domain)
		_wafs = self.waf_identify(req)
		_wafs.run_crawl()

		wafs = _wafs.waf

		self.alert('WAFs')
		if wafs != []:
			for scheme in wafs:
				self.output(f"\t{scheme}", 'g')
		else:
			self.output('\tNo result')

		self.save_gather(wafs, 'footprint/waf', domain, output=self.options['output'])
