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

meta = {
    'name': 'Spotify Search',
    'author': 'Kunal Khandelwal',
    'version': '0.1',
    'description': 'Search artists, albums, playlist and users on spotify',
    'sources': ('google', 'yahoo', 'bing','duckduckgo', 'metacrawler', 'millionshort', 'carrot2', 'qwant'),
    'options': (
        ('query', None, True, 'Query string', '-q', 'store', str),
        ('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
        ('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
        ('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store', str),
        ('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
    ),
    'examples': ('spotify -q <QUERY> -l 15 --output',)
}

LINKS = []

def search(self, name, q, q_formats, limit, count):
    global LINKS
    engine = getattr(self, name)
    q = q_formats[f"{name}_q"] if f"{name}_q" in q_formats else q_formats['default_q']
    varnames = engine.__init__.__code__.co_varnames
    if 'limit' in varnames and 'count' in varnames:
        attr = engine(q, limit, count)
    elif 'limit' in varnames:
        attr = engine(q, limit)
    else:
        attr = engine(q)

    attr.run_crawl()
    LINKS += attr.links

def module_api(self):
    global LINKS
    query = self.options['query']
    limit = self.options['limit']
    count = self.options['count']
    engines = self.options['engine'].split(',')
    output = {'user': [], 'artist': [], 'playlist': [], 'album': []}
    q_formats = {
        'default_q': f"site:open.spotify.com {query}",
        'millionshort_q': f'site:open.spotify.com "{query}"',
        'qwant_q': f'site:open.spotify.com {query}'
    }

    self.thread(search, self.options['thread'], engines, query, q_formats, limit, count, meta['sources'])

    
    LINKS = list(self.reglib().filter(r"https?://(open\.)?spotify\.com/", list(set(LINKS))))

    for link in self.reglib().filter(r"https?://(open\.)?spotify\.com/user/", LINKS):
        if '/playlist/' not in link:
            output['user'].append(link)
        else:
            output['playlist'].append(link)
    output['artist'] = list(self.reglib().filter(r"https?://(open\.)?spotify\.com/artist/", LINKS))
    output['album'] = list(self.reglib().filter(r"https?://(open\.)?spotify\.com/album/", LINKS))
    output['playlist'] += list(self.reglib().filter(r"https?://(open\.)?spotify\.com/playlist/", LINKS))

    self.save_gather(output, 'search/spotify', query, output=self.options.get('output'))
    return output


def module_run(self):
    self.alert_results(module_api(self))
