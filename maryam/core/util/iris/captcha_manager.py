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
	def __init__(self, engine=None, engine_q=None):
		self.framework = main.framework

		if engine_q is None:
			self._engine_q = [
					self.framework.google,
					self.framework.startpage,
					self.framework.duckduckgo,
					self.framework.bing,
					self.framework.dogpile,
					self.framework.millionshort,
					self.framework.qwant,
					self.framework.yandex,
					self.framework.yahoo,
					self.framework.ask,
					self.framework.gigablast,
					self.framework.activesearch
				]
		else:
			self._engine_q = engine_q

		if engine is None:
			self._current_engine = self._engine_q.pop(0)
		else:
			self._current_engine = engine
			if self._current_engine in self._engine_q:
				self._engine_q.remove(self._current_engine)

		self._error_record = self.framework._error_stack


	@property
	def _get_new_errors(self):
		new_errors = self.framework._error_stack[len(self._error_record):]
		self._error_record = self.framework._error_stack
		return new_errors

	def search(self, q, limit=1, count=15):
		results = None

		while results is None:
			if 'CaptchaError' in self._get_new_errors or \
					any('Missed' in x for x in self._get_new_errors):
				if len(self._engine_q) != 0:
					self._current_engine = self._engine_q.pop(0)
				else:
					self.framework.error('All Engines Exhausted')
					return 

			sig = signature(self._current_engine.__init__)
			if 'limit' in sig.parameters and 'count' in sig.parameters:
				instance = self._current_engine(q, limit=limit, count=count)
			else:
				instance = self._current_engine(q, limit)
			instance.run_crawl()

			results = instance.results if len(instance.results) > 0 else None

		return results
