# -*- coding:utf-8 -*-
from re import search, I


class os_identify:
    """docstring for os_identify"""

    def __init__(self, framework, content, headers):
        self.framework = framework
        self.content = content
        self.headers = headers
        self._os = None

    def run_crawl(self):
        for i in dir(self):
            con1 = not i.startswith("__")
            con2 = not i.endswith("__")
            con3 = i not in ("_os", "content", "headers",
                             "framework", "get_os", "run_crawl")
            if(con1 and con2 and con3):
                getattr(self, i)()

    def windows(self):
        os = ["windows", "win32"]
        for i in os:
            for header in self.headers.items():
                if search(i, header[1], I):
                    self._os = i.title()

    def bsd(self):
        for header in self.headers.items():
            if(search(r'^bsd', header[1], I)):
                self._os = "BSD"

    def ibm(self):
        os = ['IBM', 'Lotus-Domino', 'WebSEAL']
        for i in os:
            for header in self.headers.items():
                if(search(i, header[1], I)):
                    self._os = "IBM"

    def linux(self):
        os = ["linux", "ubuntu", "gentoo", "debian", "dotdeb", "centos", "redhat", "sarge", "etch",
              "lenny", "squeeze", "wheezy", "jessie", "red hat", "scientific linux"]
        for i in os:
            for header in self.headers.items():
                if(search(i, header[1], I)):
                    self._os = i.title()

    def mac(self):
        for header in self.headers.items():
            if search(r'^mac|^macos', header[1], I):
                self._os = "MacOS"

    def solaris(self):
        os = ["solaris", "sunos", "opensolaris", "sparc64", "sparc"]
        for o in os:
            for header in self.headers.items():
                if(search(o, header[1], I)):
                    self._os = o.title()

    def unix(self):
        for header in self.headers.items():
            if(search(r'^unix', header[1], I)):
                self._os = "Unix"

    @property
    def get_os(self):
        return self._os
