1. Create setup.py file then

####Build
2. `python setup.py bdist_wheel` this creates new files

#### Local installation of package w/o uploading
3. `pip install -e .` for local installation
4. `python setup.py bdist_wheel sdist` for packaging

Use this to create gitignore files

https://www.gitignore.io/

`pip install twine` tool required for publishing package to PyPI

use: `twine upload dist/*`

username: __token__
pwd: pypi-<token_value>