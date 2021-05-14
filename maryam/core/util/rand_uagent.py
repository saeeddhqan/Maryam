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

from random import choice

class main:

	agents = ['Googlebot/2.1 ( http://www.googlebot.com/bot.html)',
			'Debian APT-HTTP/1.3 (0.8.10.3)',
			'Chromium/9.0.595.0 Chrome/9.0.595.0 Safari/534.13',
			'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Ubuntu/10.04'
			'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
			'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.5) Gecko/20060719 Firefox/1.5.0.5',
			'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
			'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.2; WOW64; .NET CLR 2.0.50727)',
			'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
			'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
			'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',
			'msnbot/1.1 (+http://search.msn.com/msnbot.htm)',
			'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
			'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ;',
			'http://help.yahoo.com/help/us/shop/merchant/)',
			'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
			'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-gb) AppleWebKit/528.4+ (KHTML, like Gecko) Version/4.0dp1 Safari/526.11.2',
			'Mozilla/4.0 (compatible; MSIE 5.22; Mac_PowerPC)',
			'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; pl) Opera 8.54',
			'Mozilla/5.0 (Windows NT 5.1; U; en) Opera 8.51',
			'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/5.0 Opera 11.11',
			'Opera/8.01 (Macintosh; U; PPC Mac OS; en)',
			'Opera/8.01 (Windows NT 5.1; U; de)',
			'Opera/9.80 (Windows NT 5.2; U; en) Presto/2.6.30 Version/10.63',
			'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; ko; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2',
			'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; he; rv:1.9.1b4pre) Gecko/20100405 Firefox/3.6.3plugin1',
			'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.12pre) Gecko/20080122 Firefox/2.0.0.12pre',
			'Mozilla/5.0 (X11; FreeBSD i686) Firefox/3.6']

	lynx = ['Lynx/2.8.5rel.1 libwww-FM/2.15FC SSL-MM/1.4.1c OpenSSL/0.9.7e-dev',
					'Lynx/2.8.5dev.16 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.7a',
					'Lynx/2.8.9dev.8 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/3.4.9',
					'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.0.16',
					'Lynx/2.8.4rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/0.8.6',
					'Lynx/2.8.4rel.1 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.6b',
					'Lynx/2.8.8pre.4 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.12.23',
					'Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1',
					'Lynx/2.8.7dev.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8d',
					'Lynx/2.8.9dev.11 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/3.5.6']

	phone = ['WeatherReport/1.0.2 CFNetwork/485.13.9 Darwin/11.0.0',
					'WeatherReport/1.2.2 CFNetwork/485.13.9 Darwin/11.0.0',
					'WeatherReport/1.2.2 CFNetwork/485.12.7 Darwin/10.4.0',
					'WeatherReport/1.2.1 CFNetwork/485.12.7 Darwin/10.4.0',
					'WeatherReport/1.2.0 CFNetwork/485.12.7 Darwin/10.4.0',
					'WeatherReport/1.2.1 CFNetwork/485.13.9 Darwin/11.0.0',
					'WeatherReport/1.2.2 CFNetwork/485.13.8 Darwin/11.0.0'
					'WeatherReport/1.2.2 CFNetwork/467.12 Darwin/10.3.1',
					'WeatherReport/1.0.2 CFNetwork/485.12.7 Darwin/10.4.0',
					'WeatherReport/1.2.1 CFNetwork/467.12 Darwin/10.3.1']

	server = ['Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)',
					'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
					'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
					'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
					'YahooMailProxy; https://help.yahoo.com/kb/yahoo-mail-proxy-SLN28749.html',
					'Mozilla/5.0 (compatible; MJ12bot/v1.4.5; http://www.majestic12.co.uk/bot.php?+)',
					'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
					'Mozilla/5.0 (compatible; MegaIndex.ru/2.0; +http://megaindex.com/crawler)',
					'Mozilla/5.0 (compatible; AhrefsBot/5.2; +http://ahrefs.com/robot/)',
					'Apache/2.4.7 (Unix) OpenSSL/1.0.1e PHP/5.4.22 mod_perl/2.0.8-dev Perl/v5.16.3 (internal dummy connection)']

	@property
	def get(self):
		return choice(self.agents)
