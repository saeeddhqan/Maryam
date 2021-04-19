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
import json

meta = {
	'name': 'Duckduckgo d.js',
	'author': 'Vikas Kundu',
	'version': '0.1',
	'description': 'Search for a query using the d.js file of duckduckgo',
	'sources': ('Google Pagespeed API','DuckDuckGo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
	),
	'examples': ('d_js -q <QUERY> --output',)
}

def search(self, query):
	self.verbose('[d_js] Searching for d.js url...')
	duck_url = f"https://duckduckgo.com/?q={query}"

	try:
		page_data = self.request(duck_url).text
	except Exception as e:
		self.error('Unable to reach DuckDuckGo!', 'modules/search', 'search')
		return ''

	urls = re.findall(r"/d\.js\?q=[^']+", page_data)

	if not urls:
		self.error('Unable to find d.js link in request!', 'modules/search', 'search')
		return ''

	final_url = f"https://links.duckduckgo.com{urls[0]}"
	return final_url
	
def data_filter(data):
	data = re.sub(r"<[^>]*>", '', data) # Remove all html tags
	data = re.findall(r"\{\"[a-zA-Z]{1,2}[^\}]*\}", data) # Find all dict elements with alphabet as key
	data = [ json.loads(i) for i in data if '"a"' in i ] # Convert to dict all elements containing key "a" 
	return data
	
def module_api(self):
	query = self.options['query']
	output = {'results': []}
	d_js_url = ''
	# These headers needed to avoid empty data in d.js request
	header_data = {'Host': 'links.duckduckgo.com',
		'Referer': 'https://duckduckgo.com/',
		'DNT': '1',
		'Connection': 'keep-alive',
		'TE': 'Trailers'
	}

	d_js_url = search(self, query)
	if not d_js_url:
		return output

	self.verbose('[d_js] Parameters for d.js file found, sending direct request...')
	try:
		# Redirects should be False to avoid error redirects after many tries.
		d_js_data = self.request(url=d_js_url, allow_redirects=False, headers=header_data).text		
	except Exception as e:
		self.error('Unable to reach duckduckgo', 'modules/search', 'module_api')
		return output

	result = data_filter(d_js_data)

	output['results'] = result
	self.save_gather(output, 'search/d_js', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))

