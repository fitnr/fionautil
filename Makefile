# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2015-6, Neil Freeman <contact@fakeisthenewreal.org>

README.rst: README.md
	- pandoc $< -o $@
	@touch $@
	python setup.py check --restructuredtext --strict

.PHONY: cov deploy clean
cov:
	- coverage run setup.py test
	coverage report
	coverage html

deploy: README.rst | clean
	python setup.py register
	python setup.py sdist
	rm -rf build
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	git push
	git push --tags

clean: ; rm -rf dist build