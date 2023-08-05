******
envrpt
******

.. image:: https://img.shields.io/pypi/v/envrpt.svg
   :target: https://pypi.org/project/envrpt
.. image:: https://img.shields.io/pypi/l/envrpt.svg
   :target: https://pypi.org/project/envrpt
.. image:: https://github.com/jayclassless/envrpt/workflows/Test/badge.svg
   :target: https://github.com/jayclassless/envrpt/actions


.. contents:: Contents


Overview
--------
``envrpt`` analyzes the packages installed in a Python environment and produces
a report of its findings. Currently, it:

* Identifies and catalogs all packages installed in the environment.
* Checks `PyPI <https://pypi.org>`_ to determine if new versions of installed
  packages are available.
* Checks for missing and incorrect dependencies amongst the installed packages.
* Checks installed packages against `Safety DB
  <https://github.com/pyupio/safety-db>`_ to identify those with known
  vulnerabilities.


Usage
-----
When installed into the environment you wish to analyze (``pip install
envrpt``), the ``envrpt`` command should become available::

    $ envrpt --help
    usage: envrpt [-h] [-v] [--skip-outdated-check] [--skip-vulnerability-check] [-f {console,html,json,markdown}]
                  [-o FILENAME] [-s] [-p]

    Analyzes the packages installed in a Python environment

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      --skip-outdated-check
                            skips querying the package server for new versions of packages
      --skip-vulnerability-check
                            skips checking installed packages for known vulnerabilities
      -f {console,html,json,markdown}, --format {console,html,json,markdown}
                            the format to output the environment report in; if not specified, defaults to console
      -o FILENAME, --output FILENAME
                            the filename to write the output to; if not specified, defaults to stdout
      -s, --summary-only    only show a summary of the environment
      -p, --problems-only   only show packages with problems


License
-------
``envrpt`` is released under the terms of the `MIT License`_.

.. _MIT License: https://opensource.org/licenses/MIT

