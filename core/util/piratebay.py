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

import re
import urllib.parse
import html

class main:

        def __init__(self, q, limit=15):
                """ piratebay search engine

                        q         : query for search
                        limit     : maximum result count
                """
                self.framework = main.framework
                self.q = q
                self.max = limit
                self._rawhtml = ''
                self._torrents = []
                self._magnets = []
                self._rows = []
                self._links_with_data = []

        def run_crawl(self):
                self.q = urllib.parse.quote(self.q)
                url = f'https://tpb.party/search/{self.q}'
                self.framework.verbose('Searching piratebay...')
                try:
                        req = self.framework.request(url=url)
                except:
                        self.framework.error('[PIRATEBAY] ConnectionError')
                        self.framework.error('Piratebay is missed!')
                        self.framework.error('Try again after a few seconds!')
                        return
                self._rawhtml = req.text
                self._torrents = list(re.findall('<tr>(.*?)</tr>', 
                        self._rawhtml, 
                        flags=re.DOTALL))

        @property
        def raw(self):
                return self._rawhtml

        @property
        def links_with_data(self):
                findtitle = lambda x: re.findall('Details for (.*?)">', x, flags=re.DOTALL)
                magnet_regex = r'<a href="(magnet:.*?)" title="Download this torrent using magnet">'
                findmagnet = lambda x: re.findall(magnet_regex, x)
                finduploader = lambda x: re.findall('title="Browse (.*?)"', x)
                finddatesize = lambda x: re.findall('Uploaded .*?, ULed by', x)
                seedandleech = lambda x: re.findall( '<td align="right">(.*?)</td>', x)
                

                limitcount = 0
                for torrent in self._torrents:
                        limitcount+=1
                        if limitcount>self.max:
                            break

                        title = findtitle(torrent)
                        magnet = findmagnet(torrent)
                        uploader = finduploader(torrent)
                        date = finddatesize(torrent)
                        seedleechcount = seedandleech(torrent)

                        if len(title)==len(magnet)==len(uploader)==len(date)==1\
                        and len(seedleechcount)==2:
                                self._links_with_data.append({
                                        'title': html.unescape(title[0]),
                                        'date': html.unescape(date[0]),
                                        'uploader': uploader[0],
                                        'magnet' : magnet[0],
                                        'seeders': seedleechcount[0],
                                        'leechers': seedleechcount[1]
                                        })

                return self._links_with_data
