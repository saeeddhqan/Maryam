"""
OWASP Maryam!

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSEdocs.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# Based on the Recon-ng core(https://github.com/lanmaster53/recon-ng)

from __future__ import print_function
import os
import textwrap
# framework libs
from core import framework
from core.util import ahmia
from core.util import ask
from core.util import baidu
from core.util import bing
from core.util import cms_identify
from core.util import crt
from core.util import carrot2
from core.util import exalead
from core.util import google
from core.util import hunter
from core.util import keywords
from core.util import lang_identify
from core.util import metacrawler
from core.util import millionshort
from core.util import netcraft
from core.util import os_identify
from core.util import onionland
from core.util import page_parse
from core.util import qwant
from core.util import rand_uagent
from core.util import reglib
from core.util import searchencrypt
from core.util import startpage
from core.util import urlib
from core.util import virustotal
from core.util import waf_identify
from core.util import web_scrap
from core.util import wapps
from core.util import yahoo
from core.util import yandex
from core.util import yippy

# =================================================
# MODULE CLASS
# =================================================


class BaseModule(framework.Framework):

	def __init__(self, params, query=None):
		framework.Framework.__init__(self, params)
		self.options = framework.Options()
		# register all other specified options
		if self.meta.get('options'):
			for option in self.meta.get('options'):
				name, val, req, desc = option[:4]
				self.register_option(name, val, req, desc)
		self._reload = 0

	# ==================================================
	# OPTIONS METHODS
	# ==================================================

	def _get_source(self, params, query=None):
		if os.path.exists(params):
			sources = open(params).read().split()
		else:
			sources = [params]
		if not sources:
			raise framework.FrameworkException('Source contains no input.')
		return sources

	# ==================================================
	# SHOW METHODS
	# ==================================================

	def show_source(self):
		for path in [os.path.join(x, 'modules', self._modulename) + self.module_extention for x in (self.app_path, self._home)]:
			if os.path.exists(path):
				filename = path
		with open(filename) as f:
			content = f.readlines()
			nums = [str(x) for x in range(1, len(content)+1)]
			num_len = len(max(nums, key=len))
			for num in nums:
				print(f'{num.rjust(num_len)}|{content[int(num)-1]}', end='')

	def show_info(self):
		self.meta['path'] = os.path.join(\
			'modules', self._modulename) + self.module_ext
		print('')
		# meta info
		for item in ('name', 'path', 'author', 'version'):
			if self.meta.get(item):
				print(f'{item.title().rjust(10)}: {self.meta[item]}')
		print('')
		# description
		if 'description' in self.meta:
			print('Description:')
			print(f"{self.spacer}{textwrap.fill(self.meta['description'], 100, subsequent_indent=self.spacer)}")
		# options
		print('Options:', end='')
		self.show_options()
		# comments
		if 'comments' in self.meta:
			print('Comments:')
			for comment in self.meta['comments']:
				prefix = '* '
				if comment.startswith('\t'):
					prefix = self.spacer + '- '
					comment = comment[1:]
				print(f"{self.spacer}{textwrap.fill(prefix+comment, 100, subsequent_indent=self.spacer)}")
			print('')

		# Show Sources
		if 'sources' in self.meta:
			print('\nSources:\n\t' + '\n\t'.join(self.meta.get('sources')))

		# Show Examples
		if "examples" in self.meta:
			print('\nExamples:\n\t' + '\n\t'.join(self.meta.get('examples')))

	def show_globals(self):
		self.show_options(self._global_options)

	# ==================================================
	# UTIL METHODS
	# ==================================================

	def ahmia(self, q):
		search = ahmia.main(self, q)
		return search

	def ask(self, q, limit=5):
		search = ask.main(self, q, limit)
		return search

	def baidu(self, q, limit=3):
		search = baidu.main(self, q, limit)
		return search

	def bing(self, q, limit=1, count=10):
		search = bing.main(self, q, limit, count)
		return search

	def cms_identify(self, content, headers):
		_cms = cms_identify.main(content, headers)
		return _cms

	def crt(self, q):
		search = crt.main(self, q)
		return search

	def carrot2(self, q):
		search = carrot2.main(self, q)
		return search

	def exalead(self, q, limit=3):
		search = exalead.main(self, q, limit)
		return search

	def google(self, q, limit=1, count=10):
		search = google.main(self, q, limit, count)
		return search

	def hunter(self, q, key, limit=100):
		search = hunter.main(self, q, key, limit)
		return search

	def keywords(self, q):
		search = keywords.main(self, q)
		return search

	def lang_identify(self, content, headers):
		search = lang_identify.main(content, headers)
		return search

	def metacrawler(self, q, limit=1):
		search = metacrawler.main(self, q, limit)
		return search

	def millionshort(self, q, limit=2):
		search = millionshort.main(self, q, limit)
		return search

	def netcraft(self, q, limit=4):
		search = netcraft.main(self, q, limit)
		return search

	def os_identify(self, content, headers):
		search = os_identify.main(content, headers)
		return search

	def onionland(self, q, limit=5):
		search = onionland.main(self, q, limit)
		return search

	def page_parse(self, page):
		return page_parse.main(self, page)

	def qwant(self, q, limit=2):
		search = qwant.main(self, q, limit)
		return search

	def rand_uagent(self):
		return rand_uagent.main

	def reglib(self, page=None):
		return reglib.main(page)

	def urlib(self, url):
		return urlib.main(url)

	def virustotal(self, q, limit):
		search = virustotal.main(self, q, limit)
		return search

	def wapps(self, q, page, headers):
		search = wapps.main(self, q, page, headers)
		return search

	def waf_identify(self, req):
		_waf = waf_identify.main(req)
		return _waf

	def web_scrap(self, url, debug=False, limit=5, thread=1):
		search = web_scrap.main(self, url, debug, limit, thread)
		return search

	def searchencrypt(self, q, count=50):
		search = searchencrypt.main(self, q, count)
		return search

	def startpage(self, q, limit):
		search = startpage.main(self, q, limit)
		return search


	def yahoo(self, q, limit=2, count=50):
		search = yahoo.main(self, q, limit, count)
		return search

	def yandex(self, q, limit=2, count=50):
		search = yandex.main(self, q, limit, count)
		return search

	def yippy(self, q):
		search = yippy.main(self, q)
		return search

	# ==================================================
	# COMMAND METHODS
	# ==================================================

	def do_reload(self, params):
		'''Reloads the current module'''
		self._reload = 1
		return True

	def do_run(self, params):
		'''Runs the module'''
		spool_flag = 0
		try:
			if params:
				params = f'start {params}'
				self.do_spool(params)
				spool_flag = 1
			self._validate_options()
			self.module_pre()
			self.module_run()
			self.module_post()
		except KeyboardInterrupt:
			print('')
		except Exception:
			self.print_exception()
		finally:
			if spool_flag:
				self.do_spool('stop')
	def module_pre(self):
		pass

	def module_run(self):
		pass

	def module_post(self):
		pass
