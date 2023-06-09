#!/usr/bin/env python3
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
import subprocess
from setuptools import setup, find_packages

# Check if Node.js and npm are installed
try:
    subprocess.run(["node", "-v"], check=True)
    subprocess.run(["npm", "-v"], check=True)
except FileNotFoundError:
    print("Node.js or npm is not installed. Installing Node.js...")
    subprocess.run(
        ["sudo", "apt", "install", "nodejs", "-y"]
    )  # Modify the package manager command based on your Linux distribution
    print("Node.js installed successfully.")

# Rest of the setup() function remains the same

setup(
    name="maryam",
    version="2.5.1-3",
    url="https://github.com/saeeddhqan/Maryam",
    author="Saeed Dehqan",
    author_email="saeed.dehghan@owasp.org",
    packages=find_packages(),
    include_package_data=True,
    package_data={"maryam": ["data/*"]},
    license="GPL-V3",
    description="OWASP Maryam is a modular/optional open-source framework based on OSINT and data gathering.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=["OWASP", "OSINT", "search-engine", "social-networks", "Maryam"],
    scripts=["bin/maryam"],
    install_requires=[
        "requests",
        "cloudscraper",
        "bs4",
        "lxml",
        "flask",
        "vaderSentiment",
        "plotly",
        "nltk",
        "matplotlib",
        "pandas",
        "wordcloud",
        "numpy",
        "dask",
        "scikit-learn",
        "scipy",
        "umap",
        "bertopic",
        "sentence_transformers",
        "gensim",
        "top2vec",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
)

# Check if the current path exists and contains the /bin/local/web folder
try:
    subprocess.run(["ls", "./maryam/core/web/webSearchInterface"], check=True)
except FileNotFoundError:
    print(
        "The specified path does not exist or does not contain the /bin/local/web folder."
    )
    exit(1)

# Install npm packages in the specified path
print("Installing npm packages...")
subprocess.run(["npm", "install"], cwd="./maryam/core/web/webSearchInterface")
print("npm packages installed successfully.")

