anymarkup-core
==============

.. image:: https://travis-ci.org/bkabrda/anymarkup-core.svg?branch=master
   :target: https://travis-ci.org/bkabrda/anymarkup-core
   :alt: Build Status

.. image:: https://landscape.io/github/bkabrda/anymarkup-core/master/landscape.svg?style=flat
   :target: https://landscape.io/github/bkabrda/anymarkup-core/master
   :alt: Code Health

.. image:: https://coveralls.io/repos/bkabrda/anymarkup-core/badge.svg?branch=master
   :target: https://coveralls.io/r/bkabrda/anymarkup-core?branch=master
   :alt: Coverage

This is the core library that implements functionality of https://github.com/bkabrda/anymarkup.
You can install this if you only want to use a subset of anymarkup parsers. For example, you
can do this::

  $ pip install anymarkup-core PyYAML
  $ python -c "import anymarkup_core; print(anymarkup_core.parse('foo: bar'))"

... and you don't need `xmltodict` installed, for example. You can use anymarkup-core
in the same way you use anymarkup, except you have to import from `anymarkup_core`, obviously.
