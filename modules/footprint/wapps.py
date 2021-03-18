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

from json import loads

meta = {
	'name': 'Web Applications Identifier',
	'author': 'Saeed',
	'version': '0.3',
	'description': 'Web fingerprinting to identify the applications used with over 1000 pyload.',
	'sources': ('wappalyzer.com', 'github.com/EnableSecurity/wafw00f'),
	'options': (
		('domain', None, True, 'Domain string', '-d', 'store', str),
	),
	'examples': ('wapps -d <DOMAIN>',)
}

def module_api(self):
	domain = self.options['domain']
	req = self.request(domain)
	urlib = self.urlib(domain)
	query = urlib.sub_service('http')
	headers = req.headers
	text = req.text
	resp = {}
	_wafs = self.waf_identify(req)
	_wafs.run_crawl()
	wafs = _wafs._waf
	resp['waf'] = wafs
	v = self.wapps(domain, text, headers)
	wapps = v.run_crawl()
	resp['wapps'] = wapps

	_os = self.os_identify(text, headers)
	_os.run_crawl()
	if _os.os:
		resp['os'] = _os.os

	cms = self.cms_identify(text, headers)
	cms.run_crawl()
	if cms.cms:
		resp['cms'] = cms.cms

	lang = self.lang_identify(text, headers)
	lang.run_crawl()
	if lang.lang:
		resp['lang'] = lang.lang

	self.save_gather(resp, 'footprint/wapps', domain, output=self.options['output'])
	return resp

def module_run(self):
	self.alert_results(module_api(self))
