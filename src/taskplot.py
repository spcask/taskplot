#!/usr/bin/env python3

# Copyright (c) 2014 Susam Pal
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""Susam's taskplot program to plot effort versus time for multiple tasks.

This module provides a class called TaskPlot and a command line
interface application based on it to plot effort made on various
tasks versus time.

There are three ways to feed data to this program (either TaskPlot class
or the CLI application).

  1. Using a task directory containing task files: When effort data is
     fed using a directory of task files, the filename of each task file
     is expected to be of the format yyyy-mm-dd.* where yyyy-mm-dd
     represents the date of the effort, and .* represents any extension
     name. Files which do not conform to this naming pattern are
     ignored. This naming pattern may be altered by using the datefmt
     keyword argument of add_effort_from_directory method or the
     --datefmt command line option. Each task file should contain one
     more task entries in a specific format illustrated with the
     following examples:

        GYM: [xx]
        WORK: [xxxx] [xx]
        WORK: [xx] [x.] [..]

     Each task entry must fit in one line. Each task entry contains a
     task name followed immediately by a colon and whitespace. This is
     followed by one or more whitespace separated effort groups. Each
     effort group consists of a pair of square brackets enclosing x's or
     dots. Each x represents 30 minutes of effort. Each dot represents
     no effort. An effort group may contain as many number of x's and
     dots as desired by the user.  Square brackets and dots are ignored
     while determining the amount of effort. Only x's are counted.
     Therefore, how various x's are arranged into effort groups are
     irrelevant to this program.  They are only meant to enhance
     readability by humans.

     Leading or trailing whitespace is allowed around each task entry.
     Lines that do not conform to this format are ignored. Therefore,
     any line not conforming to this format may be used as comments in
     the file.

  2. Using a task list file: A task list consists of multiple task
     blocks. Each task block consists of a header followed by date
     entries. Here is an example of a task block. Each task block begins
     with a header. A header consists of the string 'DATE' followed by
     whitespace separated task names. A header is recognized by
     searching for lines that contain 'DATE' as the first word (the
     search is case-insensitive). The header may be followed by one or
     more task entries. Each entry begins with date of effort expected
     in yyyy-mm-dd format by default. The date format may be changed
     using the datefmt keyword argument of add_effort_from_file method
     or the --datefmt command line option.

        DATE GYM WORK MUSIC
        2014-02-01 2 0 2.5
        2014-02-03 1 5.5 1
        2014-02-04 0 6 1

     There may be multiple task blocks in a task list file as shown
     below.

        DATE GYM WORK MUSIC
        2014-02-01 2 0 2.5
        2014-02-03 1 5.5 1
        2014-02-04 0 6 1

        DATE WORK GOLF
        2014-02-06 5 2
        2014-02-08 0 2

     Blank lines are ignored. Arbitrary amount of whitespace between
     each token in a line is allowed. Leading and trailing whitespace is
     allowed in each line. Therefore, task blocks may be neatly arranged
     in a tabular fashion by adding extra whitespace. Here is an
     example.

        DATE        GYM   WORK  MUSIC
        2014-02-01  2     0     2.5
        2014-02-03  1     5.5   1
        2014-02-04  0     6     1

        DATE        WORK  GOLF
        2014-02-06  5     2
        2014-02-08  0     2

  3. Using your own program that uses the TaskPlot class: If the data
     needs to be added from source which are not in either of the two
     formats explained in the previous two points, then a separate
     program needs to be written that use the TaskPlot class defined in
     this module. Here is an example of a simple program using the
     TaskPlot class.

        import taskplot
        import datetime

        taskplot = taskplot.TaskPlot()
        taskplot.add_effort('GYM', datetime.datetime(2014, 1, 1), 0.5)
        taskplot.add_effort('GYM', datetime.datetime(2014, 1, 2), 0.5)
        taskplot.add_effort('GYM', datetime.datetime(2014, 1, 3), 1.0)
        taskplot.add_effort('WORK', datetime.datetime(2014, 1, 2), 5.0)
        taskplot.add_effort('WORK', datetime.datetime(2014, 1, 3), 6.0)
        taskplot.add_effort('WORK', datetime.datetime(2014, 1, 3), 1.0)

        taskplot.print_summary()
        taskplot.plot_graph()
        taskplot.save_graph('taskplot.png')

     Note that the add_effort may be called multiple times for the same
     task and same date.

