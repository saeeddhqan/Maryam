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

from core.module import BaseModule
import re


class Module(BaseModule):
    meta = {
        'name': 'Reddit Search',
        'author': 'Kunal Khandelwal',
        'version': '0.1',
        'description': 'Search your query in the Reddit and show the results.',
        'sources': ('google', 'yahoo', 'bing'),
        'options': (
            ('query', None, True, 'Query string', '-q', 'store'),
            ('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
            ('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store'),
            ('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
            ('output', False, False, 'Save output to workspace', '--output', 'store_true'),
        ),
        'examples': ('reddit -q <QUERY> -l 15 --output',)
    }

    def module_run(self):
        query = self.options['query']
        limit = self.options['limit']
        count = self.options['count']
        engine = self.options['engine'].split(',')
        google_q = f"site:www.reddit.com inurl:{query}"
        q = f"site:www.reddit.com {query}"
        usernames = []

        run = self.google(q, limit, count)
        run.run_crawl()
        links = run.links

        if 'bing' in engine:
            run = self.bing(q, limit, count)
            run.run_crawl()
            for item in run.links_with_title:
                link, title = item
                links.append(link)

        if 'yahoo' in engine:
            run = self.yahoo(q, limit, count)
            run.run_crawl()
            links += run.links

        links = list(set(links))
        if links is None:
            self.output('Without result')
        else:
            links = [link for link in links if re.search('https?://(www.)?reddit.com/', link)]
            self.alert('Usernames')
            for link in links:
                if re.search(r"https?://(www.)?reddit.com/user/", link):
                    link = re.sub('https?://(www.)?reddit.com/user/', '', link)
                    if re.search(r'^[\w\d_\-\/]+$', link):
                        link = link.rsplit('/')
                        if link[0] not in usernames:
                            usernames.append(link[0])
                            self.output(f"\t{link[0]}", 'G')

            self.alert('Posts')
            for link in links:
                if re.search(r"https?://(www.)?reddit.com/r/", link):
                    post_url = re.sub('https?://(www.)?reddit.com/r/', '', link)
                    post_url = post_url.rsplit('/')
                    subreddit = post_url[0]
                    try:
                        post = post_url[3]
                    except Exception as e:
                        continue

                    post = post.replace('_', ' ')
                    post = self.urlib(post).unquote
                    self.output(f'\t{post.title()} --> r/{subreddit} \n\t\t{link}')

        self.save_gather({'links': links, 'usernames': usernames},
                         'search/reddit', query, output=self.options.get('output'))
