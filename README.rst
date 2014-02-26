TaskPlot - Plot your tasks
==========================

TaskPlot is a command line tool as well as a Python library module that
may be used from the command line or from another program to plot
progress in multiple tasks in a single graph.

.. sectnum::
.. contents::

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

Getting started
---------------
There are three ways to feed data to TaskPlot and let it plot graphs.

1. Using a task directory containing task files: Let us assume your
   current directory contains the following files and contents::

    -- 2014-02-01.txt --
    READING: [xx] [xx]
    MUSIC: [xx] [xx]
    READING: [x]

    -- 2014-02-03.txt --
    READING: [x]
    CODING: [xx]

    -- 2014-02-04.txt --
    READING: [xx] [x]
    MUSIC: [xx]

    -- 2014-02-08.txt --
    MUSIC: [xx]
    CODING: [xx] [xx]

    -- 2014-02-10.txt --
    READING: [xx]
    MUSIC: [xx]
    READING: [xx]

   Execute the following command in the current directory::

    taskplot

   The above command will plot a graph from those files and save it in
   a file called taskplot.png

   .. image:: http://i.imgur.com/AoAkGcK.png
      :width: 640px


2. Using a task list file: Let us assume your current directory contains
   a file called tasklist.txt with the following content::

    DATE        READING  MUSIC     CODING
    2014-02-01  1.0      0.5       0.0
    2014-02-03  0.5      0.0       1.0
    2014-02-04  0.5      0.5       0.5
    2014-02-05  0.5      0.0       0.5
    2014-02-08  0.5      0.5       1.5

    DATE        CHESS    MUSIC     CODING
    2014-02-09  1.0      0.5       0.5
    2014-02-10  1.5      1.0       0.5
    2014-02-11  0.5      1.0       1.0
    2014-02-12  2.0      0.5       0.0
    2014-02-15  0.0      0.0       0.5

   Execute the following command in the current directory::

    taskplot tasklist.txt

   The above command will plot a graph from those files and save it in
   a file called taskplot.png

   .. image:: http://i.imgur.com/Nk24ZOb.png
      :width: 640px

3. Using your own program: Here is an example program::

    import taskplot
    import datetime

    taskplot = taskplot.TaskPlot()
    taskplot.add_effort('READING', datetime.datetime(2014, 2, 1), 0.5)
    taskplot.add_effort('READING', datetime.datetime(2014, 2, 5), 1.0)
    taskplot.add_effort('READING', datetime.datetime(2014, 2, 8), 0.5)
    taskplot.add_effort('READING', datetime.datetime(2014, 2, 12), 0.5)
    taskplot.add_effort('CODING', datetime.datetime(2014, 2, 1), 1.0)
    taskplot.add_effort('CODING', datetime.datetime(2014, 2, 3), 1.0)
    taskplot.add_effort('CODING', datetime.datetime(2014, 2, 7), 1.0)
    taskplot.add_effort('MUSIC', datetime.datetime(2014, 2, 9), 1.0)
    taskplot.add_effort('MUSIC', datetime.datetime(2014, 2, 15), 1.0)
    taskplot.print_summary()
    taskplot.plot_graph()
    taskplot.save_graph('taskplot.png')

   Executing this program using Python 3 interpreter will plot a graph
   and generate the following graph.

   .. image:: http://i.imgur.com/oEby9Hf.png
      :width: 640px

Support
-------
To report any bugs, or ask any question, please visit
<https://github.com/susam/taskplot/issues>. Please search the existing
issues to see if there is an existing issue for the bug you want to
report or the question you want to ask. If it does not exist, then
please create a new issue.

Resources
---------
Here is a list of useful links about this project.

- `Latest release on PyPI <https://pypi.python.org/pypi/taskplot>`_
- `Source code on GitHub <https://github.com/susam/taskplot>`_
- `Issue tracker on GitHub <https://github.com/susam/taskplot/issues>`_
- `Change Log on GitHub
  <https://github.com/susam/taskplot/blob/master/CHANGES.rst>`_

License
-------
This is free software. You are permitted to redistribute and use it in
source and binary forms, with or without modification, under the terms
of the Simplified BSD License. See the LICENSE.rst file for the complete
license.

This software is provided WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
LICENSE.rst file for the complete disclaimer.
