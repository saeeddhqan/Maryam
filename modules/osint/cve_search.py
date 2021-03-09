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

from concurrent.futures import thread
from core.module import BaseModule
import re
import concurrent.futures

class Module(BaseModule):

    meta = {
        'name': 'Common Vulnerabilities and Exposures Searcher',
        'author': 'Dimitrios Papageorgiou',
        'version': '0.1',
        'description': 'Search in open-sources to find CVEs.',
        'sources': ('mitre'),
        'options': (
                ('query', None,
                 True, 'Query string(bug name, app name, etc)', '-q', 'store'),
                ('sources', 'mitre', False,
                 'DB source to search. e.g mitre,...(default=mitre)', '-s', 'store'),
                ('thread', 2, False,
                 'The number of engine that run per round(default=2)', '-t', 'store'),
                ('output', False, False, 'Save output to  workspace',
                 '--output', 'store_true'),
        ),
        'examples': ('cve_search -q sql -s mitre --output')
    }

    names = []
    links = []
    descriptions = []

    def clear(self):
        self.names = []
        self.links = []
        self.descriptions = []

    def mitre(self, q):
        self.verbose('[MITRE] Searching in mitre...')
        try:
            req = self.request(
                f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={q}")
        except Exception as e:
            self.error('Mitre is missed!')
        else:
            self.names.extend(re.findall(
                r'<a href=".*?">(CVE-.*?)</a>', req.text))
            hrefs = re.findall(
                r'<a href="(/cgi-bin/cvename.cgi\?name=.*?)">', req.text)
            self.links.extend(
                list(map(lambda x: f"https://cve.mitre.org/{x}", hrefs)))
            self.descriptions.extend(re.findall(
                r'<td valign="top">(.*?)<\/td>', req.text.replace('\n', '')))

    def thread(self, function, thread_count, sources, q):
        threadpool = concurrent.futures.ThreadPoolExecutor(
            max_workers=thread_count)
        futures = (threadpool.submit(function, source, q)
                   for source in sources if source in self.meta['sources'])
        for _ in concurrent.futures.as_completed(futures):
            pass

    def search(self, source, q):
        getattr(self, source)(q)

    def module_run(self):
        self.clear()
        q = self.options['query']
        sources = self.options['sources'].split(',')
        thread_count = self.options['thread']

        self.thread(self.search, thread_count, sources, q)

        if self.names == []:
            self.output('No CVE found', 'O')

        for i in range(len(self.names)):
            self.output(self.names[i], 'G')
            self.output(self.links[i], 'R')
            self.output(f"{self.descriptions[i]}\n")

        self.save_gather({'names': self.names, 'links': self.links,
                          'descriptions': self.descriptions}, 'osint/cve_search',
                         q, output=self.options.get('output'))
