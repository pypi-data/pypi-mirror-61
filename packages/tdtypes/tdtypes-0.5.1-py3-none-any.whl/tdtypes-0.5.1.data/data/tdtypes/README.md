# tdtypes

[![PyPi](https://img.shields.io/pypi/v/tdtypes.svg)](https://pypi.python.org/pypi/tdtypes) [![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) ![Python3.7+](https://img.shields.io/pypi/pyversions/tdtypes.svg)

[tdtypes](https://bitbucket.org/padhia/tdtypes) is a Python library provides an abstraction layer for Teradata Database objects and utilities. By default It uses [teradatasql](https://pypi.org/project/teradatasql/), but generally, it should be possible to use any [DB API](https://www.python.org/dev/peps/pep-0249/) compliant library.

*NOTES:*

-   This started as a personal project, but it is being made available as an open-source library in the hope that someone else might find it useful. This library does not come with any kind of warranty.
-   *Python2* series is no longer supported.
-   Although no longer the default, but older [teradata](https://pypi.python.org/pypi/teradata/) and [pyodbc](https://github.com/mkleehammer/pyodbc) modules can still be used.
-   This library is not endorsed by [Teradata Inc](http://www.teradata.com/).

## Installation

Use Python's `pip` utility to install `tdtypes`.

    $ python -m pip install -U tdtypes

## Customizations

It is possible to customize how **tdtypes** library obtains a raw database connection. This might be helpful, for example, to use DB API modules other than `teradatasql`, or get authentication information in ways other than the default implementation. This can be done by creating `tdconn_site.py` module and place it in your `PYTHONPATH`. Please consult `tdconn_default.py` module for guidance on creating your own custom module.

The default implementation allows applications to either pass connection information as a parameter or get connection information from `TDCONN` environment variable at run-time. Either way, connection information consists of a valid *JSON* string as expected by [teradatasql](https://pypi.org/project/teradatasql/) module.

Another customization allows how **tdtypes** library searches for and obtains Table and View XML definitions. The default implementation uses *DBC.TablesV* for searching, and `SHOW ... IN XML` SQL statement to get XML definition.  Placing *tdfinder_site.py* in `PYTHONPATH` will override the default search and instantiation behaviors. To create a custom *tdfinder_site.py* module, please consult *tdfinder_default.py*.

## Support

Report bugs using [issue tracker](https://bitbucket.org/padhia/tdtypes/issues?status=new&status=open). I'll try to provide a fix as soon as I can. If you have already developed a fix, send me a pull request.

## Contributions

Feel free to fork this repository and enhance it in any way you see fit. If you think your changes will benefit more people, send me a pull request.
