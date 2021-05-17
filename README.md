[![Build Status](https://travis-ci.com/saeeddhqan/maryam.svg?branch=master)](https://travis-ci.com/saeeddhqan/maryam)
![Version 2.2.6](https://img.shields.io/badge/Version-2.2.6-green.svg)
![GPLv3 License](https://img.shields.io/badge/License-GPLv3-green.svg)
![Python 3.8.x](https://img.shields.io/badge/Python-3.8.x-green.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/40d81c48b3444ee78ffc6c5c8639134c)](https://www.codacy.com/manual/saeeddhqan/Maryam?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=saeeddhqan/Maryam&amp;utm_campaign=Badge_Grade)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4577/badge)](https://bestpractices.coreinfrastructure.org/projects/4577)

# OWASP Maryam

OWASP Maryam is a modular/optional open source framework based on OSINT and data gathering. Maryam is written in Python programming language and it’s designed
to provide a powerful environment to harvest data from open sources and search engines and collect data quickly and thoroughly.

# Install

### Supported OS
 - Linux
 - FreeBSD
 - OSX

```bash
$ pip install maryam
```

## Tips

```bash
# Using dns_search. --max means all of resources. --api shows the results as json.
# .. -t means use multi-threading.
maryam -e dns_search -d ibm.com -t 5 --max --api --form 
# Using youtube. -q means query
maryam -e youtube -q "<QUERY>"
maryam -e google -q "<QUERY>"
maryam -e dnsbrute -d domain.tld
# Show the framework modules
maryam -e show modules
# Set framework options. It'll save in the workspace.
maryam -e set proxy ..
maryam -e set agent ..
maryam -e set timeout ..
# Run web API
maryam -e web api 127.0.0.1 1313
```

## Updates
**Last Updates**

 - Speed up the core
 - Add setup.py and change arch
 - Web API: web command
 - Error stack and a better performance for dev
 - Update google and yahoo: new format
 - Add API interface


## Contribution

Contributes are welcome! Here is a start guide: [Development Guide](https://github.com/saeeddhqan/maryam/wiki/Development-Guide)
You can add a new search engine to the util classes or use current search engines to write a new module.
The best help to write a new module is by checking the current modules.

## Roadmap

 - Write a complete metacrawler engine based on OSINT by using the current search engines
 - Add clustering algorithms
 - Web User Interface

## links
### [OWASP](https://owasp.org/www-project-maryam/)
### [Wiki](https://github.com/saeeddhqan/maryam/wiki)
### [Install](https://github.com/saeeddhqan/maryam/wiki#install)
### [Modules Guide](https://github.com/saeeddhqan/maryam/wiki/modules)
### [Development Guide](https://github.com/saeeddhqan/maryam/wiki/Development-Guide)

To report bugs, requests, or any other issues please [create an issue](https://github.com/saeeddhqan/maryam/issues).