Once the data is fed into the program, it can be used to show a
summary of the tasks on the standard output as well as a plot a graph of
effort versus time for the tasks.
"""


# Module attributes for pydoc
__version__ = '0.1.0'
__date__ = '21 February 2013'
__author__ = 'Susam Pal <susam@susam.in>'
__credits__ = ('Matplotlib development team for a wonderful '
               'plotting library.')


import os
import argparse
import configparser
import sys
import datetime
import collections
import re

from matplotlib import ticker
from matplotlib import dates
from matplotlib import pyplot
from dateutil import rrule


# Module attributes for CLI
_prog = os.path.basename(sys.argv[0]).split('.', 1)[0]
_copyright = 'Copyright (c) 2014 Susam Pal'
_license = (
    'This is free software. You are permitted to redistribute and use it in\n'
    'source and binary forms, with or without modification, under the terms\n'
    'of the Simplified BSD License. See <http://susam.in/licenses/bsd/> for\n'
    'the complete license.'
)


class _Task:

    """A single task.

    Each instance of this class is used to save and query effort made on
    a task.

    Methods:

    add_effort       -- Add effort made on this task on the specified date.
    get_effort       -- Get effort made on this task on the specified date.
    get_total_effort -- Get the total effort made on this task.
    get_min_date     -- Get the earliest date of effort on this task.
    get_max_date     -- Get the latest date of effort on this task.
    """

    def __init__(self):
        """Initialize the task."""
        self._data = collections.Counter()

    def add_effort(self, date, effort):
        """Add effort made on this task on the specified date.

        The specified effort is added to the effort for the specified
        date. Effort is usually a count that indicates how much of the
        task has been complete, e.g. number of hours, number of units of
        work, etc.

        Arguments:
        date   -- Date of effort (type: datetime.datetime)
        effort -- Effort (type: float)
        """
        self._data[date] += effort

    def get_effort(self, date):
        """Get effort made on this task on the specified date.

        Arguments:
        date -- Date of effort (type: datetime.datetime)

        Return: Effort (type: float)
        """
        return self._data[date]

    def get_total_effort(self):
        """Get the total effort made on this task.

        Return: Total effort (type: float)
        """
        return sum(self._data.values())

    def get_min_date(self):
        """Get the earliest date of effort on this task.

        Return: Earliest date of effort (type: datetime.datetime)
        """
        return min(self._data)

    def get_max_date(self):
        """Get the latest date of effort on this task.

        Return: Latest date of effort (type: datetime.datetime)
        """
        return max(self._data)


class TaskPlot:

    """Show effort summary and plot effort versus time.

    The effort data for tasks can be fed to an instance of this class in
    one of three different ways.

      1. From a task directory containing task files.

            taskplot = taskplot.TaskPlot()
            taskplot.add_effort_from_directory('.')

      2. From a task list file.

            taskplot = taskplot.TaskPlot()
            taskplot.add_effort_from_file('tasklist.txt')

      3. Calling the add_effort method repeatedly.

            taskplot = taskplot.TaskPlot()
            taskplot.add_effort('GYM', datetime.datetime(2014, 1, 1), 0.5)
            taskplot.add_effort('WORK', datetime.datetime(2014, 1, 2), 5.0)

    See the module docstring for more information on the various ways of
    feeding data to print summary and plot graph.

    Methods:
    add_effort_from_directory -- Add effort data from a task directory.
    add_effort_from_file      -- Add effort data from a task list file.
    """

    def __init__(self):
        """Initialize an instance of this class."""
        self._tasks = {}

    def add_effort_from_directory(self, path,
                                  start_date=None, end_date=None,
                                  datefmt='%Y-%m-%d'):
        """Add effort data from a task directory.

        If start_time is not None, then task files for dates before
        start_time are ignored. If end_date is not None, then task files
        for dates after end_date are ignored.

        In other words, if both start_date and end_date are not None,
        then effort data is read from task files for dates from
        start_date to end_date only.

        Arguments:
        path       -- Path of the task directory (type: str)

        Keyword arguments:
        start_date -- Minimum date for a task file for it to be read
                      (type: datetime.datetime) (default: None)
        end_date   -- Maximum date for a task file for it to be read
                      (type: datetime.datetime) (default: None)
        datefmt    -- Expected format of the date in the name of the
                      task files (ignoring the extension name) in task
                      directory (type: str) (default: '%Y-%m-%d')
        """
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                extless = filename.split('.')[0]
                try:
                    date = datetime.datetime.strptime(extless, datefmt)
                except ValueError:
                    # Ignore task files that do not contain date in the
                    # filename
                    continue

                # Ignore task files outside the specified date range
                if start_date is not None and date < start_date or \
                   end_date is not None and date > end_date:
                    continue

                filepath = os.path.join(dirpath, filename)

                # Look for lines that look like:
                #     PROGRAMMING: [xx] [xx] [..]
                pattern = r'^\s*\w+:(?:\s+\[(?:x|\.)+\])+\s*$'
                for line in open(filepath):
                    match = re.match(pattern, line)
                    if match is not None:
                        tokens = match.group().strip().split(':')
                        task_name = tokens[0]
                        effort = tokens[1].count('x') / 2
                        self.add_effort(task_name, date, effort)

    def add_effort_from_file(self, path, start_date=None, end_date=None,
                             datefmt='%Y-%m-%d'):
        """Add effort data from a task list file.

        If start_time is not None, then task entries for dates before
        start_time are ignored. If end_date is not None, then task
        entries for dates after end_date are ignored.

        In other words, if both start_date and end_date are not None,
        then effort data is read from task entries for dates from
        start_date to end_date only.

        Arguments:
        path       -- Path of the task directory (type: str)

        Keyword arguments:
        start_date -- Minimum date for a task entry for it to be read
                      (type: datetime.datetime) (default: None)
        end_date   -- Maximum date for a task entry for it to be read
                      (type: datetime.datetime) (default: None)
        datefmt    -- Expected format of the date in each task entry
                      (type: str) (default: '%Y-%m-%d')
        """
        for line in open(path):
            line = line.strip()
            if not line:
                # Skip blank line
                continue
            if re.match('^date\s+(?i)', line):
                # Parse header
                task_names = line.split()[1:]
            else:
                # Parse date entry
                tokens = line.split()
                date = datetime.datetime.strptime(tokens[0], datefmt)

                # Ignore task entries outside the specified date range
                if start_date is not None and date < start_date or \
                   end_date is not None and date > end_date:
                    continue

                # Add effort values from the task entry
                efforts = tokens[1:]
                for task_name, effort in zip(task_names, efforts):
                    self.add_effort(task_name, date, float(effort))

    def add_effort(self, task_name, date, effort):
        """Add effort data for the specified task on specified date.

        Arguments:
        task_name -- Name of the task (type: str)
        date      -- Date of effort (type: datetime.datetime)
        effort    -- Effort value (type: float)
        """
        date = _get_midnight_date(date)
        if task_name not in self._tasks:
            self._tasks[task_name] = _Task()
        self._tasks[task_name].add_effort(date, effort)

    def print_summary(self, task_names=None,
                      start_date=None, end_date=None):
        """Print a summary of tasks within specified date range.

        A daily effort summary and a cumulative effort summary of the
        specified tasks is printed for the specified date range. If
        task_names is None, then summary of all tasks is printed. If
        start_date is None, then summary is printed from the first date
        of effort. If end_date is None, then summary is printed till the
        last date of effort.

        Keyword arguments:
        task_names -- Names of tasks for which summary should be printed
                      (type: list) (default: None)
        start_date -- Start of summary date range
                      (type: datetime.datetime) (default: None)
        end_date   -- End of summary date range
                      (type: datetime.datetime) (default: None)
        """
        print('[DAILY]')
        self.print_bare_summary(task_names, start_date, end_date)

        print()
        print('[CUMULATIVE]')
        self.print_bare_summary(task_names, start_date, end_date, True)

        if end_date is None:
            end_date = self.get_max_date()

        days = (end_date - self.get_min_date()).days + 1
        print()

        if task_names is not None:
            tasks_effort = self.get_total_effort(task_names)
            print('TASKS: {:.1f} hours in {} days ({:.1f} h/d)'.format(
                  tasks_effort, days, tasks_effort / days))

        total_effort = self.get_total_effort()
        print('TOTAL: {:.1f} hours in {} days ({:.1f} h/d)'.format(
              total_effort, days, total_effort / days))

    def print_bare_summary(self, task_names=None,
                           start_date=None,
                           end_date=None,
                           cumulative=False,
                           date_format='%Y-%m-%d',
                           effort_format='7.1f'):
        """Print a simple summary of tasks within specified date range.

        A simple summary of the specified tasks is printed for the
        specified date range. If task_names is None, then summary of
        all tasks is printed. If start_date is None, then summary is
        printed from the first date of effort. If end_date is None, then
        summary is printed till the last date of effort.

        Keyword arguments:
        task_names    -- Names of tasks for which summary should be printed
                         (type: list) (default: None)
        start_date    -- Start of summary date range
                         (type: datetime.datetime) (default: None)
        end_date      -- End of summary date range
                         (type: datetime.datetime) (default: None)
        cumulative    -- Whether to print cumulative summary
                         (type: bool) (default: False)
        date_format   -- Format of date in summary
                         (type: str) (default: '%Y-%m-%d')
        effort_format -- Format of effort in summary
                         (type: str) (default: '7.1f')
        """
        min_date = self.get_min_date()
        max_date = self.get_max_date()

        if task_names is None:
            task_names = self.get_sorted_task_names()

        if start_date is None:
            start_date = min_date

        if end_date is None:
            end_date = max_date

        if start_date < min_date:
            start_date = min_date

        date_format = '{:' + date_format + '}'
        effort_format = '{:' + effort_format + '}'

        date_len = len(date_format.format(datetime.datetime(1, 1, 1)))
        effort_len = len(effort_format.format(0))
        task_name_len = max(len(s) for s in task_names)
        if effort_len < task_name_len:
            effort_pad = ' ' * (task_name_len - effort_len)
        else:
            effort_pad = ''
            task_name_len = effort_len

        task_name_format = '{:>' + str(task_name_len) + '}'

        # Print title row
        date_header = ' ' * date_len
        task_header = '   '.join(task_name_format.format(s)
                                 for s in task_names)
        print(date_header, '  ', task_header, sep='')

        for date, efforts in self.efforts(task_names, start_date,
                                          end_date, cumulative):
            date_str = date_format.format(date) + ': '
            effort_str = ' + '.join(effort_pad +
                         effort_format.format(efforts[t]) for t in task_names)
            total_effort_str = effort_format.format(sum(efforts.values()))
            print(date_str, effort_str, ' = ', total_effort_str, sep='')

    def plot_graph(self, task_names=None,
                   start_date=None, end_date=None, color_map={}):
        """Plot a graph of effort versus time for specified tasks.

        The time axis is limited to the date range specified by
        start_date and end_date.

        If task_names is None, effort is plotted for all tasks. If
        start_date is None, the time axis of the graph begins with the
        date of first effort. If end_date is None, the time axis of the
        graph ends with the date of last effort.

        The color to be used to plot the effort for each task is
        specified by the color_map. It is a dictionary that maps each
        task name (type: str) to a color name (type: str). If the color
        for any task is missing from the color_map, it's color is
        decided on the fly using an internal set of colors.

        Keyword arguments:
        task_names -- Name of tasks for which effort should be plotted
                      (type: list) (default: None)
        start_date -- Beginning of the date range in time axis
                      (type: datetime.datetime) (default: None)
        end_date   -- End of the date range in time axis
                      (type: datetime.datetime) (default: None)
        color_map  -- Map of task names to colors
                      (type: dict) (default: {})
        """
        _assign_colors_to_tasks(self.get_sorted_task_names(), color_map)

        min_date = self.get_min_date()
        max_date = self.get_max_date()

        if task_names is None:
            task_names = self.get_sorted_task_names()

        if start_date is None:
            start_date = min_date

        if end_date is None:
            end_date = max_date

        # Although, the time axis of the graph can go beyond the time
        # range in the data, the line graphs should not go beyond the
        # date range in the data
        plot_start_date = max(start_date, min_date)
        plot_end_date = min(end_date, max_date)

        x_dates = []
        y_efforts = {t: [] for t in task_names}

        for date, efforts in self.efforts(task_names, plot_start_date,
                                          plot_end_date, True):
            x_dates.append(dates.date2num(date))
            for task_name in task_names:
                y_efforts[task_name].append(efforts[task_name])

        max_effort = max([y_efforts[t][-1] for t in task_names])
        graph_max_effort = max_effort + 5 - max_effort % 5

        pyplot.xlim(start_date, end_date)
        pyplot.ylim([0, graph_max_effort])

        for t in task_names:
            pyplot.plot_date(x_dates, y_efforts[t], linestyle='-',
                             markersize=3.0, color=color_map[t], label=t)

    def save_graph(self, image_path, xlabel='Days', ylabel='Effort'):
        """Save the plot of effort versus time.

        Arguments:
        image_path -- Path of the image to save the graph to (type: str)

        Keyword arguments:
        xlabel     -- Label for the time axis (type: str)
        ylabel     -- Label for the effort axis (type: str)
        """
        pyplot.xlabel(xlabel)
        pyplot.ylabel(ylabel)

        xaxis = pyplot.axes().xaxis
        xaxis.set_major_locator(dates.WeekdayLocator(byweekday=rrule.SU))
        xaxis.set_major_formatter(dates.DateFormatter('%b'))
        xaxis.set_tick_params('major', pad=20)
        xaxis.set_minor_locator(dates.DayLocator())
        xaxis.set_minor_formatter(dates.DateFormatter('%d'))

        yaxis = pyplot.axes().yaxis
        yaxis.set_major_locator(ticker.MultipleLocator(5))
        yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        yaxis.set_minor_locator(ticker.MultipleLocator(1))

        pyplot.grid(True, which='major', color='black',
                    linestyle='-', linewidth='0.25')
        pyplot.grid(True, which='minor', color='gray',
                    linestyle='-', linewidth='0.125')

        pyplot.legend()
        figure = pyplot.gcf()
        figure.set_size_inches(16, 9)
        pyplot.savefig(image_path, bbox_inches='tight')

    def efforts(self, task_names, start_date, end_date, cumulative):
        """Yield task efforts for each date in the specified date range.

        It yields a tuple of date (type: datetime.datetime) and effort
        map (type: dict) that maps each task to the effort made on the
        task. Therefore, the effort map is a dictionary with task names
        (type: str) as keys and effort (type: float) as values.

        Arguments:
        task_names -- Name of the tasks for which effort is required
                      (type: list)
        start_date -- Beginning of the date range of required task
                      efforts (type: datetime.datetime)
        end_date   -- End of the date range of required task efforts
                      (type: datetime.datetime)
        cumulative -- Whether cumulative effort values should be
                      returned (type: bool)

        Return: Generator of date and effort map tuples (type: generator)
        """
        start_date = _get_midnight_date(start_date)
        end_date = _get_midnight_date(end_date)
        min_date = self.get_min_date()
        max_date = self.get_max_date()
        if cumulative:
            computation_start_date = min_date
        else:
            computation_start_date = start_date

        date = computation_start_date
        cumulative_efforts = dict.fromkeys(task_names, 0)
        while date <= end_date:
            efforts = dict.fromkeys(task_names, 0)
            for task_name in task_names:
                effort = self._tasks[task_name].get_effort(date)
                efforts[task_name] = effort
                if cumulative:
                    cumulative_efforts[task_name] += effort

            if start_date <= date <= end_date:
                if cumulative:
                    yield date, cumulative_efforts
                else:
                    yield date, efforts
            date += datetime.timedelta(1)

    def get_total_effort(self, task_names=None):
        """Return total effort spent on the specified tasks.

        If task_names is None, then return total effort spent on all
        tasks.

        Arguments:
        task_names -- Name of the tasks (type: list)

        Return: Total effort (type: float)
        """
        if task_names is None:
            task_names = self.get_sorted_task_names()
        total_effort = 0
        for task_name in task_names:
            total_effort += self._tasks[task_name].get_total_effort()
        return total_effort

    def get_min_date(self):
        """Return first date of effort.

        The first date of effort is the earliest date of effort made on
        any task.

        Return: First date of effort (type: datetime.datetime)
        """
        min_dates = set()
        for task_name in self.get_sorted_task_names():
            min_dates.add(self._tasks[task_name].get_min_date())
        return min(min_dates)

    def get_max_date(self):
        """Return last date of effort.

        The last date of effort is the most recent date of effort made
        on any task.

        Return: Last date of effort (type: datetime.datetime)
        """
        max_dates = set()
        for task_name in self.get_sorted_task_names():
            max_dates.add(self._tasks[task_name].get_max_date())
        return max(max_dates)

    def get_sorted_task_names(self):
        """Return a sorted list of all task names.

        Return: Sorted list of task names (type: list)
        """
        return sorted(self._tasks.keys())


def _assign_colors_to_tasks(task_names, color_map):
    # A list of colors that look good in a graph
    color_bank = ['red', 'green', 'blue', 'magenta', 'purple',
                  'orange', 'crimson', 'brown', 'deeppink',
                  'maroon']

    # Colors from color_bank that have not been used in color_map
    unused_colors = [c for c in color_bank if
                     c not in color_map.values()]

    # Tasks for which no colors have been assigned in color_map
    tasks_without_colors = [t for t in task_names if
                            t not in color_map]

    # Assign colors in color_bank to tasks in tasks_without_color
    for i, task_name in enumerate(tasks_without_colors):
        color_map[task_name] = unused_colors[i % len(unused_colors)]


def _get_midnight_date(date):
    """Return midnight date for the specified date.

    Effectively, this function returns the start of the day for the
    specified date.

    Arguments:
    date -- An arbitrary date (type: datetime.datetime)

    Return: Midnight date (type: datetime.datetime)
    """
    return datetime.datetime(date.year, date.month, date.day)


def _get_month_start_date(date):
    """Return midnight of the first day of month with the specified date.

    Arguments:
    date -- An arbitrary date (type: datetime.datetime)

    Return: Midnight of the first day of month (type: datetime.datetime)
    """
    return datetime.datetime(date.year, date.month, 1)


def _get_month_end_date(date):
    """Return midnight of the last day of month with the specified date.

    Arguments:
    date -- An arbitrary date (type: datetime.datetime)

    Return: Midnight of the last day of month (type: datetime.datetime)
    """
    return (datetime.datetime(date.year, date.month + 1, 1) -
            datetime.timedelta(1))


# ------------------------ #
# CLI code below this line #
# ------------------------ #
def cli():
    """Run taskplot command line interface.

    Exceptions:
    FileNotFoundError -- If the there is no file or directory at the
                         path specified for the --path command line
                         argument
    """
    parser, args = _parse_arguments()
    _validate_arguments(parser, args)
    config = _parse_configuration()
    today = _get_midnight_date(datetime.datetime.today())

    # Add effort data for tasks
    taskplot = TaskPlot()
    if os.path.isdir(args.path):
        taskplot.add_effort_from_directory(args.path,
                                           args.data[0], args.data[1],
                                           args.datefmt)
    elif os.path.isfile(args.path):
        taskplot.add_effort_from_file(args.path,
                                      args.data[0], args.data[1],
                                      args.datefmt)
    else:
        raise FileNotFoundError('No such file or directory: '
                                "'{}'.".format(args.path))

    # Print summary
    if args.summary[0] is None:
        args.summary[0] = today - datetime.timedelta(4)

    if args.summary[1] is None:
        args.summary[1] = today

    taskplot.print_summary(args.tasks, *args.summary)

    # Plot graph
    if args.graph[0] is None:
        start_date = _get_month_start_date(today)

    if args.graph[1] is None:
        end_date = _get_month_end_date(today)

    taskplot.plot_graph(args.tasks, start_date, end_date,
                        color_map=dict(config['colors']))
    taskplot.save_graph(args.output)


def _parse_arguments():
    """Parse command line arguments.

    This function may end the program with an error if an error is found
    in the command line arguments.
    """
    epilog = 'Report bugs to <http://github.com/susam/taskplot/issues>.'

    parser = argparse.ArgumentParser(prog=_prog,
                                     epilog=epilog,
                                     add_help=False)

    parser.add_argument('path', nargs='?', default=os.getcwd(),
                        help='path to a directory containing task files,'
                             'or a file containing task list'
                             '(default: current directory)')

    parser.add_argument('-f', '--datefmt', default='%Y-%m-%d',
                        metavar='FORMAT',
                        help='date format used in filename (without '
                             'the extension name) of each task file '
                             'in a directory of task files, or dates '
                             'in a file containing task list')

    parser.add_argument('-t', '--tasks', nargs='*',
                        metavar='TASK',
                        help='tasks for which to plot effort (default: '
                             'effort for all tasks is plotted)')

    parser.add_argument('-d', '--data', nargs=2, default=['-', '-'],
                        metavar=('START', 'END'),
                        help='date range for which effort data should '
                             'be read; data outside this range is not '
                             'considered while showing summary or '
                             'plotting graph (default: all data)')

    parser.add_argument('-s', '--summary', nargs=2, default=['-', '-'],
                        metavar=('START', 'END'),
                        help='date range for which summary should be '
                             'shown (default: last 5 days)')

    parser.add_argument('-g', '--graph', nargs=2, default=['-', '-'],
                        metavar=('START', 'END'),
                        help='date range for which effort should be '
                             'plotted (default: current month)')

    parser.add_argument('-o', '--output', default='taskplot.png',
                        metavar='IMAGE',
                        help='output path of the graph image '
                             '(default: taskplot.png)')

    parser.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')

    parser.add_argument('-v', '--version', action='store_true',
                        help="show program's version and exit")

    args = parser.parse_args()

    if args.version:
        _show_version()
        sys.exit(0)

    return parser, args


def _validate_arguments(parser, args):
    """Validate command line arguments.

    Arguments:
    parser --  argument parser (type: argparse.ArgumentParser)
    args -- arguments (type: argparse.Namespace)

    Exception:
    ValueError -- If the times in args.data, args.summary or args.graph
                  are not in yyyy-mm-dd format
    """
    _parse_dates(args.data)
    _parse_dates(args.summary)
    _parse_dates(args.graph)


def _parse_dates(dates, datefmt='%Y-%m-%d'):
    """Parse time argument.

    Arguments:
    dates -- A list of date strings (type: list)

    Exceptions:
    ValueError -- If a date is not in yyyy-mm-dd format
    """
    if dates is None:
        return

    for i, date in enumerate(dates):
        if date == '-':
            dates[i] = None
        else:
            try:
                dates[i] = datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date: '{}'.".format(date))


def _parse_configuration():
    """Parse configuration for this program.

    The configuration is parsed from the ~/.taskplotrc file.

    Return: Configuration parser (type: configparser.ConfigParser)
    """
    confpath = os.path.join(os.path.expanduser('~'), '.taskplotrc')
    config = configparser.ConfigParser()
    config.optionxform = lambda x: x
    config.read(confpath)
    if 'colors' not in config:
        config['colors'] = {}
    return config


def _show_version():
    """Show version information."""
    print(_prog, __version__)
    print(_copyright)
    print()
    print(_license)
    print()
    print('Written by', __author__ + '.')


if __name__ == '__main__':
    try:
        cli()
    except (FileNotFoundError, ValueError) as e:
        print('{}: {}'.format(e.__class__.__name__, e))
