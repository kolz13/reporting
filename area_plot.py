import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import numpy as np

def create_area_plot(graph_data,title='30 Day Rolling Traffic',ytitle='30 Day Rolling Traffic'):
  '''
  Create an area plot graph from time series data.
  :param graph_data: A pandas dataframe of time series data.
  :param title: Chart title
  :param ytitle: Y axis title
  :return: An area plot of the labels along a time frame and a csv of the data.
  '''
  # These are the "Tableau 20" colors as RGB.
  tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
               (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
               (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
               (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
               (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

  # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
  for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

  # Set series labels from the columns of graph data
  labels = list(graph_data)

  # Set the x values to the timeseries values (the index of graph data)
  x = graph_data.index.values

  # Handle the case if only a series. See if we need to create a stacked graph or just a timeseries.
  if isinstance(graph_data, pd.core.frame.DataFrame):
    y = [pd.to_numeric(graph_data[label]).tolist() for label in labels]
  else:
    y = graph_data

  fig, ax = plt.subplots(1, figsize=(12,7),edgecolor='none')

  # Set stacked area graph, colors, and labels
  ax.stackplot(x,y,colors=tableau20,labels=labels)

  # Set the chart and axis titles from the variables passed in.
  fig.suptitle(title, fontsize=20)
  plt.ylabel(ytitle, fontsize=16)

  # Format axis to date and set the boundries of the days
  fig.autofmt_xdate()
  ax.set_xlim([min(graph_data.index.values), max(graph_data.index.values)])

  # Put a legend to the right of the current axis if it needs a legend
  if isinstance(graph_data, pd.core.frame.DataFrame):
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=5, mode="expand", borderaxespad=0., fontsize=8,
             frameon=False)

  #Remove edges
  ax.spines["top"].set_visible(False)
  ax.spines["bottom"].set_visible(False)
  ax.spines["right"].set_visible(False)
  ax.spines["left"].set_visible(False)

  #Format y-axis based on the size of the data
  if np.amax(y) > 1000:
    y_format = tkr.FuncFormatter(lambda x, p: format(int(x), ','))
    ax.yaxis.set_major_formatter(y_format)
  else:
    ax.set_ylim([np.amin(y) * .9, np.amax(y) * 1.1])

  print('Writing file: ' + title.replace(" ", "-").lower() + '.png')
  plt.savefig(title.replace(" ","-").lower() + ".png", bbox_inches='tight')

  print('Writing file: ' + title.replace(" ","-").lower() + '.csv')
  graph_data.to_csv(title.replace(" ","-").lower() + ".csv")
