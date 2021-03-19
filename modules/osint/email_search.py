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
	'name': 'Find Emails',
	'author': 'Saeed',
	'version': '0.5',
	'description': 'Search in open-sources to find emails.',
	'sources': ('bing', 'google', 'yahoo', 'yandex', 'metacrawler', 
				'ask', 'baidu', 'startpage', 'yippy', 'qwant', 'duckduckgo'),
	'options': (
		('query', None, True, 'Domain name or company name', '-q', 'store', str),
		('limit', 3, False, 'Search limit(number of pages, default=3)', '-l', 'store', int),
		('count', 50, False, 'number of results per page(min=10, max=100, default=50)', '-c', 'store', int),
		('engines', 'google,metacrawler,bing', True, 'Search engine names. e.g bing,google,..', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('email_search -q microsoft.com -e bing --output',
		'email_search -q owasp.org -e google,bing,yahoo -l 20 -t 3 --output')
}

EMAILS = []

def search(self, name, q, q_formats, limit, count):
	global EMAILS
	engine = getattr(self, name)
	name = engine.__init__.__name__
	varnames = engine.__init__.__code__.co_varnames
	if name == 'ask':
		q = q.replace('"', '')
	if 'limit' in varnames and 'count' in varnames:
		attr = engine(q, limit, count)
	elif 'limit' in varnames:
		attr = engine(q, limit)
	else:
		attr = engine(q)
	attr.run_crawl()
	EMAILS.extend(attr.emails)

def module_api(self):
	domain = self.options['query'].replace('@', '')
	urlib = self.urlib(domain)
	domain = self.urlib(domain).netroot if '/' in domain else domain
	limit = self.options['limit']
	count = self.options['count']
	engines = self.options['engines'].split(',')
	query = f'"%40{domain}"'
	self.thread(search, self.options['thread'], engines, query, {}, limit, count, meta['sources'])
	output = list(set(EMAILS))

	self.save_gather(output, 'osint/email_search', domain,\
		output=self.options['output'])
	return output

def module_run(self):
	self.alert_results(module_api(self))
