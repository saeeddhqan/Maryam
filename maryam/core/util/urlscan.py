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

class main:
    def __init__(self, u, limit=100):
        """ urlscan.io scanner

        u       : The url for scanning
        limit   : Number of pages
        """
        self.framework = main.framework
        self.url = u
        self.limit = limit
        self._ips = []
        self._domains = []
        self.urlscan_api = f"https://urlscan.io/api/v1/search/?q=domain:{self.url}"

    def run_crawl(self):
        domains = []
        self.framework.verbose('[URLSCAN] Searching in urlscan.io...')
        try:
            req = self.framework.request(self.urlscan_api)
            result_json = req.json()
        except:
            self.framework.error('[URLSCAN] Connection Error')
            return
        else:
            if not result_json['total']:
                self.framework.verbose('[URLSCAN] Not yet in our database.')
                return
            elif 'results' not in result_json:
                self.framework.error(f"failed with an error: {result_json['description']}", 'util/urlscan', 'run_crawl')
                return
            else:
                for results in result_json['results']:
                    domains.append(results['task']['domain'])
                    domains.append(results['page']['domain'])
                for i in range(len(domains)):
                    if self.url in domains[i]:
                        self._domains.append(domains[i])

    @property
    def dns(self):
        return self._domains

    @property
    def get_ips(self):
        return self._ips