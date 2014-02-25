TaskPlot - Plot your tasks
==========================

TaskPlot is a command line tool as well as a Python library module that
may be used from the command line or from another program to plot
progress in multiple tasks in a single graph.

Requirements
------------
This package should be used with Python 3.4 or any later version of
Python interpreter.

On a Windows system, the following packages must be installed for
Python 3.4 from <http://www.lfd.uci.edu/~gohlke/pythonlibs/>:
numpy, dateutil, pyparsing, six and matplotlib.

On a Linux system, the python3-matplotlib package and the packages it
depends on must be installed. On a Debian system, the following command
may be used to install the required packages and execute the script::

    aptitude install python3-matplotlib

This package uses the Matplotlib library to plot graphs. 

Installation
------------
You can install this package using pip3 using the following command::

    pip3 install taskplot

You can install this package from source distribution. To do so,
download the latest .tar.gz file from
<https://pypi.python.org/pypi/taskplot>, extract it, then open command
prompt or shell, and change your current directory to the directory
where you extracted the source distribution, and then execute the
following command::

    python3 setup.py install

Note that on a Windows system, you may have to replace ``python3`` with
the path to your Python 3 interpreter.

Support
-------
To report any bugs, or ask any question, please visit
<https://github.com/susam/taskplot/issues>. Please search the existing
issues to see if there is an existing issue for the bug you want to
report or the question you want to ask. If it does not exist, then
please create a new issue.

License
-------
This is free software. You are permitted to redistribute and use it in
source and binary forms, with or without modification, under the terms
of the Simplified BSD License. See the LICENSE.rst file for the complete
license.

This software is provided WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
LICENSE.rst file for the complete disclaimer.
