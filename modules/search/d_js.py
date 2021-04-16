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
import re

meta = {
	'name': 'Duckduckgo d.js',
	'author': 'Vikas Kundu',
	'version': '0.1',
	'description': 'Search for a query using the d.js file of duckduckgo',
	'sources': ('Google Pagespeed API','DuckDuckGo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('retry', 5, False, 'Retries(default=5)', '-r', 'store', int),
	),
	'examples': ('d_js -q <QUERY> --output',)
}

def api_search(self, query):
	self.verbose('[d_js] Searching in Google Pagespeed API...')
	api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://www.duckduckgo.com/?q={query}"

	try:
		google_api_data = self.request(api_url, timeout=20).json()
	except Exception as e:
		self.error('[d_js] Unable to reach Google Pagespeed API!', 'modules/search', 'source1')
		return ''
		
	if 'error' in google_api_data.keys():
		self.error(f"[d_js] {google_api_data['error']['message']}", 'modules/search', 'source1')
		return ''
	
	for i in google_api_data['lighthouseResult']['audits']['bootup-time']['details']['items']:
		if re.search(r"https://links.duckduckgo.com/d.js.*", i['url']):
        		return i['url']
	return ''
	
def module_api(self):
	query = self.options['query']
	retry = self.options['retry']
	output = {'results': ''}
	d_js_url = ''

	for i in range(0, retry):
		self.verbose(f"[d_js] Pagespeed API Try no: {i+1}...")
		d_js_url = api_search(self, query)
		if d_js_url:
			break
		elif i+1 == retry:
			return output

	self.verbose('[d_js] Parameters for d.js file found, sending direct request...')
	try:
		d_js_data = self.request(d_js_url).text
	except Exception as e:
		self.error('[d_js] Unable to reach duckduckgo', 'modules/search', 'module_api')
		return output

	output['results'] = d_js_data
	self.save_gather(output, 'search/d_js', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
