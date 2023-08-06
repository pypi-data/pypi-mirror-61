# Open Github

A simple script that opens a Github page from the command line.

## Installation

`pip install open-github`

After installing you can make the package available in your path and bind it to any shortcut you want.

`alias og='/Users/${USER}/Library/Python/3.7/lib/python/site-packages/open_github_pkg/__init__.py'`

https://pypi.org/project/open-github/

## Usage

Navigate to any directory with a github repository and run the alias you have assigned to the script.

Example:

`og`

This will open your browser with the appropiate Github repository homepage.

As well, running with the flag `-v` will simply print the url to the console.

`og -v`

## Deploying

In order to deploy package the following tools are needed, pip, sdist & twine.

#### Bump version

In the `setup.py` bump version of package.

#### Generate distribution archive

`python3 setup.py sdist bdist_wheel`

This command should output a lot of text and once completed should generate two files in the dist directory.

#### Upload the distrubution package

`python3 -m twine upload dist/*`

If you need to use the development environment simply use:

`python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*`



#### Reference:
- https://packaging.python.org/tutorials/packaging-projects/
- https://packaging.python.org/overview/