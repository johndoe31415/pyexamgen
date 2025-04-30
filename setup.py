import setuptools

with open("README.md") as f:
	long_description = f.read()

setuptools.setup(
	name = "pyexamgen",
	packages = setuptools.find_packages(),
	version = "0.0.2",
	license = "GPL-3.0-only",
	description = "Generate LaTeX exams using advanced Mako templates",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Johannes Bauer",
	author_email = "joe@johannes-bauer.com",
	url = "https://github.com/johndoe31415/pyexamgen",
	download_url = "https://github.com/johndoe31415/pyexamgen/archive/v0.0.2.tar.gz",
	keywords = [ "exam", "generator", "template" ],
	install_requires = [
		"mako",
	],
	entry_points = {
		"console_scripts": [
			"pyexamgen = pyexamgen.__main__:main"
		]
	},
	include_package_data = True,
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",
		"Programming Language :: Python :: 3.12",
		"Programming Language :: Python :: 3.13",
	],
)
