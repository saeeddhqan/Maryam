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

class main:

	def __init__(self, q):
		""" to find suggestions for keywords
			example:
			in: 'google'
			out: ['google docs', 'google summer of code', 'google maps', 'google mail', 'google news', ..]

			q 	: Query string
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self._keys_category = []
		self._keys = []
		self._yahoo = \
			'https://search.yahoo.com/sugg/gossip/gossip-us-ura/?f=1&output=sd1&command=<Q>&pq=a&l=3&nresults=30000&b=3&s=1c&callback=<b>'
		self._google = 'https://www.google.com/complete/search?q=<Q>&cp=&client=psy-ab&xssi=t&gs_ri=gws-wiz&hl=&authuser=0&psi='
		self._bing = 'https://www.bing.com/AS/Suggestions?pt=&mkt=de-de&qry=<Q>&cp=0&css=0&cvid=1'
		self._millionshort = 'https://millionshort.com/api/suggestions?q=<Q>'
		self._zapmeta = 'https://www.zapmeta.com/suggest?q=<Q>'
		self._searx = 'https://searx.be/autocompleter?q=<Q>'
		self._peekier = {'url': 'https://search.peekier.com/suggestions', 'payload': {'q': '<Q>', 'region': ''}, 'method': 'POST'}
		self._gigablast = 'http://gigablast.com/qs?rwp=0&lang=en&q=<Q>'

	def run_crawl(self):
		keys = {}
		for source in ('yahoo', 'google', 'bing', 'millionshort',\
						'zapmeta', 'searx', 'peekier', 'gigablast'):
			attr = getattr(self, '_'+source)
			if isinstance(attr, dict):
				url = attr['url']
				method = 'POST'
				data = attr.get('payload', {'q':'<Q>'})
				data['q'] = self.q
			else:
				url = attr.replace('<Q>', self.q)
				method = 'GET'
				data = {}
			try:
				req = self.framework.request(url, method=method, data=data)
			except Exception as e:
				self.framework.error('ConnectionError', 'util/keywords', 'run_crawl')
				self.framework.print_exception()
			keys[source] = req

		keys['yahoo'] = [x['k'] for x in keys['yahoo'].json().get('r', [])]
		try:
			google = json.loads(f"{keys['google'].text[5:]}")[0]
			keys['google'] = [re.sub(r"<b>|<\\/b>|</b>", '', x[0]) for x in google]
		except:
			keys['google'] = []
		keys['bing'] = re.findall(r'<span class="sa_tm_text">([^<]+)</span>', re.sub(r'<.?strong>', '', keys['bing'].text))
		keys['zapmeta'] = [x[0] for x in keys['zapmeta'].json()] if hasattr(keys['zapmeta'], 'json') else []
		keys['millionshort'] = keys['millionshort'].json().get('suggestions', []) if hasattr(keys['millionshort'], 'json') else []
		try:
			keys['searx'] = keys['searx'].json()[self.q]
		except:
			keys['searx'] = []
		keys['peekier'] = keys['peekier'].json()['results']
		keys['gigablast'] = re.findall(r'" >([^\n]+?)</td', keys['gigablast'].text)
		self._keys_category = keys
		for s in keys:
			for i in keys[s]:
				self._keys.append(i)

	@property
	def keys_category(self):
		return self._keys_category

	@property
	def keys(self):
		return list(set(self._keys))
