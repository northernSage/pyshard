.. PyShard documentation master file, created by
   sphinx-quickstart on Wed May 27 21:44:16 2020.

Welcome to PyShard's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

|

Features
==================

|

An ease-of-use, customized Pyinstaller wrapper made entirely in python.

|

- Able to handle complex project structures by generating a recursive dependency tree of configuration and resource files, later parsed to a series of instructions which Pyinstaller_ can understand and use to properly reproduce the original directory hierarchy.
- Solves the infamous UniversalCRT_ problem of missing dlls for Python >= 3.5 targeting Windows < 10 by automatically bundling the required Visual C++ run-time dlls from visual Studio 2015, which has been renamed into "Universal CRT" and is now part of Windows 10 core.

|

.. image:: ../resources/demogif.gif

.. _UniversalCRT: https://devblogs.microsoft.com/cppblog/introducing-the-universal-crt/
.. _Pyinstaller: https://pyinstaller.readthedocs.io/en/stable/index.html

|


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


PyShard gui
===================
.. automodule:: gui.ShardMenu
   :members:
   :private-members:
   :undoc-members:
   
PyShard shard module
====================
.. automodule:: pyshard.shard.Shard
   :members:
   :private-members:
   :undoc-members:
   
