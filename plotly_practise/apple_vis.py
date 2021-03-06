import plotly as py
import pandas as pd
import numpy as np

from datetime import datetime
from datetime import time as dt_tm
from datetime import date as dt_date

import plotly.plotly as py
import plotly.tools as plotly_tools
from plotly.graph_objs import *

import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
from matplotlib.finance import quotes_historical_yahoo
import matplotlib.pyplot as plt

from scipy.stats import gaussian_kde

from IPython.display import HTML

py.sign_in("yabebal", "amestkilo163291")

#Let's grab Apple stock data using the matplotlib finance model from
#2014, then take a moving average with a numpy convolution.
x = []
y = []
ma = []

def moving_average(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

date1 = dt_date( 2014, 1, 1 )
date2 = dt_date( 2014, 12, 12 )
quotes = quotes_historical_yahoo('AAPL', date1, date2)
if len(quotes) == 0:
    print "Couldn't connect to yahoo trading database"
else:
    dates = [q[0] for q in quotes]
    y = [q[1] for q in quotes]
    for date in dates:
        x.append(datetime.fromordinal(int(date))\
                .strftime('%Y-%m-%d')) # Plotly timestamp format
    ma = moving_average(y, 10)


#Now graph the data with Plotly. See here for Plotly's line plot
#syntax and here for getting started with the Plotly Python client.
xy_data = Scatter( x=x, y=y, mode='markers', marker=Marker(size=4), name='AAPL' )
# vvv clip first and last points of convolution
mov_avg = Scatter( x=x[5:-4], y=ma[5:-4], \
                  line=Line(width=2,color='red',opacity=0.5), name='Moving average' )
data = Data([xy_data, mov_avg])

py.iplot(data, filename='apple stock moving average')

#Save the plot URL - we'll use it when generating the report later.
first_plot_url = py.plot(data, filename='apple stock moving average', auto_open=False,)
print first_plot_url
