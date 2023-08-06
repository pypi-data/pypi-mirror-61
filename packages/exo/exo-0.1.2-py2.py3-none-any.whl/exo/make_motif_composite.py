#!/usr/bin/python
from __future__ import division


import math
import sys

import click

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

import numpy

import pandas as pd

matplotlib.use('Agg')


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(options_metavar='<options>', context_settings=CONTEXT_SETTINGS)
@click.argument('sample', type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False,))
@click.option('-t', '--title', metavar="<string>", default=' ', prompt=True, show_default=' ', help='Plot Title')
@click.option('-d', '--dpi', metavar="<int>", type=int, default=100, prompt=True, show_default='100', help='Plot pixel density')
@click.option('-o', '--out', metavar="<string>", default='motifcomposite_sense_antisense.png', prompt=True, show_default='motifcomposite_sense_antisense.png', help='output filename')
def cli(sample, title, dpi, out):
    """
    Accepts a strand separate tagPileUP CDT (tabular) file to create a composite plot.

    \b
    Sense strand is blue. [defualt]
    AntiSense strand is red. [default]

    """
    click.echo('\n' + '.' * 50)

    # reading the CDT file.
    try:
        signalData = pd.read_csv(sample, sep='\t', index_col=0)
    except IOError:
        print("\nUnable to OPEN input files !\n")
        sys.exit(1)

    # prepare PlotData, remove extra decimal values
    signalData = signalData.round(decimals=3)

    # General DEBUG
    print(signalData.index)
    print(signalData.shape)

    # retrieve the row index from the dataframe
    rowIndex = list(signalData.index)

    # retrieve data for Sense strand
    sx = list(signalData.loc[rowIndex[0]])

    # retrieve values for y axis and convert them to float
    sy = list(signalData.columns)
    sy = list(map(float, sy))

    # prepare PlotData for antisense strand
    cx = list(signalData.loc[rowIndex[1]])

    # convert antisense data values to negative, to plot it below the sense data.
    x1 = [-i for i in cx]

    fig, ax = plt.subplots()
    # ax = plt.axes([0, 0, 1, 1])

    plt.plot(sy, sx, 'b', sy, x1, 'r')  # plotting the graph

    # adding the fill color for both the strands.
    d = numpy.zeros(len(sx))
    d1 = numpy.zeros(len(sx))
    plt.fill_between(sy, sx, where=sx >= d, interpolate=False, color="blue")
    plt.fill_between(sy, x1, where=sx >= d1, interpolate=False, color="red")

    # Option to draw a vertical line at origin on x-axis
    # plt.axvline(x=0, color='black', linestyle='--')

    # creating the grid lines
    # plt.grid(linestyle='--', linewidth=0.5)

    plt.gca().xaxis.grid(True, linestyle='--', linewidth=0.5)

    # adding custom xticks and yticks
    plt.xticks(range(-100, 150, 50), fontsize=14)

    # retrieve the yticks
    my_yticks = ax.get_yticks()
    # pprint.pprint(my_yticks)
    lastTick = int(len(my_yticks) - 1)

    # Handle edge cases, not to round off to -0.0
    if my_yticks[0] <= -1.0:
        # setting the ylim for the y-axis
        ax.set_ylim(math.ceil(my_yticks[0]), math.ceil(my_yticks[lastTick]))
        # setting the ticks for y-axis
        plt.yticks([math.ceil(my_yticks[0]), 0, math.ceil(
            my_yticks[lastTick])], fontsize=14)
    else:
        # setting the ylim for the y-axis
        ax.set_ylim(my_yticks[0], math.ceil(my_yticks[lastTick]))
        # setting the ticks for y-axis
        plt.yticks([my_yticks[0], 0, math.ceil(
            my_yticks[lastTick])], fontsize=14)

    plt.ylabel('Tags', fontsize=18)

    # setting the padding space between the y-axis label and the y-axis
    if math.ceil(my_yticks[lastTick]) < 10:
        ax.yaxis.labelpad = -10
    else:
        ax.yaxis.labelpad = -15

    # to increase the width of the plot borders and tick width
    plt.setp(ax.spines.values(), linewidth=2)
    plt.tick_params(length=8, width=2)

    # if you chose to not include the xticks , since they are similar to heatmap x-axis ticks
    # plt.xticks([-100,0,100])
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.xaxis.set_ticks_position('none')

    # plt.yticks(range(-10,12,2))
    # plt.xticks([-500,0,500])

    # start,end=ax.get_ylim()
    # ax.set_ylim(start-1,end+1)

    # Customizing the border/ spines on each side of the plot.
    # frame1 = plt.gca()
    # frame1.axes.xaxis.set_ticklabels([])
    # frame1.axes.yaxis.set_ticklabels([])
    # frame1.axes.spines['top'].set_visible(False)
    # frame1.axes.spines['right'].set_visible(False)
    # frame1.axes.spines['bottom'].set_visible(False)
    # frame1.axes.spines['left'].set_visible(False)

    # plt.show()
    plt.title(title, fontsize=25)
    # setting the margins
    plt.margins(0.01)

    # saving the image at 300dpi , web standard for printing images.
    plt.savefig(out, facecolor=None, dpi=dpi, pad_inches=0)
    click.echo('\n' + '.' * 50)
