export const module_meta: { [modulename: string]: any}= {
  'crawl_pages':{
    'name' : 'Regex Web Search',
    'author' : 'Saeed',
    'version' : '0.6',
    'description' : 'Search to find keywords, emails, usernames, errors, meta tags and regex on the page/pages.',
    'options' : [
      ['domain', null, true, 'Domain string', '-d', 'store', 'string'],
      ['regex', null, true, 'Regex or string for search in the pages', '-r', 'store', 'string'],
      ['more', false, false, 'Extract more information from the pages', '--more', 'store_true', 'boolean'],
      ['limit', 1, false, 'Scraper depth level[default=1]', '-l', 'store', 'number'],
      ['debug', false, false, 'debug the scraper', '--debug', 'store_true', 'boolean'],
      ['thread', 1, false, 'The number of links that open per round', '-t', 'store', 'number'],
    ],
    'examples': ['crawl_pages -d <DOMAIN> -r "https?://[A-z0-9\./]+"\
      --output', 'crawl_pages -d <DOMAIN> --limit 2 --more']
  }
}