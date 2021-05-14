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
	'version': '1.0',
	'description': 'Search in open-sources to find emails.',
	'sources': ('bing', 'pastebin', 'google', 'yahoo', 'yandex', 'metacrawler',
				'ask', 'baidu', 'startpage', 'qwant', 'duckduckgo', 'hunter', 'gigablast', 'github'),
	'options': (
		('query', None, True, 'Domain name or company name', '-q', 'store', str),
		('limit', 3, False, 'Search limit(number of pages, default=3)', '-l', 'store', int),
		('count', 50, False, 'number of results per page(min=10, max=100, default=50)', '-c', 'store', int),
		('engines', None, True, 'Search engine names. e.g bing,google,..', '-e', 'store', str),
		('key', None, False, 'Give a valid hunter API key. Limit for free plan is 10 results', '-k', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('email_search -q microsoft.com -e bing --output',
		'email_search -q owasp.org -e google,bing,yahoo -l 20 -t 3 --output')
}

EMAILS = []

def search(self, name, q, q_formats, limit, count):
	global EMAILS
	engine = getattr(self, name)
	eng = name
	varnames = engine.__init__.__code__.co_varnames
	q = q_formats[f"{eng}"] if f"{eng}" in q_formats else q_formats['default']
	if 'limit' in varnames and 'count' in varnames:
		attr = engine(q, limit, count)
	elif 'limit' in varnames and 'key' in varnames:
		key = q.split('&api_key=')[1]
		k_q = q.split('&api_key=')[0]
		if key == 'None':
			self.error('-k <API KEY> is required for hunter', 'email_search', 'search')
			return
		else:
			attr = engine(k_q, key, limit)
	elif 'limit' in varnames:
		attr = engine(q, limit)
	else:
		attr = engine(q)
	
	attr.run_crawl()
	EMAILS.extend(attr.emails)

def module_api(self):
	query = self.options['query']
	domain = self.options['query'].replace('@', '')
	urlib = self.urlib(domain)
	domain = self.urlib(domain).netroot if '/' in domain else domain
	limit = self.options['limit']
	count = self.options['count']
	engines = self.options['engines'].split(',')
	key = self.options['key']
	q_formats = {
		'default': f'"%40{domain}"',
		'ask': f"%40{domain}",
		'hunter': f"{domain}&api_key={key}",
		'github': domain
	}
	self.thread(search, self.options['thread'], engines, query, q_formats, limit, count, meta['sources'])
	output = {'emails': list(set(EMAILS))}
	
	self.save_gather(output, 'osint/email_search', domain,\
		output=self.options['output'])
	return output

def module_run(self):
	self.alert_results(module_api(self))
