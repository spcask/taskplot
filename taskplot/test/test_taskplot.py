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


"""Tests for taskplot package."""


import unittest
import datetime

from taskplot import taskplot

class TaskPlotTest(unittest.TestCase):

    def test_get_total_effort(self):
        # Empty taskplot
        tp = taskplot.TaskPlot()
        self.assertEqual(tp.get_total_effort(), 0)
        self.assertRaises(KeyError, tp.get_total_effort, ['INVALID'])
        # Taskplot with data
        tp = self._get_test_taskplot()
        self.assertEqual(tp.get_total_effort(), 15)
        self.assertEqual(tp.get_total_effort(['MUSIC']), 3)
        self.assertEqual(tp.get_total_effort(['CHESS']), 12)
        self.assertEqual(tp.get_total_effort([]), 0)
        self.assertRaises(KeyError, tp.get_total_effort, ['INVALID'])

    def test_get_min_date(self):
        # Empty taskplot
        tp = taskplot.TaskPlot()
        self.assertIsNone(tp.get_min_date())
        # Taskplot with data
        tp = self._get_test_taskplot()
        self.assertEqual(tp.get_min_date(), datetime.datetime(2014, 2, 1))

    def test_get_max_date(self):
        # Empty taskplot
        tp = taskplot.TaskPlot()
        self.assertIsNone(tp.get_max_date())
        # Taskplot with data
        tp = self._get_test_taskplot()
        self.assertEqual(tp.get_max_date(), datetime.datetime(2014, 2, 3))

    def test_get_sorted_task_names(self):
        # Empty taskplot
        tp = taskplot.TaskPlot()
        self.assertEqual(tp.get_sorted_task_names(), [])
        # Taskplot with data
        tp = self._get_test_taskplot()
        self.assertEqual(tp.get_sorted_task_names(), ['CHESS', 'MUSIC'])

    def _get_test_taskplot(self):
        tp = taskplot.TaskPlot()
        tp.add_effort('MUSIC', datetime.datetime(2014, 2, 1), 1)
        tp.add_effort('MUSIC', datetime.datetime(2014, 2, 1), 2)
        tp.add_effort('CHESS', datetime.datetime(2014, 2, 2), 3)
        tp.add_effort('CHESS', datetime.datetime(2014, 2, 2), 4)
        tp.add_effort('CHESS', datetime.datetime(2014, 2, 3), 5)
        return tp
