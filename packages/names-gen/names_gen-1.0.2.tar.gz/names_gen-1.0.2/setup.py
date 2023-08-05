from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
	version = f.read()

setup(
	name = 'names_gen',
	version = version,
	description = "Generate random names with lenght",
	long_description = long_description,
	long_description_content_type = 'text/markdown',
    url="https://github.com/treyhunner/names",
	author = 'Michal Kopys',
	author_email = 'mikopys@gmail.com',
    include_package_data=True,
	keywords = 'random names',
	packages = find_packages(),
    scripts = ['gen_names/gen_names.py'],
    install_requires = ['names']
)
