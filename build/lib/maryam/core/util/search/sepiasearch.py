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


class main :
    def __init__(self, q, limit=15):
        """ sepiasearch.org search
        
            q 		  : The query for search
            limit	  : The number of details min 15 if exist
        """
        self.q = q
        self.limit = limit
        self.url = 'https://sepiasearch.org/api/v1/search/videos?'
        self.params = {'search': self.q, 'boostLanguages[]': 'en', 'nsfw': 'false', 'start': 0, 'count': self.limit, 'sort': '-match'}
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self._collected_data = []
        self._result_found = 0
        
    def run_crawl(self):
        self.framework.verbose('[SEPIASEARCH] Extracting Data From API')
        response = self.framework.request(self.url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            self.framework.error('Request Fail', 'util/sepiasearch', 'run_crawl')
            return
        
        response = response.json()
        self._result_found = response['total']
        for result in response['data']:
            self._collected_data.append({
                'Title': result['name'],
                'Author': result['account']['displayName'],
                'URL': result['url'],
                'Length': self.sec_to_hours(int(result.get('duration'))),
                'Thumbnail': result['thumbnailUrl'],
                'Embeded URL': result.get('embedUrl'),
                'Published Date': result['publishedAt'],
            })

    def sec_to_hours(self, minute):
        """Convert minutes in hours"""
        if isinstance(minute, int):
            minu, sec = divmod(minute, 60)
            return "{}:{}:{} hours".format(*divmod(minu, 60), sec)
        return None

    @property
    def collected_data(self):
        return self._collected_data

    @property
    def total_result_found(self):
        return self._result_found