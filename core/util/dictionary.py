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
import json

class main:

		def __init__(self, q):
			""" Google Dictionary search engine
					q     : Query to search
			"""
			self.framework = main.framework
			self.q = q
			self._json = ''
			self.dictionary = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'

		def run_crawl(self):
			self.q = self.framework.urlib(self.q).quote
			self.url = f"{self.dictionary}{self.q}"

			self.framework.verbose('Searching Dictionary...')
			try:
				req = self.framework.request(url=self.url)
				self._json = req.json()
			except:
				self.framework.error('ConnectionError.', 'util/dictionary', 'run_crawl')
				self.framework.error('Dictionary is missed!', 'util/dictionary', 'run_crawl')

		@property
		def json(self):
			return self._json

		@property
		def raw(self):
			return json.dumps(self._json)

		@property
		def definitions(self):
			definition_list = []

			if not (type(self._json) == dict and \
					self._json.get('title') == 'No Definitions Found'):
				for context in self._json:
					meanings = context['meanings']
					if len(meanings) > 0:
						for meaning in meanings:
							partOfSpeech = meaning['partOfSpeech']
							definition_sections = meaning['definitions']

							for section in definition_sections:
								definition_list.append({
									'partOfSpeech': partOfSpeech.title(),
									'definition': section['definition']
									})
			return definition_list
