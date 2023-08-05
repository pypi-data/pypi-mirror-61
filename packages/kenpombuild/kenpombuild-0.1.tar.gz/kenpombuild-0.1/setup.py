from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name="kenpombuild",
	author="Brendan Weibel",
	author_email="me@bwhybel.com",
	description="Builds a CSV with all the kenpom rankings info",
	long_description=long_description,
	version='0.1',
	py_modules=['KenPomCSV'],
	install_requires=[
		'Click',
		'requests',
		'bs4',
		'datetime',
	],
	entry_points='''
		[console_scripts]
		kenpombuild=KenPomCSV:buildCSV
	''',
)
