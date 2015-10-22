# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

README.rst: README.md
	pandoc $< -o $@ || cp $< $@

.PHONY: cov deploy
cov:
	coverage run setup.py test
	coverage html
	open htmlcov/index.html

deploy:
	rm -rf dist build
	python setup.py sdist
	rm -rf build
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
