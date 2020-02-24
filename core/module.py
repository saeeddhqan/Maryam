#! /usr/bin/python
# -*- coding: u8 -*-
"""
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

# Based on the Recon-ng: https://github.com/lanmaster53/recon-ng

from __future__ import print_function
import os
import textwrap
# framework libs
from core import framework
from core.util import web_scrap
from core.util import reglib
from core.util import urlib
from core.util import netcraft_search
from core.util import google_engine
from core.util import metacrawler_engine
from core.util import ahmia_engine
from core.util import bing_engine
from core.util import yandex_engine
from core.util import hunter_engine
from core.util import yahoo_engine
from core.util import ask_engine
from core.util import page_parse
from core.util import search_eng
from core.util import cms_identify
from core.util import os_identify
from core.util import frameworks_identify
from core.util import lang_identify
from core.util import waf_identify
from core.util import rand_uagent

# =================================================
# MODULE CLASS
# =================================================


class BaseModule(framework.Framework):

    def __init__(self, params, query=None):
        framework.Framework.__init__(self, params)
        self.options = framework.Options()
        # register all other specified options
        if(self.meta.get("options")):
            for option in self.meta.get("options"):
                self.register_option(*option)
        self._reload = 0
        self._init_var()
        

    # ==================================================
    # OPTIONS METHODS
    # ==================================================

    def _get_source(self, params, query=None):
        if(os.path.exists(params)):
            sources = open(params).read().split()
        else:
            sources = [params]
        if(not sources):
            raise framework.FrameworkException("Source contains no input.")
        return sources

    # ==================================================
    # SHOW METHODS
    # ==================================================

    def show_source(self):
        for path in [os.path.join(x, "modules", self._modulename) + self.module_extention for x in (self.app_path, self._home)]:
            if(os.path.exists(path)):
                filename = path
        with open(filename) as f:
            content = f.readlines()
            nums = [str(x) for x in range(1, len(content)+1)]
            num_len = len(max(nums, key=len))
            for num in nums:
                print("%s|%s" % (num.rjust(num_len), content[int(num)-1]), end='')

    def show_info(self):
        self.meta["path"] = os.path.join(
            "modules", self._modulename) + self.module_extention
        print('')
        # meta info
        for item in ["name", "path", "author", "version"]:
            if self.meta.get(item):
                print("%s: %s" % (item.title().rjust(10), self.meta[item]))
        print('')
        # description
        if("description" in self.meta):
            print("Description:")
            print("%s%s" % (self.spacer, textwrap.fill(
                self.meta["description"], 100, subsequent_indent=self.spacer)))
            print('')
        # options
        print("Options:", end='')
        self.show_options()
        # comments
        if("comments" in self.meta):
            print("Comments:")
            for comment in self.meta["comments"]:
                prefix = '* '
                if(comment.startswith('\t')):
                    prefix = self.spacer+'- '
                    comment = comment[1:]
                print('%s%s' % (self.spacer, textwrap.fill(prefix+comment, 100, subsequent_indent=self.spacer)))
            print('')
 
    def show_globals(self):
        self.show_options(self._global_options)

    # ==================================================
    # UTIL METHODS
    # ==================================================

    def web_scrap(self, url,  multipage=False, cookie=None, agent=None, proxy=None, timeout=None):
        scrap_at = web_scrap.web_scrap(framework=self, url=url, cookie=cookie,
                                       agent=agent, proxy=proxy, timeout=timeout, multipage=multipage)
        return scrap_at

    def urlib(self, url):
        return urlib.urlib(url)

    def reglib(self):
        return reglib.reglib()

    def page_parse(self, page):
        return page_parse.page_parse(self, page)

    def netcraft_search(self, word, agent=None, proxy=None, timeout=None):
        search_at = netcraft_search.netcraft_search(
            framework=self, word=word, agent=agent, proxy=proxy, timeout=timeout)
        return search_at

    def google_engine(self, word, limit=5, start_page=1):
        search_at = google_engine.google_engine(
            framework=self, word=word, limit=limit, start_page=start_page)
        return search_at
        
    def google_engine(self, word, limit=5, count=100, cookie=None, agent=None, proxy=None, timeout=None):
        search_at = google_engine.google_engine(
            framework=self, word=word, limit=limit, count=count, cookie=cookie, agent=agent, proxy=proxy, timeout=timeout)
        return search_at

    def metacrawler_engine(self, word, limit=5, count=50, cookie=None, agent=None, proxy=None, timeout=None):
        search_at = metacrawler_engine.metacrawler_engine(
            framework=self, word=word, limit=limit, count=count, cookie=cookie, agent=agent, proxy=proxy, timeout=timeout)
        return search_at

    def ahmia_engine(self, word, limit=5, count=50, cookie=None, agent=None, proxy=None, timeout=None):
        search_at = ahmia_engine.ahmia_engine(
            framework=self, word=word, limit=limit, count=count, cookie=cookie, agent=agent, proxy=proxy, timeout=timeout)
        return search_at

    def bing_engine(self, word, limit=5, cookie=None, count=50, agent=None, proxy=None, timeout=None):
        search_at = bing_engine.bing_engine(
            framework=self, word=word, limit=limit, count=count, cookie=cookie, agent=agent, proxy=proxy, timeout=timeout)
        return search_at

    def yahoo_engine(self, word, limit=5, cookie=None, count=50, agent=None, proxy=None, timeout=None):
        search_at = yahoo_engine.yahoo_engine(
            framework=self, word=word, limit=limit, count=count, cookie=cookie, agent=agent, proxy=proxy, timeout=timeout)
        return search_at

    def ask_engine(self, word, limit=5, cookie=None, count=50, agent=None, proxy=None, timeout=None):
        search_at = ask_engine.ask_engine(
            framework=self, word=word, limit=limit, count=count, cookie=cookie, agent=agent, proxy=proxy, timeout=timeout)
        return search_at

    def yandex_engine(self, word, limit=5, cookie=None, count=50, agent=None, proxy=None, timeout=None):
        search_at = yandex_engine.yandex_engine(
            framework=self, word=word, limit=limit, count=count, cookie=cookie, agent=agent, proxy=proxy, timeout=timeout)
        return search_at

    def hunter_engine(self, word, key, limit=100, cookie=None, agent=None, proxy=None, timeout=None):
        search_at = hunter_engine.hunter_engine(
            framework=self, word=word, limit=limit, key=key, cookie=cookie, agent=agent, proxy=proxy, timeout=timeout)
        return search_at

    def search_eng(self, word, engines, limit=10, count=50, cookie=None, agent=None, proxy=None, timeout=None):
        _search_eng = search_eng.search_eng(
            self, word=word, limit=limit, count=count, engines=engines, cookie=cookie, agent=agent, proxy=proxy, timeout=timeout)
        return _search_eng

    def cms_identify(self, content, headers):
        _cms = cms_identify.cms_identify(self, content, headers)
        return _cms

    def os_identify(self, content, headers):
        _os = os_identify.os_identify(self, content, headers)
        return _os

    def frameworks_identify(self, content, headers):
        _frameworks = frameworks_identify.frameworks_identify(
            self, content, headers)
        return _frameworks

    def lang_identify(self, content, headers):
        _lang = lang_identify.lang_identify(self, content, headers)
        return _lang

    def waf_identify(self, content, headers):
        _waf = waf_identify.waf_identify(self, content, headers)
        return _waf

    def rand_uagent(self):
        return rand_uagent.rand_uagent(self)
        
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
            if(params):
                params = "start " + params
                self.do_spool(params)
                spool_flag = 1
            self._summary_counts = {}
            self._validate_options()
            self.module_pre()
            self.module_run()
            self.module_post()
        except KeyboardInterrupt:
            print('')
        except Exception:
            self.print_exception()
        finally:
            if(spool_flag):
                self.do_spool("stop")
    def module_pre(self):
        pass

    def module_run(self):
        pass

    def module_post(self):
        pass
