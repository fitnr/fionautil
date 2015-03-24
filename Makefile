# This file is part of fionautil.
# http://github.com/fitnr/fionautil

# Licensed under the GPLv3 license:
# http://www.opensource.org/licenses/GPLv3-license
# Copyright (c) 2015, Neil Freeman <contact@fakeisthenewreal.org>

readme.rst: readme.md
	pandoc -o $@ $<
