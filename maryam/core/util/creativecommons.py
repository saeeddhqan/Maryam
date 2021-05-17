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
        """ search.creativecommons.org search
        
            q 		  : The query for search
            limit	  : The number of details min 15 if exist
        """
        self.q = q
        self.limit = limit
        self.url = 'https://api.creativecommons.engineering/v1/images'
        self.params = {'q': self.q}
        self._collected_data = []
        self._result_found = 0
        
    def run_crawl(self):
        self.framework.verbose('[creativecommons] Extracting Data From API')
        
        # first page
        success, response = self.send_request(params=self.params)
        if not success: 
            return

        self._result_found = response['result_count']
        self.extract_data(response['results']) 
        total_pages = response['page_count']
        page_size = response['page_size']

        # all next pages
        if total_pages > 1 and len(self._collected_data) < self.limit:
            self.params['shouldPersistImages'] = 'true' 
            for i in range(self.limit//page_size + 1):
                self.framework.verbose(f"[creativecommons] Extracting Data From API request-{i+1}")
                success, response = self.send_request(params={**self.params, 'page': i+1})
                if not success: 
                    continue
                self.extract_data(response['results'])
        
    def send_request(self, params):
        try:
            response = self.framework.request(self.url, params=params)
        except:
            self.framework.error('Request Fail', 'util/creativecommons', 'send_request')
        else:
            if response.status_code != 200:
                self.framework.error('Request Fail - Invalid request', 'util/creativecommons', 'send_request')
                return False, None
            return True, response.json()

    def extract_data(self, data):
        for result in data:
            self._collected_data.append({
                'Title': result['title'],
                'Creator': result['creator'],
                'Creator_url': result['creator_url'],
                'Image-URL': result['url'],
            })

    @property
    def collected_data(self):
        return self._collected_data

    @property
    def total_result_found(self):
        return self._result_found