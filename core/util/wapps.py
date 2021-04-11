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
import re
import os

class main:

	def __init__(self, q, page, headers):
		""" Web application fingerprint for detect apps. like wappalizer
			
			q 		  : Domain name
			page	  : Web page
			headers	  : Web headers
		"""
		self.framework = main.framework
		self.q = q
		self.page = page
		self.headers = headers
		# Wapps json file
		self.wfile = os.path.join(self.framework.data_path, 'wapps.json')

	def _req_parse(self):
		parser = self.framework.page_parse(self.page)

		# tree = fromstring(self.page)
		# Get Script[src] links
		self.scripts = parser.get_jsfiles
		# Get meta tags
		self.meta = {}
		meta = parser.get_metatags
		for attr in meta:
			if 'name' in attr and 'content' in attr:
				self.meta[attr['name']] = attr['content']

	def _has_app(self, app):
		# Search the easiest things first and save the full-text search of the
		# HTML for last

		for regexes in app['url']:
			for regex in regexes:
				if regex.search(self.q):
					return True
				
		# Headers
		for name, regexes in app['headers'].items():
			if name in self.headers:
				content = self.headers[name]
				# print(regexes)
				for regex in regexes:
					if regex.search(content):
						return True

		# Javascript links
		for regexes in app['scripts']:
			if regexes:
				for regex in regexes:
					for script in self.scripts:
						search = regex.search(script)
						if search:
							return search.group()

		# Meta tags
		for name, regex in app['meta'].items():
			if name in self.meta:
				content = self.meta[name]
				if regex.search(content):
					return True

		# Html search
		for regexes in app['html']:
			if regexes:
				for regex in regexes:
					if regex.search(self.page):
						return True

	def _init_pattern(self, patterns):
		outcome = []
		if isinstance(patterns, list):
			for patt in patterns:
				regex, _, rest = patt.partition('\\;')
				try:
					outcome.append(re.compile(regex, re.I))
				except re.error as e:
					outcome.append(re.compile(r'(?!x)x'))
			return outcome
		else:
			try:
				return [re.compile(patterns, re.I)]
			except re.error as e:
				return [re.compile(r'(?!x)x')]

	def _init_wfile(self):
		with open(self.wfile) as wf:
			jload = json.loads(wf.read())
		self.apps = jload['technologies']
		self.categories = jload['categories']
		"""
		Normalize app data, preparing it for the detection phase.
		"""
		for name, app in self.apps.items():
			self._init_app(app)
	
	def _init_app(self, app):
		# Ensure these keys' values are lists
		for key in ['url', 'html', 'scripts', 'implies']:
			try:
				value = app[key]
			except KeyError:
				app[key] = []
			else:
				if not isinstance(value, list):
					app[key] = [value]

		# Ensure these keys exist
		for key in ['headers', 'meta']:
			try:
				value = app[key]
			except KeyError:
				app[key] = {}

		# Ensure the 'meta' key is a dict
		obj = app['meta']
		if not isinstance(obj, dict):
			app['meta'] = {'generator': obj}

		# Ensure keys are lowercase
		for key in ['headers', 'meta']:
			obj = app[key]
			app[key] = {k.lower(): v for k, v in obj.items()}

		"""
		Strip out key:value pairs from the pattern and compile the regular
		expression.
		"""
		for key in ['url', 'html', 'scripts']:
			app[key] = [self._init_pattern(pattern) for pattern in app[key]]

		for key in ['headers', 'meta']:
			obj = app[key]
			for name, pattern in obj.items():
				obj[name] = self._init_pattern(obj[name])

	def _get_implied_apps(self, detected_apps):
		def __get_implied_apps(apps):
			_implied_apps = set()
			for app in apps:
				try:
					_implied_apps.update(set(self.apps[app]['implies']))
				except KeyError:
					pass
			return _implied_apps

		implied_apps = __get_implied_apps(detected_apps)
		all_implied_apps = set()

		# Descend recursively until we've found all implied apps
		while not all_implied_apps.issuperset(implied_apps):
			all_implied_apps.update(implied_apps)
			implied_apps = __get_implied_apps(all_implied_apps)

		return all_implied_apps

	def get_categories(self, app_name):
		"""
		Returns a list of the categories for an app name.
		"""
		cat_nums = self.apps.get(app_name, {}).get('cats', [])
		cat_names = [self.categories.get(f'{cat_num}', '')
					 for cat_num in cat_nums]

		return cat_names

	def analyze(self):

		detected_apps = set()
		for app_name, app in self.apps.items():
			"""
			Determine whether the web page matches the app signature.
			"""
			has_app = self._has_app(app)
			if has_app:
				detected_apps.add(app_name)

		"""
		Get the set of apps implied by detected_apps
		"""
		detected_apps |= self._get_implied_apps(detected_apps)
		return detected_apps

	def run_crawl(self):
		self._init_wfile()
		self._req_parse()
		app_list = list(self.analyze())
		resp = {}
		for app in app_list:
			app = re.split(r"\\?;", app)[0]
			resp[app] = self.apps[app].get('website')
 
		return resp
