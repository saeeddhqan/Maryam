try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



setup(
    name='OWASP Maryam',
    version='2.1.5',
    @version=open('.config/version.txt').read().split(),
    url='https://github.com/saeeddhqan/Maryam',
    classifiers = [...],
    description='OWASP Maryam is a modular/optional open source framework based on OSINT and data gathering. harvest data from  OSINT/search engines',
    @description=open('.config/description.txt').read().split(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #keywords=open('.config/keywords.txt').read().split(' '),
    install_reqs = parse_requirements('requirements')
    py_modules=['module1s','core' ,'data'],
    #scripts=['scripts/script1','scripts/script2']
)