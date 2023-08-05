pip-reqs
========

Command line tools to streamline and speed up management of pip requirements using a remote wheels proxy instance.


Release
-------

To release a new version, update the CHANGELOG.rst file, update the version in the ``pip_reqs/__init__.py`` file and execute the following commands::

   python3 setup.py sdist bdist_wheel
   twine upload dist/*

