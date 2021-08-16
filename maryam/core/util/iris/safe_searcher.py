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

from inspect import signature

class main:
	def __init__(self, engine_q=None):
		self.framework = main.framework

		if engine_q is None:
			self._engine_q = [
					self.framework.google,
					self.framework.duckduckgo,
					self.framework.bing,
					self.framework.millionshort,
					self.framework.startpage,
					self.framework.dogpile,
					self.framework.qwant,
					self.framework.yandex,
					self.framework.yahoo,
					self.framework.ask,
					self.framework.gigablast,
					self.framework.activesearch
				]
		else:
			self._engine_q = engine_q

		self._error_record = []


	@property
	def _get_new_errors(self):
		new_errors = self.framework._error_stack[len(self._error_record):]
		self._error_record = self.framework._error_stack
		return new_errors

	def search(self,  q, engine=None, limit=1, count=15):	
		if engine is None:
			engine = self._engine_q.pop(0)
		else:
			if engine in self._engine_q:
				self._engine_q.remove(engine)

		results = None

		while results is None:
			sig = signature(engine.__init__)
			if 'limit' in sig.parameters and 'count' in sig.parameters:
				instance = engine(q, limit=limit, count=count)
			elif 'limit' in sig.parameters:
				instance = engine(q, limit=limit)
			elif 'count' in sig.parameters:
				instance = engine(q, count=count)
			else:
				instance = engine(q)

			instance.run_crawl()

			if hasattr(instance,'results'):
				results = instance.results
			else:
				results = instance.links_with_title

			results = results if len(results)>0 else None

			if any('captcha' in x.lower() or 'missed' in x.lower() for x in self.framework._error_stack):
				self.framework._reset_error_stack()
				if len(self._engine_q) != 0:
					engine = self._engine_q.pop(0)
				else:
					self.framework.error('All Engines Exhausted')
					return 

		return results
