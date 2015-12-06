.. _Maciej Fijalkowski: https://bitbucket.org/fijal/
.. _example-interpreter2: https://bitbucket.org/fijal/example-interpreter2
.. _RPython: http://rpython.readthedocs.org/
.. _Python: https://www.python.org/
.. _Kermit: https://github.com/prologic/kermit
.. _virtualenv: https://pypy.python.org/pypi/virtualenv
.. _virtualenvwrapper: https://pypy.python.org/pypi/virtualenvwrapper
.. _Docker: https://docker.com/
.. _Latest Releases: https://github.com/prologic/hermit/releases
.. _example interpreter: https://bitbucket.org/pypy/example-interpreter

Hermit - An example interpreter
===============================

.. image:: https://travis-ci.org/prologic/hermit.svg
   :target: https://travis-ci.org/prologic/hermit
   :alt: Build Status

.. image:: https://coveralls.io/repos/prologic/hermit/badge.svg
   :target: https://coveralls.io/r/prologic/hermit
   :alt: Coverage

.. image:: https://landscape.io/github/prologic/hermit/master/landscape.png
   :target: https://landscape.io/github/prologic/hermit/master
   :alt: Quality

An Interpreter written in `RPython`_ continuing
`Maciej Fijalkowski`_'s (@fijal) original work in `example-interpreter2`_
with ideas and features taken from `Kermit`_.


Prerequisites
-------------

It is recommended that you do all development using a Python Virtual
Environment using `virtualenv`_ and/or using the nice `virtualenvwrapper`_.

::
   
    $ mkvirtualenv hermit


Installation
------------

Grab the source from https://github.com/prologic/hermit and either
run ``python setup.py develop`` or ``pip install -e .``

::
    
    $ git clone https://github.com/prologic/hermit.git
    $ cd hermit
    $ pip install -e .


Building
--------

To build the interpreter simply run ``hermit/main.py`` against the RPython
Compiler. There is a ``Makefile`` that has a default target for building
and translating the interpreter.

::
    
    $ make

You can also use `Docker`_ to build the interpreter:

::
    
    $ docker build -t hermit .


Usage
-----

You can either run the interpreter using `Python`_ itself or by running the
compiled interpreter ``hermit`` in ``./bin/hermit``.

::
    
    $ ./bin/hermit examples/hello.her

Untranslated running on top of `Python`_ (*CPython*):

::
    
    $ hermit examples/hello.her


Grammar
-------

The grammar of hermit is currently as follows:

::
  
    main : expr
    expr : expr + expr
           | expr ; expr
           | T_NUMBER
           | T_VARIABLE
           | T_FLOAT_NUMBER
           | T_VARIABLE = expr
