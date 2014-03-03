import datetime
from taskplot import taskplot

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
