from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ohmgroups/__init__.py
from ohmgroups import __version__ as version

setup(
	name="ohmgroups",
	version=version,
	description="Wind Mill",
	author="thirvusoft",
	author_email="thirvusoft@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
