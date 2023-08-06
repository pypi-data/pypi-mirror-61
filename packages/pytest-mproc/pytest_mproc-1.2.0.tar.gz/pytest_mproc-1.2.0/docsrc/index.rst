.. pytest_mpdist documentation master file, created by
   sphinx-quickstart on Sat Feb  8 16:47:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pytest_mpdist's documentation!
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   developer-guide


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
============

Welcome to pytest-mpdist, a plugin for pytest to run distributed testing via multiprocessing.  This manner
of distributed testing has several advantages, including more efficient execution over pytest-xdist in many cases.

xdist works for cases perhaps where there are large number of tests, but the cost of overhead in using rsync and
overall implementation prevents realization of test-execution-time gains that one might hope for.

To begin using pytest mpdist, just install:

% pip install pytest-mpdist


Usage
=====

To use with pytest, you use the -C or equivalently --cores argument to specify how many cores to run on:

% pytest --cores 3 [remaining arguments]

or to specify use of all available cores:

% pytest --cores auto [remaining arguments]

You can also specify things like "auto*2" or "auto/2" for number of cores

Grouping Tests
==============

By default all tests are assumed independently runnable and isolated from one another.  That is the order in which they
run within which process does not matter.  You may wish to specify a group of tests that must run serially within the
same process/thread.  To do this, annotate each test using a unique name for the group:

.. code-block:: python

   import pytest_mproc
   TEST_GROUP1 = "group1"

   @pytest_mproc.group(TEST_GROUP1)
   def test_something1():
        pass

   @pytest_mproc.group(TEST_GROUP1)
   def test_something2():
        pass

Likewise, you can use the same annotation on test class to group all test methods within that class:

.. code-block:: python

   import pytest_mproc

   TEST_GROUP_CLASSS = "class_group"

   @pytest.mproc.group(TEST_GROUP_CLASS)
   class TestClass:
       def test_method1(self):
          pass

       def test_method2(self):
          pass

This is useful if the tests are using a common resource for testing and parallelized execution of tests might
result in interference.

Global Initializers/Finalizers
==============================

.. warning::
    Much like pytest-xdist, session level variables are called once for EACH THREAD.  So if you run on 4 cores, each
    session-scoped fixture will run 4 times.  This is because forking is used to parallelize tests.

To add an initializer and finalzier to be called only once before all tests execute and after all tests executed,
respectively, use fixture from the pytest_mproc_utils package:

.. code-block:: python

   from pytest_mproc utils import pytest_mproc_global_initializer, pytest_mproc_global_finalizer
   @pytest_mproc_global_initializer
   def initualizer():
       pass

   @pytest_mproc_global_finalizer
   def finalizer():
       pass

